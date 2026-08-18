#!/usr/bin/env python3
import sys
import json
import os

def format_table(results_file):
    if not os.path.exists(results_file):
        print(f"Error: File '{results_file}' not found.")
        sys.exit(1)

    with open(results_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"\n# Benchmark Results Summary: {os.path.basename(results_file)}\n")

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
                print("| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |")
                print("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

                rows = []
                for lang_name, lang_data in data.items():
                    res = lang_data["tiers"][tier]["endpoints"].get(ep, {})
                    if isinstance(res, dict) and "average" in res:
                        res = res["average"]

                    rps = res.get("requests_per_sec", 0.0)
                    rps_sd = res.get("rps_stdev", 0.0)
                    rps_ci_low = res.get("rps_ci95_low", rps)
                    rps_ci_high = res.get("rps_ci95_high", rps)

                    lat_mean = res.get("latency_mean_ms", 0.0)
                    lat_sd = res.get("latency_stdev_ms", 0.0)
                    lat_p50 = res.get("latency_p50_ms", lat_mean)
                    lat_p90 = res.get("latency_p90_ms", lat_mean)
                    lat_p95 = res.get("latency_p95_ms", lat_mean)
                    lat_p99 = res.get("latency_p99_ms", lat_mean)
                    lat_max = res.get("latency_max_ms", 0.0)
                    errs = res.get("errors", 0)

                    rows.append({
                        "lang": lang_name,
                        "rps": rps,
                        "rps_sd": rps_sd,
                        "rps_ci": f"[{rps_ci_low:,.1f} - {rps_ci_high:,.1f}]",
                        "lat_mean": lat_mean,
                        "lat_sd": lat_sd,
                        "p50": lat_p50,
                        "p90": lat_p90,
                        "p95": lat_p95,
                        "p99": lat_p99,
                        "max": lat_max,
                        "errs": errs
                    })

                rows.sort(key=lambda x: x["rps"], reverse=True)

                for rank, r in enumerate(rows, start=1):
                    rps_str = f"{r['rps']:,.2f}" if r['rps_sd'] == 0 else f"{r['rps']:,.2f} ± {r['rps_sd']:.2f}"
                    lat_str = f"{r['lat_mean']:.2f}ms" if r['lat_sd'] == 0 else f"{r['lat_mean']:.2f} ± {r['lat_sd']:.2f}ms"
                    print(f"| #{rank} | **{r['lang']}** | {rps_str} | {r['rps_ci']} | {lat_str} | {r['p50']:.2f}ms | {r['p90']:.2f}ms | {r['p95']:.2f}ms | {r['p99']:.2f}ms | {r['max']:.2f}ms | {r['errs']} |")
                print()
    else:
        endpoints = list(first_lang["endpoints"].keys())
        for ep in endpoints:
            print(f"### Endpoint: `{ep}`")
            print("| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |")
            print("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

            rows = []
            for lang_name, lang_data in data.items():
                res = lang_data["endpoints"].get(ep, {})
                if isinstance(res, dict) and "average" in res:
                    res = res["average"]

                rps = res.get("requests_per_sec", 0.0)
                rps_sd = res.get("rps_stdev", 0.0)
                rps_ci_low = res.get("rps_ci95_low", rps)
                rps_ci_high = res.get("rps_ci95_high", rps)

                lat_mean = res.get("latency_mean_ms", 0.0)
                lat_sd = res.get("latency_stdev_ms", 0.0)
                lat_p50 = res.get("latency_p50_ms", lat_mean)
                lat_p90 = res.get("latency_p90_ms", lat_mean)
                lat_p95 = res.get("latency_p95_ms", lat_mean)
                lat_p99 = res.get("latency_p99_ms", lat_mean)
                lat_max = res.get("latency_max_ms", 0.0)
                errs = res.get("errors", 0)

                rows.append({
                    "lang": lang_name,
                    "rps": rps,
                    "rps_sd": rps_sd,
                    "rps_ci": f"[{rps_ci_low:,.1f} - {rps_ci_high:,.1f}]",
                    "lat_mean": lat_mean,
                    "lat_sd": lat_sd,
                    "p50": lat_p50,
                    "p90": lat_p90,
                    "p95": lat_p95,
                    "p99": lat_p99,
                    "max": lat_max,
                    "errs": errs
                })

            rows.sort(key=lambda x: x["rps"], reverse=True)

            for rank, r in enumerate(rows, start=1):
                rps_str = f"{r['rps']:,.2f}" if r['rps_sd'] == 0 else f"{r['rps']:,.2f} ± {r['rps_sd']:.2f}"
                lat_str = f"{r['lat_mean']:.2f}ms" if r['lat_sd'] == 0 else f"{r['lat_mean']:.2f} ± {r['lat_sd']:.2f}ms"
                print(f"| #{rank} | **{r['lang']}** | {rps_str} | {r['rps_ci']} | {lat_str} | {r['p50']:.2f}ms | {r['p90']:.2f}ms | {r['p95']:.2f}ms | {r['p99']:.2f}ms | {r['max']:.2f}ms | {r['errs']} |")
            print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 compare_results.py <path_to_results.json>")
        sys.exit(1)
    format_table(sys.argv[1])
