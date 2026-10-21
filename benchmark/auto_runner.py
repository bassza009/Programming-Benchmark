#!/usr/bin/env python3
"""
benchmark/auto_runner.py
Extensible Multi-Language Algorithm Benchmark Runner (Interactive & Recursive Suites).

Features:
- Plugin/Config-driven language registry (`languages.json`) & task registry (`tasks.json`).
- Easily add new languages via `--register-lang` or editing `languages.json`.
- Pre-compiles compiled languages (Go, Java, Rust, C++) before timing so compiler startup never skews results.
- Uses persistent Docker containers (`docker exec`) to eliminate container creation overhead during iterations.
- Integrates `thermal_guard.py` between runs to protect CPU/motherboard VRMs & capacitors (`<= 75°C`).
- Outputs hyperfine-compatible JSON + CSV + Markdown summaries with Mean, SD, 95% CI, Median, Min, Max, and CPU temperatures.
"""

import argparse
from datetime import datetime, timezone
import json
import math
import os
import shlex
import statistics
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(BASE_DIR)

sys.path.insert(0, BASE_DIR)
from thermal_guard import check_and_cool, get_cpu_temp

LANGUAGES_FILE = os.path.join(BASE_DIR, "languages.json")
TASKS_FILE = os.path.join(BASE_DIR, "tasks.json")

T_CRIT_95 = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447,  7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    15: 2.131, 19: 2.093, 20: 2.086, 30: 2.042
}


def get_t_crit(n):
    if n <= 1:
        return 1.96
    df = n - 1
    if df in T_CRIT_95:
        return T_CRIT_95[df]
    for k in sorted(T_CRIT_95.keys()):
        if df <= k:
            return T_CRIT_95[k]
    return 1.96


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def format_cmd_tokens(tokens, context):
    if not tokens:
        return None
    if isinstance(tokens, str):
        tokens = shlex.split(tokens)
    return [t.format(**context) for t in tokens]


def run_timed_process(cmd, cwd):
    """
    Executes `cmd` in `cwd`, measuring exact wall-clock time (`perf_counter`)
    and child CPU user/system time via `os.wait4`.
    """
    start_wall = time.perf_counter()
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    _, status, rusage = os.wait4(proc.pid, 0)
    elapsed = time.perf_counter() - start_wall
    stderr_out = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
    if proc.stderr:
        proc.stderr.close()

    exit_code = os.waitstatus_to_exitcode(status) if hasattr(os, "waitstatus_to_exitcode") else (status >> 8)
    return {
        "elapsed": elapsed,
        "user": float(rusage.ru_utime),
        "system": float(rusage.ru_stime),
        "exit_code": exit_code,
        "stderr": stderr_out.strip()
    }


def compute_summary_entry(cmd_str, times, users, systems, exit_codes, temps, started_at, completed_at, elapsed_sec):
    n = len(times)
    if n == 0:
        return {
            "command": cmd_str,
            "mean": 0.0,
            "stddev": 0.0,
            "median": 0.0,
            "user": 0.0,
            "system": 0.0,
            "min": 0.0,
            "max": 0.0,
            "ci95_margin": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
            "cpu_temp_avg_c": 0.0,
            "cpu_temp_max_c": 0.0,
            "started_at": started_at,
            "completed_at": completed_at,
            "elapsed_sec": round(elapsed_sec, 2),
            "times": [],
            "exit_codes": []
        }

    mean_val = sum(times) / n
    sd_val = statistics.stdev(times) if n > 1 else 0.0
    med_val = statistics.median(times)
    min_val = min(times)
    max_val = max(times)
    user_mean = sum(users) / n if users else 0.0
    sys_mean = sum(systems) / n if systems else 0.0

    t_crit = get_t_crit(n)
    ci95_margin = t_crit * (sd_val / math.sqrt(n)) if n > 1 else 0.0
    valid_temps = [t for t in temps if t and t > 0]
    avg_temp = round(sum(valid_temps) / len(valid_temps), 1) if valid_temps else 0.0
    max_temp = round(max(valid_temps), 1) if valid_temps else 0.0

    return {
        "command": cmd_str,
        "mean": mean_val,
        "stddev": sd_val,
        "median": med_val,
        "user": user_mean,
        "system": sys_mean,
        "min": min_val,
        "max": max_val,
        "ci95_margin": ci95_margin,
        "ci95_low": max(0.0, mean_val - ci95_margin),
        "ci95_high": mean_val + ci95_margin,
        "cpu_temp_avg_c": avg_temp,
        "cpu_temp_max_c": max_temp,
        "started_at": started_at,
        "completed_at": completed_at,
        "elapsed_sec": round(elapsed_sec, 2),
        "times": times,
        "exit_codes": exit_codes
    }


