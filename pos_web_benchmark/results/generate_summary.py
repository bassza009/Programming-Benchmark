#!/usr/bin/env python3
import os
import sys
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
    output.append("# Web Framework Benchmark: Comprehensive Summary\n")
    output.append("Multi-language performance evaluation across **Docker Containerized** and **Bare Metal (Host)** environments.\n")
    output.append(r"Statistical metrics include Arithmetic Mean ($\bar{X}$), Standard Deviation ($\sigma$), 95% Confidence Interval (95% CI), and Latency Percentiles ($p_{50}, p_{90}, p_{95}, p_{99}$)." + "\n")

    # Load all datasets into memory
    loaded_data = {}
    for fpath in json_files:
        fname = os.path.basename(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            loaded_data[fname] = json.load(f)

    # 1. Unified Side-by-Side Comparison Section (Dkr vs BME)
    output.append("## Executive Comparison: Docker vs Bare Metal (`/raw/1table` - Light Tier)\n")
    output.append("| Suite | Language | Docker (Req/s ± SD) | Bare Metal (Req/s ± SD) | Docker p50 / p95 (ms) | BME p50 / p95 (ms) | Overhead / Gain |")
    output.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

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
            dkr_str = "-"
            bme_str = "-"
            dkr_pct = "-"
            bme_pct = "-"
            gain = "N/A"
            d_r_num = 0.0
            b_r_num = 0.0

            if dkr_data and lang in dkr_data:
                tiers_dict = dkr_data[lang].get("tiers", {})
                first_tier = next(iter(tiers_dict.values()), {}) if tiers_dict else {}
                d_val = (
                    tiers_dict.get("poc", {}).get("endpoints", {}).get("/raw/1table")
                    or tiers_dict.get("poc", {}).get("endpoints", {}).get("/raw/post/1table")
                    or tiers_dict.get("min", {}).get("endpoints", {}).get("/raw/1table")
                    or tiers_dict.get("min", {}).get("endpoints", {}).get("/raw/post/1table")
                    or first_tier.get("endpoints", {}).get("/raw/1table")
                    or first_tier.get("endpoints", {}).get("/raw/post/1table")
                    or dkr_data[lang].get("endpoints", {}).get("/raw/1table")
                    or dkr_data[lang].get("endpoints", {}).get("/raw/post/1table")
                    or {}
                )
                if d_val:
                    r = d_val.get("requests_per_sec", 0.0)
                    r_sd = d_val.get("rps_stdev", 0.0)
                    l_mean = d_val.get("latency_mean_ms", 0.0)
                    p50 = d_val.get("latency_p50_ms", l_mean)
                    p95 = d_val.get("latency_p95_ms", l_mean)
                    d_r_num = r
                    dkr_str = f"{r:,.2f}" if r_sd == 0 else f"{r:,.2f} ± {r_sd:.2f}"
                    dkr_pct = f"{p50:.2f}ms / {p95:.2f}ms"

            if bme_data and lang in bme_data:
                tiers_dict = bme_data[lang].get("tiers", {})
                first_tier = next(iter(tiers_dict.values()), {}) if tiers_dict else {}
                b_val = (
                    tiers_dict.get("poc", {}).get("endpoints", {}).get("/raw/1table")
                    or tiers_dict.get("poc", {}).get("endpoints", {}).get("/raw/post/1table")
                    or tiers_dict.get("min", {}).get("endpoints", {}).get("/raw/1table")
                    or tiers_dict.get("min", {}).get("endpoints", {}).get("/raw/post/1table")
                    or first_tier.get("endpoints", {}).get("/raw/1table")
                    or first_tier.get("endpoints", {}).get("/raw/post/1table")
                    or bme_data[lang].get("endpoints", {}).get("/raw/1table")
                    or bme_data[lang].get("endpoints", {}).get("/raw/post/1table")
                    or {}
                )
                if b_val:
                    r = b_val.get("requests_per_sec", 0.0)
                    r_sd = b_val.get("rps_stdev", 0.0)
                    l_mean = b_val.get("latency_mean_ms", 0.0)
                    p50 = b_val.get("latency_p50_ms", l_mean)
                    p95 = b_val.get("latency_p95_ms", l_mean)
                    b_r_num = r
                    bme_str = f"{r:,.2f}" if r_sd == 0 else f"{r:,.2f} ± {r_sd:.2f}"
                    bme_pct = f"{p50:.2f}ms / {p95:.2f}ms"

            if dkr_str != "-" and bme_str != "-":
                if d_r_num > 0:
                    diff = ((b_r_num - d_r_num) / d_r_num) * 100
                    gain = f"{'+' if diff > 0 else ''}{diff:.1f}% BME"

            output.append(f"| **{s}** | **{lang}** | {dkr_str} | {bme_str} | {dkr_pct} | {bme_pct} | {gain} |")
        output.append("\n---\n")

    # 2. Detailed Breakdown by Suite
    for fpath in json_files:
        fname = os.path.basename(fpath)
        is_bme = "_bme.json" in fname
        env_label = "Bare Metal (Host)" if is_bme else "Docker (Container)"
        suite_name = fname.replace("_dkr.json", "").replace("_bme.json", "").replace(".json", "")

        output.append(f"## Suite: `{suite_name}` — {env_label}\n")
        
        try:
            res = subprocess.run([sys.executable, COMPARE_SCRIPT, fpath], capture_output=True, text=True, check=True)
            output.append(res.stdout.strip())
            output.append("\n---\n")
        except Exception as e:
            output.append(f"Error reading {fname}: {e}\n")

    with open(SUMMARY_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print(f"Markdown summary written to {SUMMARY_MD}")

def clean_ep_name(ep):
    return ep.replace("/raw/post/", "").replace("/raw/", "")

def generate_csv(json_files):
    rows = []
    headers = [
        "Suite",
        "Environment",
        "Tier",
        "Language",
        "Endpoint",
        "Requests/sec (Mean)",
        "Requests/sec (SD)",
        "Requests/sec (95% CI Low)",
        "Requests/sec (95% CI High)",
        "Latency Mean (ms)",
        "Latency SD (ms)",
        "Latency (95% CI Low)",
        "Latency (95% CI High)",
        "Latency p50 (ms)",
        "Latency p90 (ms)",
        "Latency p95 (ms)",
        "Latency p99 (ms)",
        "Latency Max (ms)",
        "Total Errors"
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

        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        first_lang = next(iter(data.values()))
        is_multi_tier = "tiers" in first_lang

        if is_multi_tier:
            for tier, tier_data in first_lang["tiers"].items():
                tier_name = tier_data.get("config", {}).get("name", tier)

                for lang_name in sorted(data.keys()):
                    lang_data = data[lang_name]
                    tier_info = lang_data.get("tiers", {}).get(tier)
                    if not tier_info:
                        continue
                    endpoints = tier_info.get("endpoints", {})
                    
                    for ep_key, ep_res in endpoints.items():
                        if isinstance(ep_res, dict) and "average" in ep_res:
                            ep_res = ep_res["average"]

                        rps = ep_res.get("requests_per_sec", 0.0)
                        rps_sd = ep_res.get("rps_stdev", 0.0)
                        rps_ci_low = ep_res.get("rps_ci95_low", rps)
                        rps_ci_high = ep_res.get("rps_ci95_high", rps)

                        lat_mean = ep_res.get("latency_mean_ms", 0.0)
                        lat_sd = ep_res.get("latency_stdev_ms", 0.0)
                        lat_ci_low = ep_res.get("latency_ci95_low", lat_mean)
                        lat_ci_high = ep_res.get("latency_ci95_high", lat_mean)

                        lat_p50 = ep_res.get("latency_p50_ms", lat_mean)
                        lat_p90 = ep_res.get("latency_p90_ms", lat_mean)
                        lat_p95 = ep_res.get("latency_p95_ms", lat_mean)
                        lat_p99 = ep_res.get("latency_p99_ms", lat_mean)
                        lat_max = ep_res.get("latency_max_ms", 0.0)
                        errs = ep_res.get("errors", 0)

                        rows.append([
                            suite,
                            env,
                            tier_name,
                            lang_name,
                            ep_key,
                            f"{rps:.2f}",
                            f"{rps_sd:.2f}",
                            f"{rps_ci_low:.2f}",
                            f"{rps_ci_high:.2f}",
                            f"{lat_mean:.2f}",
                            f"{lat_sd:.2f}",
                            f"{lat_ci_low:.2f}",
                            f"{lat_ci_high:.2f}",
                            f"{lat_p50:.2f}",
                            f"{lat_p90:.2f}",
                            f"{lat_p95:.2f}",
                            f"{lat_p99:.2f}",
                            f"{lat_max:.2f}",
                            errs
                        ])
        else:
            for lang_name in sorted(data.keys()):
                lang_data = data[lang_name]
                endpoints = lang_data.get("endpoints", {})
                
                for ep_key, ep_res in endpoints.items():
                    if isinstance(ep_res, dict) and "average" in ep_res:
                        ep_res = ep_res["average"]

                    rps = ep_res.get("requests_per_sec", 0.0)
                    rps_sd = ep_res.get("rps_stdev", 0.0)
                    rps_ci_low = ep_res.get("rps_ci95_low", rps)
                    rps_ci_high = ep_res.get("rps_ci95_high", rps)

                    lat_mean = ep_res.get("latency_mean_ms", 0.0)
                    lat_sd = ep_res.get("latency_stdev_ms", 0.0)
                    lat_ci_low = ep_res.get("latency_ci95_low", lat_mean)
                    lat_ci_high = ep_res.get("latency_ci95_high", lat_mean)

                    lat_p50 = ep_res.get("latency_p50_ms", lat_mean)
                    lat_p90 = ep_res.get("latency_p90_ms", lat_mean)
                    lat_p95 = ep_res.get("latency_p95_ms", lat_mean)
                    lat_p99 = ep_res.get("latency_p99_ms", lat_mean)
                    lat_max = ep_res.get("latency_max_ms", 0.0)
                    errs = ep_res.get("errors", 0)

                    rows.append([
                        suite,
                        env,
                        "Default",
                        lang_name,
                        ep_key,
                        f"{rps:.2f}",
                        f"{rps_sd:.2f}",
                        f"{rps_ci_low:.2f}",
                        f"{rps_ci_high:.2f}",
                        f"{lat_mean:.2f}",
                        f"{lat_sd:.2f}",
                        f"{lat_ci_low:.2f}",
                        f"{lat_ci_high:.2f}",
                        f"{lat_p50:.2f}",
                        f"{lat_p90:.2f}",
                        f"{lat_p95:.2f}",
                        f"{lat_p99:.2f}",
                        f"{lat_max:.2f}",
                        errs
                    ])

    with open(SUMMARY_CSV, "w", newline="", encoding="utf-8") as f:
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
