#!/usr/bin/env python3
import sys
import json
import os

def format_table(results_file):
    if not os.path.exists(results_file):
        print(f"Error: File '{results_file}' not found.")
        sys.exit(1)

    with open(results_file, "r") as f:
        data = json.load(f)

    print(f"\n# Benchmark Results Summary: {os.path.basename(results_file)}\n")

    # Detect structure (multi-tier vs single)
    first_lang = next(iter(data.values()))
    is_multi_tier = "tiers" in first_lang

    if is_multi_tier:
        tiers = list(first_lang["tiers"].keys())
        for tier in tiers:
            tier_name = first_lang["tiers"][tier]["config"]["name"]
            tier_cfg = first_lang["tiers"][tier]["config"]
            print(f"## Tier: {tier_name} (-t{tier_cfg['threads']} -c{tier_cfg['connections']} -d{tier_cfg['duration']})\n")

            endpoints = list(first_lang["tiers"][tier]["endpoints"].keys())
            for ep in endpoints:
                print(f"### Endpoint: `{ep}`")
                print("| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |")
                print("| :--- | :--- | :--- | :--- | :--- | :--- |")

                # Collect and sort by requests_per_sec descending
                rows = []
                for lang_name, lang_data in data.items():
                    res = lang_data["tiers"][tier]["endpoints"].get(ep, {})
                    if isinstance(res, dict) and "average" in res:
                        res = res["average"]
                    rps = res.get("requests_per_sec", 0.0)
                    lat_avg = res.get("latency_mean_ms", 0.0)
                    lat_max = res.get("latency_max_ms", 0.0)
                    errs = res.get("errors", 0)
                    rows.append((lang_name, rps, lat_avg, lat_max, errs))

                rows.sort(key=lambda x: x[1], reverse=True)

                for rank, (lang, rps, lat_avg, lat_max, errs) in enumerate(rows, start=1):
                    print(f"| #{rank} | **{lang}** | {rps:,.2f} | {lat_avg:.2f}ms | {lat_max:.2f}ms | {errs} |")
                print()
    else:
        endpoints = list(first_lang["endpoints"].keys())
        for ep in endpoints:
            print(f"### Endpoint: `{ep}`")
            print("| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |")
            print("| :--- | :--- | :--- | :--- | :--- | :--- |")

            rows = []
            for lang_name, lang_data in data.items():
                res = lang_data["endpoints"].get(ep, {})
                if isinstance(res, dict) and "average" in res:
                    res = res["average"]
                rps = res.get("requests_per_sec", 0.0)
                lat_avg = res.get("latency_mean_ms", 0.0)
                lat_max = res.get("latency_max_ms", 0.0)
                errs = res.get("errors", 0)
                rows.append((lang_name, rps, lat_avg, lat_max, errs))

            rows.sort(key=lambda x: x[1], reverse=True)

            for rank, (lang, rps, lat_avg, lat_max, errs) in enumerate(rows, start=1):
                print(f"| #{rank} | **{lang}** | {rps:,.2f} | {lat_avg:.2f}ms | {lat_max:.2f}ms | {errs} |")
            print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 compare_results.py <path_to_results.json>")
        sys.exit(1)
    format_table(sys.argv[1])
