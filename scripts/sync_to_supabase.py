#!/usr/bin/env python3
"""
sync_to_supabase.py - Upload benchmark results to Supabase for the Benchmark-web site.

Each run creates a new row in run_batches and uploads EVERY benchmark into it.
The batch is marked 'complete' only at the end, so the website (which reads the
latest complete batch) never sees a half-uploaded batch.

Usage:
    python scripts/sync_to_supabase.py            # upload
    python scripts/sync_to_supabase.py --dry-run  # parse files and print counts only

Needs in .env (repo root):
    SUPABASE_URL=https://xxxx.supabase.co
    SUPABASE_SECRET_KEY=sb_secret_...

Schema: Benchmark-web/supabase/migrations/001_init.sql
"""

import os
import sys
import json
import subprocess

import requests
from dotenv import load_dotenv

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# What to upload
# ---------------------------------------------------------------------------

WEB_SUITES = {
    "main": {"folder": "main_web_benchmark", "db_engine": "MySQL"},
    # PostgreSQL suite is still incomplete (BME has no Go/Java yet). Uncomment when done.
    # "pos": {"folder": "pos_web_benchmark", "db_engine": "PostgreSQL"},
}

WEB_TESTS = {
    "get_no_index": {"title_en": "GET without index", "title_th": "GET ไม่มี index"},
    "get_with_index": {"title_en": "GET with index", "title_th": "GET มี index"},
    "post": {"title_en": "POST (insert)", "title_th": "POST (เพิ่มข้อมูล)"},
}

# slug: (suite, folder under results/, title_en, title_th, description)
ALGO_BENCHMARKS = {
    "door": ("interactive", "interactive/door", "100 Doors", "100 Doors",
             "1 nested loop, 1,000,000 doors"),
    "prisoners": ("interactive", "interactive/Prison", "100 Prisoners", "100 Prisoners",
                  "2 nested loops, 1,000,000 prisoners"),
    "matrix": ("interactive", "interactive/Metrix", "Matrix multiplication", "คูณเมทริกซ์",
               "3 nested loops, 1000 x 1000"),
    "factorial": ("recursive", "recursive/factorial", "Factorial", "Factorial",
                  "Recursive factorial(100)"),
    "fibonacci": ("recursive", "recursive/fibonacci", "Fibonacci", "Fibonacci",
                  "Recursive fibonacci(50)"),
}

# hyperfine file name -> language label shown on the website
ALGO_LANGUAGES = {"go": "Go", "java": "Java", "node": "Node.js", "php": "PHP", "python": "Python"}

TIER_ORDER = {"poc": 1, "small": 2, "general": 3, "high": 4, "stress": 5}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def to_env(label):
    """'BME' / 'Bare Metal' -> 'bme', 'Docker' -> 'docker'."""
    return "docker" if "docker" in label.lower() else "bme"


def to_endpoint(path):
    """'/raw/2join' -> '2join', '/raw/post/3table' -> 'post-3table'."""
    return path.replace("/raw/", "", 1).replace("/", "-")


def git_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Read local result files
# ---------------------------------------------------------------------------

def collect_web():
    """Return (benchmarks, rows). rows carry 'benchmark_slug' until ids are known."""
    benchmarks = []
    rows = []
    order = 0

    for suite, info in WEB_SUITES.items():
        results_dir = os.path.join(REPO_ROOT, info["folder"], "results")

        for test, titles in WEB_TESTS.items():
            slug = f"web-{suite}-{test.replace('_', '-')}"
            found = False

            for env_file in ("bme", "dkr"):
                path = os.path.join(results_dir, f"{test}_{env_file}.json")
                raw_path = os.path.join(results_dir, "raw_results", f"{test}_{env_file}_raw.json")
                if not os.path.exists(path):
                    continue
                found = True
                data = load_json(path)
                raw = load_json(raw_path) if os.path.exists(raw_path) else {}

                for language, lang_data in data.items():
                    env = to_env(lang_data.get("Environment", env_file))

                    for tier, tier_data in lang_data["tiers"].items():
                        config = tier_data.get("config", {})

                        for ep_path, m in tier_data["endpoints"].items():
                            raw_ep = (raw.get(language, {}).get("tiers", {}).get(tier, {})
                                      .get("endpoints", {}).get(ep_path, {}))
                            rows.append({
                                "benchmark_slug": slug,
                                "language": language,
                                "environment": env,
                                "tier": tier,
                                "tier_order": TIER_ORDER[tier],
                                "tier_name": config.get("name"),
                                "tier_scenario": config.get("scenario"),
                                "threads": config.get("threads"),
                                "connections": config.get("connections"),
                                "duration": config.get("duration"),
                                "endpoint": to_endpoint(ep_path),
                                "endpoint_path": ep_path,
                                "rps_mean": m.get("requests_per_sec"),
                                "rps_sd": m.get("rps_stdev"),
                                "rps_ci95_margin": m.get("rps_ci95_margin"),
                                "rps_ci95_low": m.get("rps_ci95_low"),
                                "rps_ci95_high": m.get("rps_ci95_high"),
                                "lat_mean_ms": m.get("latency_mean_ms"),
                                "lat_sd_ms": m.get("latency_stdev_ms"),
                                "lat_ci95_margin": m.get("latency_ci95_margin"),
                                "lat_ci95_low": m.get("latency_ci95_low"),
                                "lat_ci95_high": m.get("latency_ci95_high"),
                                "lat_p50_ms": m.get("latency_p50_ms"),
                                "lat_p90_ms": m.get("latency_p90_ms"),
                                "lat_p95_ms": m.get("latency_p95_ms"),
                                "lat_p99_ms": m.get("latency_p99_ms"),
                                "lat_max_ms": m.get("latency_max_ms"),
                                "cpu_temp_avg_c": m.get("cpu_temp_avg_c"),
                                "cpu_temp_max_c": m.get("cpu_temp_max_c"),
                                "errors": m.get("errors"),
                                "runs_count": m.get("runs_count"),
                                "raw_runs": raw_ep.get("raw_runs"),
                            })

            if found:
                order += 1
                benchmarks.append({
                    "slug": slug,
                    "category": "web",
                    "suite": suite,
                    "title_en": titles["title_en"],
                    "title_th": titles["title_th"],
                    "description_en": None,
                    "description_th": None,
                    "db_engine": info["db_engine"],
                    "unit": "req/s",
                    "sort_order": order,
                })

    return benchmarks, rows


