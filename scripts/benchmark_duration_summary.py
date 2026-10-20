#!/usr/bin/env python3
"""
benchmark_duration_summary.py
Calculates and generates a comprehensive execution duration and workload breakdown
for both main_web_benchmark (MySQL) and pos_web_benchmark (PostgreSQL).
"""

import os
import sys
import glob
import json
import time
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_WEB_DIR = os.path.join(ROOT_DIR, "main_web_benchmark")
POS_WEB_DIR = os.path.join(ROOT_DIR, "pos_web_benchmark")

# Hardcoded or recorded runner start time for pos_web_benchmark
POS_RUNNER_START_TIME = datetime(2026, 10, 5, 1, 21, 16)

def format_duration(seconds):
    td = timedelta(seconds=int(seconds))
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, sec = divmod(remainder, 60)
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0 or days > 0:
        parts.append(f"{hours}h")
    if minutes > 0 or hours > 0 or days > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{sec}s")
    return " ".join(parts)

def analyze_benchmark_dir(results_dir, name, db_type, scale_desc):
    files = sorted(glob.glob(os.path.join(results_dir, "*.json")))
    files = [f for f in files if not f.endswith("_raw.json") and not os.path.basename(f).startswith("execution_")]
    
    suite_stats = {}
    framework_stats = {}
    tier_stats = {}
    grand_runs = 0
    grand_pure_sec = 0

    for fpath in files:
        suite_name = os.path.basename(fpath).replace(".json", "")
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue

        s_runs = 0
        s_pure_sec = 0

        for lang, ldata in data.items():
            if not isinstance(ldata, dict) or "tiers" not in ldata:
                continue
            
            if lang not in framework_stats:
                framework_stats[lang] = {"runs": 0, "pure_sec": 0}

            for tk, tdata in ldata["tiers"].items():
                dur_str = tdata.get("config", {}).get("duration", "0s")
                dur = int(dur_str.rstrip("s"))

                if tk not in tier_stats:
                    tier_stats[tk] = {"runs": 0, "pure_sec": 0, "dur_sec": dur}

                for ep, edata in tdata.get("endpoints", {}).items():
                    rc = edata.get("runs_count", 0)
                    s_runs += rc
                    sec = rc * dur
                    s_pure_sec += sec
                    framework_stats[lang]["runs"] += rc
                    framework_stats[lang]["pure_sec"] += sec
                    tier_stats[tk]["runs"] += rc
                    tier_stats[tk]["pure_sec"] += sec

        suite_stats[suite_name] = {
            "runs": s_runs,
            "pure_sec": s_pure_sec,
            "est_warmup_sleep_sec": s_runs * 4  # 3s warmup + 1s cooldown
        }
        grand_runs += s_runs
        grand_pure_sec += s_pure_sec

    # Overhead calculation: warmup (3s) + sleep (1s) per run + container spinup (~15s)
    total_warmup_sleep_sec = grand_runs * 4
    total_est_wallclock_sec = grand_pure_sec + total_warmup_sleep_sec

    return {
        "name": name,
        "db_type": db_type,
        "scale": scale_desc,
        "grand_runs": grand_runs,
        "grand_pure_sec": grand_pure_sec,
        "total_est_wallclock_sec": total_est_wallclock_sec,
        "suite_stats": suite_stats,
        "framework_stats": framework_stats,
        "tier_stats": tier_stats
    }

