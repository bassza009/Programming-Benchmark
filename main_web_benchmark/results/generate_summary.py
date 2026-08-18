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
    output.append("# Web Framework Benchmark: Comprehensive Summary\n")
    output.append("Multi-language performance evaluation across **Docker Containerized** and **Bare Metal (Host)** environments.\n")

    # Load all datasets into memory
    loaded_data = {}
    for fpath in json_files:
        fname = os.path.basename(fpath)
        with open(fpath, "r") as f:
            loaded_data[fname] = json.load(f)

    # 1. Unified Side-by-Side Comparison Section (Dkr vs BME)
    output.append("## Executive Comparison: Docker vs Bare Metal (`/raw/1table` - Light Tier)\n")
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
                    l = d_val.get("latency_mean_ms", 0.0)
                    dkr_rps = f"{r:,.2f}"
                    dkr_lat = f"{l:.2f}ms"
                    d_r_num = r

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
        env_label = "Bare Metal (Host)" if is_bme else "Docker (Container)"
        suite_name = fname.replace("_dkr.json", "").replace("_bme.json", "").replace(".json", "")

        output.append(f"## Suite: `{suite_name}` — {env_label}\n")
        
        try:
            res = subprocess.run(["python3", COMPARE_SCRIPT, fpath], capture_output=True, text=True, check=True)
            output.append(res.stdout.strip())
            output.append("\n---\n")
        except Exception as e:
            output.append(f"Error reading {fname}: {e}\n")

    with open(SUMMARY_MD, "w") as f:
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
        "1table (Req/s)",
        "1table Latency (ms)",
        "2table/2join (Req/s)",
        "2table/2join Latency (ms)",
        "3table/3join (Req/s)",
        "3table/3join Latency (ms)",
        "4table/4join (Req/s)",
        "4table/4join Latency (ms)",
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

        with open(fpath, "r") as f:
            data = json.load(f)

        first_lang = next(iter(data.values()))
        is_multi_tier = "tiers" in first_lang

        if is_multi_tier:
            for tier, tier_data in first_lang["tiers"].items():
                tier_name = tier_data.get("config", {}).get("name", tier)

                for lang_name in sorted(data.keys()):
                    lang_data = data[lang_name]
                    endpoints = lang_data["tiers"][tier]["endpoints"]
                    
                    ep_map = {}
                    total_errors = 0
                    for ep_key, ep_res in endpoints.items():
                        cleaned = clean_ep_name(ep_key)
                        rps = ep_res.get("requests_per_sec", 0.0)
                        lat = ep_res.get("latency_mean_ms", 0.0)
                        errs = ep_res.get("errors", 0)
                        total_errors += errs
                        ep_map[cleaned] = (rps, lat)

                    val_1 = ep_map.get("1table", (0.0, 0.0))
                    val_2 = ep_map.get("2join", ep_map.get("2table", (0.0, 0.0)))
                    val_3 = ep_map.get("3join", ep_map.get("3table", (0.0, 0.0)))
                    val_4 = ep_map.get("4join", ep_map.get("4table", (0.0, 0.0)))

                    rows.append([
                        suite,
                        env,
                        tier_name,
                        lang_name,
                        f"{val_1[0]:.2f}",
                        f"{val_1[1]:.2f}",
                        f"{val_2[0]:.2f}",
                        f"{val_2[1]:.2f}",
                        f"{val_3[0]:.2f}",
                        f"{val_3[1]:.2f}",
                        f"{val_4[0]:.2f}",
                        f"{val_4[1]:.2f}",
                        total_errors
                    ])
        else:
            for lang_name in sorted(data.keys()):
                lang_data = data[lang_name]
                endpoints = lang_data.get("endpoints", {})
                
                ep_map = {}
                total_errors = 0
                for ep_key, ep_res in endpoints.items():
                    cleaned = clean_ep_name(ep_key)
                    rps = ep_res.get("requests_per_sec", 0.0)
                    lat = ep_res.get("latency_mean_ms", 0.0)
                    errs = ep_res.get("errors", 0)
                    total_errors += errs
                    ep_map[cleaned] = (rps, lat)

                val_1 = ep_map.get("1table", (0.0, 0.0))
                val_2 = ep_map.get("2join", ep_map.get("2table", (0.0, 0.0)))
                val_3 = ep_map.get("3join", ep_map.get("3table", (0.0, 0.0)))
                val_4 = ep_map.get("4join", ep_map.get("4table", (0.0, 0.0)))

                rows.append([
                    suite,
                    env,
                    "Default",
                    lang_name,
                    f"{val_1[0]:.2f}",
                    f"{val_1[1]:.2f}",
                    f"{val_2[0]:.2f}",
                    f"{val_2[1]:.2f}",
                    f"{val_3[0]:.2f}",
                    f"{val_3[1]:.2f}",
                    f"{val_4[0]:.2f}",
                    f"{val_4[1]:.2f}",
                    total_errors
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