def collect_algorithm():
    """Read hyperfine files results/<folder>/json/<lang>.json.
    Inside each file: the command containing 'docker' is Docker, the other is Bare Metal."""
    benchmarks = []
    rows = []

    for order, (name, (suite, folder, title_en, title_th, desc)) in enumerate(ALGO_BENCHMARKS.items(), 1):
        slug = f"algo-{name}"
        benchmarks.append({
            "slug": slug,
            "category": "algorithm",
            "suite": suite,
            "title_en": title_en,
            "title_th": title_th,
            "description_en": desc,
            "description_th": desc,
            "db_engine": None,
            "unit": "s",
            "sort_order": 100 + order,
        })

        for file_name, language in ALGO_LANGUAGES.items():
            path = os.path.join(REPO_ROOT, "results", folder, "json", f"{file_name}.json")
            if not os.path.exists(path):
                print(f"  ! missing {path}")
                continue

            for r in load_json(path)["results"]:
                rows.append({
                    "benchmark_slug": slug,
                    "language": language,
                    "environment": to_env(r["command"]),
                    "command": r["command"],
                    "mean_s": r.get("mean"),
                    "sd_s": r.get("stddev"),
                    "median_s": r.get("median"),
                    "min_s": r.get("min"),
                    "max_s": r.get("max"),
                    "user_s": r.get("user"),
                    "system_s": r.get("system"),
                    "runs_count": len(r.get("times", [])),
                    "times": r.get("times"),
                })

    return benchmarks, rows


# ---------------------------------------------------------------------------
# Supabase REST (PostgREST)
# ---------------------------------------------------------------------------

class Supabase:
    def __init__(self, url, key):
        self.base = url.rstrip("/") + "/rest/v1"
        self.headers = {"apikey": key, "Content-Type": "application/json"}

    def request(self, method, table, params=None, body=None, prefer=None):
        headers = dict(self.headers)
        if prefer:
            headers["Prefer"] = prefer
        res = requests.request(method, f"{self.base}/{table}", params=params,
                               headers=headers, json=body, timeout=60)
        if res.status_code >= 400:
            raise RuntimeError(f"{method} {table} failed ({res.status_code}): {res.text}")
        return res.json() if res.text else None

    def insert_in_chunks(self, table, rows, size=200):
        for i in range(0, len(rows), size):
            self.request("POST", table, body=rows[i:i + size], prefer="return=minimal")
            print(f"  {table}: {min(i + size, len(rows))}/{len(rows)}")


def attach_ids(rows, batch_id, slug_to_id):
    out = []
    for row in rows:
        row = dict(row)
        row["benchmark_id"] = slug_to_id[row.pop("benchmark_slug")]
        row["batch_id"] = batch_id
        out.append(row)
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    dry_run = "--dry-run" in sys.argv

    print("[1/4] Reading result files...")
    web_benchmarks, web_rows = collect_web()
    algo_benchmarks, algo_rows = collect_algorithm()
    benchmarks = web_benchmarks + algo_benchmarks
    print(f"  benchmarks: {len(benchmarks)}  web rows: {len(web_rows)}  algorithm rows: {len(algo_rows)}")
    for b in benchmarks:
        n = sum(1 for r in web_rows + algo_rows if r["benchmark_slug"] == b["slug"])
        print(f"    {b['slug']:<28} {n} rows")

    if dry_run:
        print("Dry run: nothing uploaded.")
        return

    load_dotenv(os.path.join(REPO_ROOT, ".env"))
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SECRET_KEY")
    if not url or not key:
        sys.exit("Missing SUPABASE_URL or SUPABASE_SECRET_KEY in .env")
    db = Supabase(url, key)

    print("[2/4] Upserting benchmarks...")
    saved = db.request("POST", "benchmarks", params={"on_conflict": "slug"}, body=benchmarks,
                       prefer="resolution=merge-duplicates,return=representation")
    slug_to_id = {b["slug"]: b["id"] for b in saved}

    print("[3/4] Creating batch and uploading results...")
    batch = db.request("POST", "run_batches", body={"git_commit": git_commit()},
                       prefer="return=representation")[0]
    batch_id = batch["id"]
    try:
        db.insert_in_chunks("web_results", attach_ids(web_rows, batch_id, slug_to_id))
        db.insert_in_chunks("algo_results", attach_ids(algo_rows, batch_id, slug_to_id))
    except Exception:
        # Remove the half-uploaded batch (results cascade-delete with it)
        db.request("DELETE", "run_batches", params={"id": f"eq.{batch_id}"})
        raise

    print("[4/4] Marking batch complete...")
    db.request("PATCH", "run_batches", params={"id": f"eq.{batch_id}"}, body={"status": "complete"})
    print(f"Done. Batch #{batch_id} is now live on the website.")


if __name__ == "__main__":
    main()
