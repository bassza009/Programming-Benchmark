#!/usr/bin/env python3
import os
import glob
import json
import csv
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COMPARE_SCRIPT = os.path.join(os.path.dirname(SCRIPT_DIR), "compare_results.py")
SUMMARY_MD = os.path.join(SCRIPT_DIR, "SUMMARY.md")
SUMMARY_CSV = os.path.join(SCRIPT_DIR, "SUMMARY.csv")

def generate_markdown(json_files):
    output = []
    output.append("# 📊 Web Framework Benchmark: Comprehensive Summary\n")
    output.append("Multi-language performance evaluation across **Docker Containerized** and **Bare Metal (Host)** environments.\n")

    # Load all datasets into memory
    loaded_data = {}
    for fpath in json_files:
        fname = os.path.basename(fpath)
        with open(fpath, "r") as f:
            loaded_data[fname] = json.load(f)

    # 1. Unified Side-by-Side Comparison Section (Dkr vs BME)
    output.append("## ⚡ Executive Comparison: Docker vs Bare Metal (`/raw/1table` - Light Tier)\n")
    output.append("| Suite | Language | Docker (Req/s) | Bare Metal (Req/s) | Docker Latency | BME Latency | Overhead / Gain |")
    output.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

    # Check for matched suites (e.g. get_no_index)
    suites = set([k.replace("_dkr.json", "").replace("_bme.json", "").replace(".json", "") for k in loaded_data.keys()])
    for s in sorted(suites):
        dkr_key = f"{s}_dkr.json"
        bme_key = f"{s}_bme.json"
        dkr_data = loaded_data.get(dkr_key)
        bme_data = loaded_data.get(bme_key)

        langs = set()
        if dkr_data:
            langs.update(dkr_data.keys())
        if bme_data:
            langs.update(bme_data.keys())

        for lang in sorted(langs):
            # Extract 1table min tier
            dkr_rps = "-"
            dkr_lat = "-"
            bme_rps = "-"
            bme_lat = "-"
            gain = "N/A"

            if dkr_data and lang in dkr_data:
                d_val = (
                    dkr_data[lang].get("tiers", {}).get("min", {}).get("endpoints", {}).get("/raw/1table")
                    or dkr_data[lang].get("tiers", {}).get("min", {}).get("endpoints", {}).get("/raw/post/1table")
                    or dkr_data[lang].get("endpoints", {}).get("/raw/1table")
                    or dkr_data[lang].get("endpoints", {}).get("/raw/post/1table")
                    or {}
                )
                if d_val:
                    r = d_val.get("requests_per_sec", 0.0)
                    l = d_val.get("latency_mean_ms", 0.0)
                    dkr_rps = f"{r:,.2f}"
                    dkr_lat = f"{l:.2f}ms"
                    d_r_num = r

            if bme_data and lang in bme_data:
                b_val = (
                    bme_data[lang].get("tiers", {}).get("min", {}).get("endpoints", {}).get("/raw/1table")
                    or bme_data[lang].get("tiers", {}).get("min", {}).get("endpoints", {}).get("/raw/post/1table")
                    or bme_data[lang].get("endpoints", {}).get("/raw/1table")
                    or bme_data[lang].get("endpoints", {}).get("/raw/post/1table")
                    or {}
                )
                if b_val:
                    r = b_val.get("requests_per_sec", 0.0)
                    l = b_val.get("latency_mean_ms", 0.0)
                    bme_rps = f"{r:,.2f}"
                    bme_lat = f"{l:.2f}ms"
                    b_r_num = r

            if dkr_rps != "-" and bme_rps != "-":
                if d_r_num > 0:
                    diff = ((b_r_num - d_r_num) / d_r_num) * 100
                    gain = f"{'+' if diff > 0 else ''}{diff:.1f}% BME"

            output.append(f"| **{s}** | **{lang}** | {dkr_rps} | {bme_rps} | {dkr_lat} | {bme_lat} | {gain} |")
    output.append("\n---\n")

    # 2. Detailed Breakdown by Suite
    for fpath in json_files:
        fname = os.path.basename(fpath)
        is_bme = "_bme.json" in fname
        env_label = "🖥️ Bare Metal (Host)" if is_bme else "🐳 Docker (Container)"
        suite_name = fname.replace("_dkr.json", "").replace("_bme.json", "").replace(".json", "")

        output.append(f"## 📁 Suite: `{suite_name}` — {env_label}\n")
        
        try:
            res = subprocess.run(["python3", COMPARE_SCRIPT, fpath], capture_output=True, text=True, check=True)
            output.append(res.stdout.strip())
            output.append("\n---\n")
        except Exception as e:
            output.append(f"Error reading {fname}: {e}\n")

    with open(SUMMARY_MD, "w") as f:
        f.write("\n".join(output))
    print(f"Markdown summary written to {SUMMARY_MD}")

