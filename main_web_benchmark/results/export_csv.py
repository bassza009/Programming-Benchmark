#!/usr/bin/env python3
import os
import glob
import json
import csv

RESULTS_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(RESULTS_DIR, "SUMMARY.csv")

def clean_ep_name(ep):
    # Normalize endpoints like /raw/1table, /raw/post/1table to clean column names
    ep = ep.replace("/raw/post/", "").replace("/raw/", "")
    return ep

def export_to_csv():
    json_files = sorted(glob.glob(os.path.join(RESULTS_DIR, "*.json")))
    if not json_files:
        print("No JSON files found in", RESULTS_DIR)
        return

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
            tiers = list(first_lang["tiers"].keys())
            for tier in tiers:
                tier_name = first_lang["tiers"][tier]["config"].get("name", tier)

                for lang_name in sorted(data.keys()):
                    lang_data = data[lang_name]
                    endpoints = lang_data["tiers"][tier]["endpoints"]
                    
                    # Map endpoints: 1table, 2join/2table, 3join/3table, 4join/4table
                    ep_map = {}
                    total_errors = 0
                    for ep_key, ep_res in endpoints.items():
                        cleaned = clean_ep_name(ep_key)
                        rps = ep_res.get("requests_per_sec", 0.0)
                        lat = ep_res.get("latency_mean_ms", 0.0)
                        errs = ep_res.get("errors", 0)
                        total_errors += errs
                        ep_map[cleaned] = (rps, lat)

                    # Find keys for 1, 2, 3, 4
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

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Successfully generated {CSV_FILE} with {len(rows)} data rows.")

if __name__ == "__main__":
    export_to_csv()