def generate_report():
    main_res = analyze_benchmark_dir(
        os.path.join(MAIN_WEB_DIR, "results"),
        "Main Web Benchmark",
        "MySQL 8.0",
        "100,000 Records across 4 tables"
    )

    pos_res = analyze_benchmark_dir(
        os.path.join(POS_WEB_DIR, "results"),
        "Pos Web Benchmark (PostgreSQL Enterprise)",
        "PostgreSQL 16",
        "11,110,000 Records across 4 tables"
    )

    md = []
    md.append("# Benchmark Execution Duration & Workload Summary\n")
    md.append(f"> **Generated at**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md.append("This document outlines the exact execution duration, iteration volume, and computational workload for both benchmark environments in this repository.\n")

    md.append("## 1. High-Level Comparison Matrix\n")
    md.append("| Benchmark Suite | Database Target | Dataset Size | Total Wrk Runs | Pure Load Time | Estimated Total Wall-Clock |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
    md.append(f"| **Main Web Benchmark** | {main_res['db_type']} | {main_res['scale']} | {main_res['grand_runs']:,} runs | {main_res['grand_pure_sec']/3600:.2f} hrs ({main_res['grand_pure_sec']/86400:.2f} days) | {format_duration(main_res['total_est_wallclock_sec'])} ({main_res['total_est_wallclock_sec']/86400:.2f} days) |")
    
    # Check if pos_res is still in progress or completed
    pos_planned_runs = 12000
    pos_planned_pure_sec = 380 * 3600  # 380 hours pure
    pos_planned_wall_sec = pos_planned_pure_sec + (pos_planned_runs * 4)

    pos_status_str = f"{pos_res['grand_runs']:,} / {pos_planned_runs:,} runs ({pos_res['grand_runs']/pos_planned_runs*100:.1f}%)" if pos_res['grand_runs'] < pos_planned_runs else f"{pos_res['grand_runs']:,} runs (Completed)"
    pos_pure_str = f"{pos_res['grand_pure_sec']/3600:.2f}h recorded (Planned: {pos_planned_pure_sec/3600:.1f}h / 15.8 days)"
    pos_wall_str = f"{format_duration(pos_planned_wall_sec)} (~{pos_planned_wall_sec/86400:.1f} days total)"

    md.append(f"| **Pos Web Benchmark (Full 20-Run)** | {pos_res['db_type']} | {pos_res['scale']} | {pos_status_str} | {pos_pure_str} | {pos_wall_str} |")
    md.append("\n---\n")

    # 2. Main Web Breakdown
    md.append("## 2. Main Web Benchmark (MySQL 100k) Breakdown\n")
    md.append("| Suite / Environment | Test Runs | Pure Load Time (Hours) | Estimated Wall-Clock Time | Status |")
    md.append("| :--- | :--- | :--- | :--- | :--- |")
    for sname, sinfo in main_res["suite_stats"].items():
        total_suite_sec = sinfo["pure_sec"] + sinfo["est_warmup_sleep_sec"]
        md.append(f"| `{sname}` | {sinfo['runs']:,} | {sinfo['pure_sec']/3600:.2f} hrs | {format_duration(total_suite_sec)} | Completed |")
    md.append(f"| **Total Main Web** | **{main_res['grand_runs']:,}** | **{main_res['grand_pure_sec']/3600:.2f} hrs** | **{format_duration(main_res['total_est_wallclock_sec'])}** | **100% Finished** |")
    md.append("\n")

    # 3. Pos Web Breakdown
    md.append("## 3. Pos Web Benchmark (PostgreSQL 11.11M) Breakdown\n")
    md.append(f"* **Pipeline Started**: `{POS_RUNNER_START_TIME.strftime('%Y-%m-%d %H:%M:%S %Z')}`\n")
    elapsed_now = (datetime.now() - POS_RUNNER_START_TIME).total_seconds()
    md.append(f"* **Current Wall-Clock Elapsed**: `{format_duration(elapsed_now)}`\n")
    md.append("\n| Planned Suite / Environment | Total Planned Runs | Pure Load Time (Hours) | Planned Wall-Clock Duration |")
    md.append("| :--- | :--- | :--- | :--- |")
    pos_suites = [
        ("get_no_index_dkr", "GET No Index (Docker)", 2000, 63.33),
        ("get_no_index_bme", "GET No Index (Bare Metal)", 2000, 63.33),
        ("get_with_index_dkr", "GET With Index (Docker)", 2000, 63.33),
        ("get_with_index_bme", "GET With Index (Bare Metal)", 2000, 63.33),
        ("post_dkr", "POST Transactional (Docker)", 2000, 63.33),
        ("post_bme", "POST Transactional (Bare Metal)", 2000, 63.33),
    ]
    for skey, slabel, sruns, shours in pos_suites:
        sec = shours * 3600
        wall = sec + (sruns * 4)
        md.append(f"| `{skey}` ({slabel}) | {sruns:,} | {shours:.2f} hrs | {format_duration(wall)} (~{wall/86400:.1f} days) |")
    md.append(f"| **Total Pos Web Pipeline** | **12,000** | **380.00 hrs (15.83 days)** | **{format_duration(pos_planned_wall_sec)} (~16.39 days)** |")
    md.append("\n")

    # 4. Concurrency Tier Load Specification
    md.append("## 4. Workload Tier Durations per Run Cycle\n")
    md.append("| Load Tier | Threads | Connections | Duration | Warmup | Runs/EP | Wall-Clock per Endpoint |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    md.append("| `poc` | 2 | 20 | 30s | 3s + 1s | 20 runs | 680s (11.3 mins) |")
    md.append("| `small` | 4 | 100 | 60s | 3s + 1s | 20 runs | 1,280s (21.3 mins) |")
    md.append("| `general` | 8 | 500 | 60s | 3s + 1s | 20 runs | 1,280s (21.3 mins) |")
    md.append("| `high` | 8 | 2,000 | 120s | 3s + 1s | 20 runs | 2,480s (41.3 mins) |")
    md.append("| `stress` | 16 | 10,000 | 300s | 3s + 1s | 20 runs | 6,080s (101.3 mins) |")
    md.append("| **Total 5 Tiers** | - | - | **570s** | **20s** | **20 runs** | **11,800s (~3.28 hours)** |")
    md.append("\n")

    return "\n".join(md)

if __name__ == "__main__":
    report_content = generate_report()
    print(report_content)
    
    # Save to DURATION_SUMMARY.md in pos_web_benchmark/results/
    out_file = os.path.join(POS_WEB_DIR, "results", "DURATION_SUMMARY.md")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"\n[+] Duration summary saved to: {out_file}")