def generate_csv(json_files):
    rows = []
    headers = [
        "Suite",
        "Environment",
        "Tier",
        "Threads",
        "Connections",
        "Duration",
        "Endpoint",
        "Rank",
        "Language",
        "Requests_Per_Sec",
        "Avg_Latency_ms",
        "Max_Latency_ms",
        "Errors"
    ]

    for fpath in json_files:
        fname = os.path.basename(fpath)
        if "_dkr" in fname:
            env = "Docker"
            suite = fname.replace("_dkr.json", "")
        elif "_bme" in fname:
            env = "Bare Metal"
            suite = fname.replace("_bme.json", "")
        else:
            env = "Unknown"
            suite = fname.replace(".json", "")

        with open(fpath, "r") as f:
            data = json.load(f)

        first_lang = next(iter(data.values()))
        is_multi_tier = "tiers" in first_lang

        if is_multi_tier:
            for tier, tier_data in first_lang["tiers"].items():
                t_cfg = tier_data.get("config", {})
                tier_name = t_cfg.get("name", tier)
                threads = t_cfg.get("threads", "")
                conns = t_cfg.get("connections", "")
                dur = t_cfg.get("duration", "")
                endpoints = list(tier_data["endpoints"].keys())

                for ep in endpoints:
                    ep_data = []
                    for lang_name, lang_data in data.items():
                        res = lang_data["tiers"][tier]["endpoints"].get(ep, {})
                        rps = res.get("requests_per_sec", 0.0)
                        lat_avg = res.get("latency_mean_ms", 0.0)
                        lat_max = res.get("latency_max_ms", 0.0)
                        errs = res.get("errors", 0)
                        ep_data.append((lang_name, rps, lat_avg, lat_max, errs))

                    ep_data.sort(key=lambda x: x[1], reverse=True)

                    for rank, (lang, rps, lat_avg, lat_max, errs) in enumerate(ep_data, start=1):
                        rows.append([
                            suite,
                            env,
                            tier_name,
                            threads,
                            conns,
                            dur,
                            ep,
                            rank,
                            lang,
                            f"{rps:.2f}",
                            f"{lat_avg:.2f}",
                            f"{lat_max:.2f}",
                            errs
                        ])
        else:
            for ep in first_lang["endpoints"].keys():
                ep_data = []
                for lang_name, lang_data in data.items():
                    res = lang_data["endpoints"].get(ep, {})
                    rps = res.get("requests_per_sec", 0.0)
                    lat_avg = res.get("latency_mean_ms", 0.0)
                    lat_max = res.get("latency_max_ms", 0.0)
                    errs = res.get("errors", 0)
                    ep_data.append((lang_name, rps, lat_avg, lat_max, errs))

                ep_data.sort(key=lambda x: x[1], reverse=True)

                for rank, (lang, rps, lat_avg, lat_max, errs) in enumerate(ep_data, start=1):
                    rows.append([
                        suite,
                        env,
                        "Default",
                        "",
                        "",
                        "",
                        ep,
                        rank,
                        lang,
                        f"{rps:.2f}",
                        f"{lat_avg:.2f}",
                        f"{lat_max:.2f}",
                        errs
                    ])

    with open(SUMMARY_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"CSV summary written to {SUMMARY_CSV} ({len(rows)} data rows)")

def main():
    json_files = sorted(glob.glob(os.path.join(SCRIPT_DIR, "*.json")))
    if not json_files:
        print("No result JSON files found in", SCRIPT_DIR)
        return
    generate_markdown(json_files)
    generate_csv(json_files)

if __name__ == "__main__":
    main()
