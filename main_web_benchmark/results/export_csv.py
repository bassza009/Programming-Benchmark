#!/usr/bin/env python3
import os
import glob
import json
import csv

RESULTS_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(RESULTS_DIR, "SUMMARY.csv")

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
        # Identify suite & environment
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
                t_cfg = first_lang["tiers"][tier]["config"]
                tier_name = t_cfg.get("name", tier)
                threads = t_cfg.get("threads", "")
                conns = t_cfg.get("connections", "")
                dur = t_cfg.get("duration", "")
                endpoints = list(first_lang["tiers"][tier]["endpoints"].keys())

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
            endpoints = list(first_lang["endpoints"].keys())
            for ep in endpoints:
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

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"Successfully generated {CSV_FILE} with {len(rows)} data rows.")

if __name__ == "__main__":
    export_to_csv()
