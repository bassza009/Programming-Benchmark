#!/usr/bin/env python3
"""
setup_db.py - Automated PostgreSQL Database Setup & Data Ingestion Pipeline
Seeds:
  - factory:   10,000 records
  - product:  100,000 records
  - customer: 1,000,000 records
  - orders:   10,000,000 records
Total: 11,110,000 records
"""

import argparse
import os
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_SQL = os.path.join(SCRIPT_DIR, "schema.sql")
SEED_SQL = os.path.join(SCRIPT_DIR, "seed.sql")
INDEXES_SQL = os.path.join(SCRIPT_DIR, "add_indexes.sql")
DROP_INDEXES_SQL = os.path.join(SCRIPT_DIR, "drop_indexes.sql")

import shutil

def run_psql_file(filepath, host, port, user, password, dbname):
    t0 = time.time()
    if shutil.which("psql"):
        env = os.environ.copy()
        env["PGPASSWORD"] = password
        cmd = [
            "psql",
            "-h", host,
            "-p", str(port),
            "-U", user,
            "-d", dbname,
            "-v", "ON_ERROR_STOP=1",
            "-f", filepath
        ]
        res = subprocess.run(cmd, env=env, capture_output=True, text=True)
    else:
        with open(filepath, "r") as f:
            res = subprocess.run([
                "docker", "exec", "-i", "benchmark-postgres", "psql", "-U", user, "-d", dbname, "-v", "ON_ERROR_STOP=1"
            ], stdin=f, capture_output=True, text=True)
    elapsed = time.time() - t0
    if res.returncode != 0:
        print(f"[!] Error executing {os.path.basename(filepath)}:\n{res.stderr}", file=sys.stderr)
        return False, elapsed
    return True, elapsed

def run_psql_query(query, host, port, user, password, dbname):
    if shutil.which("psql"):
        env = os.environ.copy()
        env["PGPASSWORD"] = password
        cmd = [
            "psql",
            "-h", host,
            "-p", str(port),
            "-U", user,
            "-d", dbname,
            "-t", "-A",
            "-c", query
        ]
        res = subprocess.run(cmd, env=env, capture_output=True, text=True)
    else:
        res = subprocess.run([
            "docker", "exec", "-i", "benchmark-postgres", "psql", "-U", user, "-d", dbname, "-t", "-A", "-c", query
        ], capture_output=True, text=True)
    return res.stdout.strip(), res.returncode

def ensure_database(host, port, user, password, dbname):
    print(f"[*] Ensuring database '{dbname}' exists on {host}:{port}...")
    env = os.environ.copy()
    env["PGPASSWORD"] = password
    # Connect to default postgres DB to check/create
    check_query = f"SELECT 1 FROM pg_database WHERE datname='{dbname}';"
    out, code = run_psql_query(check_query, host, port, user, password, "postgres")
    if code != 0:
        print(f"[!] Warning: Could not connect to default postgres db. Assuming '{dbname}' already exists.")
        return True
    if out != "1":
        print(f"[*] Creating database '{dbname}'...")
        create_query = f"CREATE DATABASE {dbname};"
        _, create_code = run_psql_query(create_query, host, port, user, password, "postgres")
        if create_code != 0:
            print(f"[!] Failed to create database '{dbname}'", file=sys.stderr)
            return False
    print(f"[+] Database '{dbname}' is ready.")
    return True

def verify_counts(host, port, user, password, dbname):
    print("\n=======================================================")
    print(" VERIFYING TABLE ROW COUNTS IN POSTGRESQL")
    print("=======================================================")
    targets = [
        ("factory", 10000),
        ("product", 100000),
        ("customer", 1000000),
        ("orders", 10000000)
    ]
    all_ok = True
    for table, expected in targets:
        count_sql = f"SELECT COUNT(*) FROM {table};"
        val, code = run_psql_query(count_sql, host, port, user, password, dbname)
        if code == 0 and val.isdigit():
            cnt = int(val)
            status = "[OK]" if cnt >= expected else "[INCOMPLETE]"
            print(f" - {table:12s}: {cnt:>12,d} rows (Expected: {expected:>10,d}) {status}")
            if cnt < expected:
                all_ok = False
        else:
            print(f" - {table:12s}: Error checking count ({val})")
            all_ok = False
    print("=======================================================\n")
    return all_ok

def main():
    parser = argparse.ArgumentParser(description="PostgreSQL Database Ingestion & Setup Pipeline")
    parser.add_argument("--host", default=os.getenv("DB_HOST", "127.0.0.1"), help="PostgreSQL host")
    parser.add_argument("--port", type=int, default=int(os.getenv("DB_PORT", "5432")), help="PostgreSQL port")
    parser.add_argument("--user", default=os.getenv("DB_USER", "admin"), help="PostgreSQL user")
    parser.add_argument("--password", default=os.getenv("DB_PASS", "secret"), help="PostgreSQL password")
    parser.add_argument("--dbname", default=os.getenv("DB_NAME", "benchmark_db"), help="PostgreSQL database name")
    parser.add_argument("--step", choices=["all", "schema", "seed", "indexes", "drop_indexes", "verify"], default="all", help="Execution step")
    args = parser.parse_args()

    print("=======================================================")
    print(" PROGRAMMING BENCHMARK: POSTGRESQL DATABASE SETUP")
    print(f" Target: {args.host}:{args.port} | DB: {args.dbname} | User: {args.user}")
    print(f" Step:   {args.step.upper()}")
    print("=======================================================\n")

    if args.step in ["all", "schema"]:
        if not ensure_database(args.host, args.port, args.user, args.password, args.dbname):
            sys.exit(1)
        print(f"[*] Applying schema from: {os.path.basename(SCHEMA_SQL)}...")
        ok, elapsed = run_psql_file(SCHEMA_SQL, args.host, args.port, args.user, args.password, args.dbname)
        if not ok:
            sys.exit(1)
        print(f"[+] Schema created in {elapsed:.2f}s.")

    if args.step in ["all", "seed"]:
        print(f"[*] Seeding 11,110,000 records from: {os.path.basename(SEED_SQL)}...")
        print("    (This will seed: factory 10k, product 100k, customer 1M, orders 10M)")
        ok, elapsed = run_psql_file(SEED_SQL, args.host, args.port, args.user, args.password, args.dbname)
        if not ok:
            sys.exit(1)
        print(f"[+] Bulk seeding completed in {elapsed:.2f}s ({elapsed/60.0:.2f} min).")

    if args.step in ["all", "indexes"]:
        print(f"[*] Creating indexes on all 4 tables from: {os.path.basename(INDEXES_SQL)}...")
        ok, elapsed = run_psql_file(INDEXES_SQL, args.host, args.port, args.user, args.password, args.dbname)
        if not ok:
            sys.exit(1)
        print(f"[+] Indexes and VACUUM ANALYZE completed in {elapsed:.2f}s.")

    if args.step == "drop_indexes":
        print(f"[*] Dropping secondary indexes from: {os.path.basename(DROP_INDEXES_SQL)}...")
        ok, elapsed = run_psql_file(DROP_INDEXES_SQL, args.host, args.port, args.user, args.password, args.dbname)
        if not ok:
            sys.exit(1)
        print(f"[+] Secondary indexes dropped in {elapsed:.2f}s.")

    if args.step in ["all", "verify"]:
        verify_counts(args.host, args.port, args.user, args.password, args.dbname)

if __name__ == "__main__":
    main()