def register_language(args):
    langs = load_json(LANGUAGES_FILE)
    key = args.register_lang.lower().strip()
    ext = args.ext if args.ext.startswith(".") else f".{args.ext}"
    compile_cmd = shlex.split(args.compile_cmd) if args.compile_cmd else None
    run_cmd = shlex.split(args.run_cmd) if args.run_cmd else [key, "{source}"]

    langs[key] = {
        "name": args.name or key.capitalize(),
        "csv_label": args.csv_label or (args.name or key.capitalize()),
        "extension": ext,
        "docker_image": args.docker_image or f"{key}:latest",
        "compile_cmd": compile_cmd,
        "run_cmd": run_cmd,
        "enabled": True
    }
    save_json(LANGUAGES_FILE, langs)
    print(f"[+] Registered language '{key}' ({langs[key]['name']}) in {LANGUAGES_FILE}")


def start_docker_container(container_name, image, host_dir):
    subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
    cmd = [
        "docker", "run", "-d", "--rm",
        "--name", container_name,
        "-v", f"{host_dir}:/app",
        "-w", "/app",
        image,
        "sleep", "infinity"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Failed to start Docker container {container_name} ({image}): {res.stderr.strip()}")


def stop_docker_container(container_name):
    subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)


def export_task_csvs(task_key, task_cfg, languages_cfg):
    res_dir = os.path.join(REPO_ROOT, task_cfg["results_dir"])
    json_dir = os.path.join(res_dir, "json")
    if not os.path.exists(json_dir):
        return

    headers = [""]
    values = ["Avg. duration"]

    for lang_key, lang_cfg in languages_cfg.items():
        json_path = os.path.join(json_dir, f"{lang_key}.json")
        if not os.path.exists(json_path):
            continue
        try:
            data = load_json(json_path)
            results = data.get("results", [])
        except Exception:
            continue

        bme_mean = None
        dkr_mean = None
        for r in results:
            if "docker" in r.get("command", "").lower():
                dkr_mean = r.get("mean")
            else:
                bme_mean = r.get("mean")

        label = lang_cfg.get("csv_label", lang_cfg["name"])
        if bme_mean is not None:
            headers.append(f"{label}(BME.)")
            values.append(f"{bme_mean:.6f}")
        if dkr_mean is not None:
            headers.append(f"{label}(Dkr.)")
            values.append(f"{dkr_mean:.6f}")

    if len(headers) <= 1:
        return

    pad_commas = "," * (len(headers) - 1)
    title_line = f"{task_cfg['title_en']} ({task_cfg['description']}){pad_commas}\n"
    header_line = ",".join(headers) + "\n"
    unit_line = ",ระยะเวลา(S.)" + ("," * (len(headers) - 2)) + "\n"
    val_line = ",".join(values) + "\n"

    csv_path = os.path.join(res_dir, task_cfg["csv_name"])
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(title_line + header_line + unit_line + val_line)

    if task_cfg.get("csv_delete_name"):
        del_path = os.path.join(res_dir, task_cfg["csv_delete_name"])
        with open(del_path, "w", encoding="utf-8") as f:
            f.write(title_line + header_line + val_line)


def generate_algo_summary(tasks_cfg, languages_cfg):
    md_lines = [
        "# Algorithm Benchmark Summary (Interactive & Recursive Suites)",
        "",
        f"> **Generated At**: `{datetime.now(timezone.utc).isoformat()}`",
        "",
        "| Category | Task | Language | BME Mean ± SD (s) | BME 95% CI (s) | Docker Mean ± SD (s) | Docker 95% CI (s) | BME Median (s) | Docker Median (s) | Overhead (%) | Max CPU Temp (°C) | Runs |",
        "| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]
    csv_lines = [
        "category,task,language,bme_mean_s,bme_sd_s,bme_ci95_margin_s,bme_median_s,bme_min_s,bme_max_s,dkr_mean_s,dkr_sd_s,dkr_ci95_margin_s,dkr_median_s,dkr_min_s,dkr_max_s,docker_overhead_pct,cpu_temp_max_c,runs"
    ]

    for task_key, task_cfg in tasks_cfg.items():
        json_dir = os.path.join(REPO_ROOT, task_cfg["results_dir"], "json")
        if not os.path.exists(json_dir):
            continue

        for lang_key, lang_cfg in languages_cfg.items():
            jpath = os.path.join(json_dir, f"{lang_key}.json")
            if not os.path.exists(jpath):
                continue
            try:
                jdata = load_json(jpath)
            except Exception:
                continue

            bme = None
            dkr = None
            for r in jdata.get("results", []):
                if "docker" in r.get("command", "").lower():
                    dkr = r
                else:
                    bme = r

            if not bme and not dkr:
                continue

            bme_m = bme.get("mean", 0.0) if bme else 0.0
            bme_sd = bme.get("stddev", 0.0) if bme else 0.0
            bme_ci = bme.get("ci95_margin", get_t_crit(len(bme.get("times", []))) * (bme_sd / math.sqrt(max(1, len(bme.get("times", [])))))) if bme else 0.0
            bme_med = bme.get("median", 0.0) if bme else 0.0

            dkr_m = dkr.get("mean", 0.0) if dkr else 0.0
            dkr_sd = dkr.get("stddev", 0.0) if dkr else 0.0
            dkr_ci = dkr.get("ci95_margin", get_t_crit(len(dkr.get("times", []))) * (dkr_sd / math.sqrt(max(1, len(dkr.get("times", [])))))) if dkr else 0.0
            dkr_med = dkr.get("median", 0.0) if dkr else 0.0

            overhead_pct = ((dkr_m - bme_m) / bme_m * 100.0) if (bme_m > 0 and dkr_m > 0) else 0.0
            max_temp = max(
                (bme.get("cpu_temp_max_c", 0.0) if bme else 0.0),
                (dkr.get("cpu_temp_max_c", 0.0) if dkr else 0.0)
            )
            runs_cnt = len((bme or dkr).get("times", []))

            md_lines.append(
                f"| {task_cfg['category']} | **{task_cfg['title_en']}** | {lang_cfg['name']} | "
                f"{bme_m:.4f} ± {bme_sd:.4f} | ±{bme_ci:.4f} | "
                f"{dkr_m:.4f} ± {dkr_sd:.4f} | ±{dkr_ci:.4f} | "
                f"{bme_med:.4f} | {dkr_med:.4f} | {overhead_pct:+.2f}% | "
                f"{max_temp:.1f} | {runs_cnt} |"
            )
            csv_lines.append(
                f"{task_cfg['category']},{task_key},{lang_cfg['name']},"
                f"{bme_m:.6f},{bme_sd:.6f},{bme_ci:.6f},{bme_med:.6f},{bme.get('min',0.0) if bme else 0.0:.6f},{bme.get('max',0.0) if bme else 0.0:.6f},"
                f"{dkr_m:.6f},{dkr_sd:.6f},{dkr_ci:.6f},{dkr_med:.6f},{dkr.get('min',0.0) if dkr else 0.0:.6f},{dkr.get('max',0.0) if dkr else 0.0:.6f},"
                f"{overhead_pct:.2f},{max_temp:.1f},{runs_cnt}"
            )

    os.makedirs(os.path.join(REPO_ROOT, "results"), exist_ok=True)
    with open(os.path.join(REPO_ROOT, "results", "ALGO_SUMMARY.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")
    with open(os.path.join(REPO_ROOT, "results", "ALGO_SUMMARY.csv"), "w", encoding="utf-8") as f:
        f.write("\n".join(csv_lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Extensible Interactive & Recursive Algorithm Benchmark Runner")
    parser.add_argument("--category", choices=["interactive", "recursive", "all"], default="all", help="Benchmark category")
    parser.add_argument("--task", default="all", help="Specific task key (door, bubble_sort, prime, prisoners, matrix, factorial, fibonacci, or all)")
    parser.add_argument("--lang", default="all", help="Specific language key (go, java, node, php, python, etc. or all)")
    parser.add_argument("--env", choices=["bme", "dkr", "all"], default="all", help="Environment to execute (bme, dkr, all)")
    parser.add_argument("--runs", type=int, default=20, help="Number of timed iterations per language/environment (default: 20)")
    parser.add_argument("--warmup", type=int, default=3, help="Number of untimed warmup iterations (default: 3)")
    parser.add_argument("--resume", action="store_true", help="Resume from existing JSON files if already completed")

    # Language Registration CLI
    parser.add_argument("--register-lang", help="Register a new language key in languages.json and exit")
    parser.add_argument("--name", help="Display name for --register-lang")
    parser.add_argument("--csv-label", help="CSV header label for --register-lang")
    parser.add_argument("--ext", help="File extension (e.g. .rs) for --register-lang")
    parser.add_argument("--docker-image", help="Docker image for --register-lang")
    parser.add_argument("--compile-cmd", help="Compile command template (e.g. 'rustc -O -o {bin} {source}')")
    parser.add_argument("--run-cmd", help="Run command template (e.g. './{bin}')")

    args = parser.parse_args()

    if args.register_lang:
        if not args.ext:
            parser.error("--ext is required when using --register-lang")
        register_language(args)
        return

    languages_cfg = load_json(LANGUAGES_FILE)
    tasks_cfg = load_json(TASKS_FILE)

    selected_tasks = [
        (k, v) for k, v in tasks_cfg.items()
        if (args.category == "all" or v["category"] == args.category)
        and (args.task == "all" or k == args.task)
    ]

    if not selected_tasks:
        print(f"[!] No tasks matched category={args.category}, task={args.task}")
        return

    selected_envs = ["bme", "dkr"] if args.env == "all" else [args.env]

    print("=================================================================")
    print(" PROGRAMMING BENCHMARK: ALGORITHM SUITE RUNNER (EXTENSIBLE)")
    print(f" Tasks: {', '.join(k for k, _ in selected_tasks)}")
    print(f" Environments: {', '.join(selected_envs).upper()} | Warmup: {args.warmup} | Runs: {args.runs}")
    print("=================================================================\n", flush=True)

    for task_key, task_cfg in selected_tasks:
        task_dir = os.path.join(BASE_DIR, task_cfg["source_dir"])
        res_dir = os.path.join(REPO_ROOT, task_cfg["results_dir"])
        json_dir = os.path.join(res_dir, "json")
        os.makedirs(json_dir, exist_ok=True)
        cooldown_sec = task_cfg.get("cooldown_sec", 2)

        print(f"\n>>>> TASK: {task_cfg['title_en']} ({task_cfg['description']}) <<<<", flush=True)

        for lang_key, lang_cfg in languages_cfg.items():
            if not lang_cfg.get("enabled", True):
                continue
            if args.lang != "all" and lang_key != args.lang.lower():
                continue

            src_file = f"{task_cfg['file_prefix']}{lang_cfg['extension']}"
            src_path = os.path.join(task_dir, src_file)
            if not os.path.exists(src_path):
                # Skip languages that don't have a source file for this task yet
                continue

            out_json_path = os.path.join(json_dir, f"{lang_key}.json")
            existing_results = {}
            if os.path.exists(out_json_path):
                try:
                    loaded = load_json(out_json_path)
                    for r in loaded.get("results", []):
                        env_type = "dkr" if "docker" in r.get("command", "").lower() else "bme"
                        existing_results[env_type] = r
                except Exception:
                    pass

            ctx = {
                "task": task_key,
                "source": src_file,
                "class_name": task_cfg["file_prefix"],
                "bin": f"main_{task_key}_{lang_key}"
            }

            for env_mode in selected_envs:
                prev_entry = existing_results.get(env_mode)
                prev_times = prev_entry.get("times", []) if prev_entry else []
                if args.resume and len(prev_times) >= args.runs:
                    print(f"  [SKIP] {lang_cfg['name']} ({env_mode.upper()}) already has {len(prev_times)}/{args.runs} runs.")
                    continue

                check_and_cool(task_key)
                container_name = f"bench-algo-{task_key}-{lang_key}"

                try:
                    if env_mode == "bme":
                        compile_cmd = format_cmd_tokens(lang_cfg.get("compile_cmd"), ctx)
                        if compile_cmd:
                            print(f"  [BME] Compiling {lang_cfg['name']}: {' '.join(compile_cmd)}", flush=True)
                            subprocess.run(compile_cmd, cwd=task_dir, check=True)
                        run_cmd = format_cmd_tokens(lang_cfg["run_cmd"], ctx)
                        cmd_label = " ".join(run_cmd)
                    else:
                        ctx_dkr = dict(ctx)
                        ctx_dkr["bin"] = f"main_{task_key}_{lang_key}_dkr"
                        print(f"  [DKR] Starting container {container_name} ({lang_cfg['docker_image']})...", flush=True)
                        start_docker_container(container_name, lang_cfg["docker_image"], task_dir)
                        compile_cmd = format_cmd_tokens(lang_cfg.get("compile_cmd"), ctx_dkr)
                        if compile_cmd:
                            dkr_compile = ["docker", "exec", container_name] + compile_cmd
                            print(f"  [DKR] Compiling in container: {' '.join(dkr_compile)}", flush=True)
                            subprocess.run(dkr_compile, cwd=task_dir, check=True)
                        inner_run = format_cmd_tokens(lang_cfg["run_cmd"], ctx_dkr)
                        run_cmd = ["docker", "exec", container_name] + inner_run
                        cmd_label = " ".join(run_cmd)

                    # Warmup runs
                    if args.warmup > 0 and not (args.resume and len(prev_times) > 0):
                        print(f"  [{env_mode.upper()}] Warming up {lang_cfg['name']} ({args.warmup} runs)...", flush=True)
                        for _ in range(args.warmup):
                            check_and_cool(task_key)
                            w_res = run_timed_process(run_cmd, cwd=task_dir)
                            if w_res["exit_code"] != 0:
                                raise RuntimeError(f"Warmup failed (exit {w_res['exit_code']}): {w_res['stderr']}")

                    times = list(prev_times) if (args.resume and prev_entry) else []
                    exit_codes = list(prev_entry.get("exit_codes", [])) if (args.resume and prev_entry) else []
                    users = [prev_entry.get("user", 0.0)] * len(times) if (args.resume and prev_entry) else []
                    systems = [prev_entry.get("system", 0.0)] * len(times) if (args.resume and prev_entry) else []
                    temps = [prev_entry.get("cpu_temp_avg_c", get_cpu_temp())] * len(times) if (args.resume and prev_entry) else []
                    start_run_idx = len(times) + 1
                    started_at = (prev_entry.get("started_at") if (args.resume and prev_entry) else None) or datetime.now(timezone.utc).isoformat()
                    t0_wall = time.time() - (prev_entry.get("elapsed_sec", 0.0) if (args.resume and prev_entry) else 0.0)

                    for run_idx in range(start_run_idx, args.runs + 1):
                        check_and_cool(task_key)
                        r_out = run_timed_process(run_cmd, cwd=task_dir)
                        post_temp = check_and_cool(task_key)

                        if r_out["exit_code"] != 0:
                            print(f"  [!] Run {run_idx} exited with code {r_out['exit_code']}: {r_out['stderr']}", file=sys.stderr)

                        times.append(r_out["elapsed"])
                        users.append(r_out["user"])
                        systems.append(r_out["system"])
                        exit_codes.append(r_out["exit_code"])
                        temps.append(post_temp)

                        completed_at = datetime.now(timezone.utc).isoformat()
                        elapsed_total = time.time() - t0_wall
                        entry = compute_summary_entry(
                            cmd_label, times, users, systems, exit_codes, temps,
                            started_at, completed_at, elapsed_total
                        )
                        existing_results[env_mode] = entry

                        # Persist immediately after every single run
                        ordered_list = []
                        if "bme" in existing_results:
                            ordered_list.append(existing_results["bme"])
                        if "dkr" in existing_results:
                            ordered_list.append(existing_results["dkr"])
                        save_json(out_json_path, {"results": ordered_list})

                        print(
                            f"    -> [{env_mode.upper()}] {lang_cfg['name']} Run {run_idx}/{args.runs}: "
                            f"{r_out['elapsed']:.4f}s | CPU: {post_temp:.1f}°C",
                            flush=True
                        )
                        if run_idx < args.runs:
                            time.sleep(cooldown_sec)

                    final_entry = existing_results[env_mode]
                    print(
                        f"  ==> [{env_mode.upper()}] {lang_cfg['name']} Average ({args.runs} runs): "
                        f"{final_entry['mean']:.4f}s ± {final_entry['stddev']:.4f}s "
                        f"(Median: {final_entry['median']:.4f}s)",
                        flush=True
                    )

                finally:
                    if env_mode == "dkr":
                        stop_docker_container(container_name)
                    # Clean up temporary compiled binaries
                    for suffix in ["", "_dkr"]:
                        bin_path = os.path.join(task_dir, f"main_{task_key}_{lang_key}{suffix}")
                        if os.path.exists(bin_path):
                            try:
                                os.remove(bin_path)
                            except Exception:
                                pass

        export_task_csvs(task_key, task_cfg, languages_cfg)

    generate_algo_summary(tasks_cfg, languages_cfg)
    print("\n=================================================================")
    print(" ALGORITHM BENCHMARKS & SUMMARIES COMPLETED SUCCESSFULLY!")
    print(" Summary saved to: results/ALGO_SUMMARY.md & results/ALGO_SUMMARY.csv")
    print("=================================================================\n", flush=True)


if __name__ == "__main__":
    main()
