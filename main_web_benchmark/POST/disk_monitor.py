#!/usr/bin/env python3
import datetime
import os
import shutil
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "disk_check.txt")

def get_disk_info(path="/"):
    total, used, free = shutil.disk_usage(path)
    pct = (used / total) * 100
    return {
        "total_gb": round(total / (1024 ** 3), 2),
        "used_gb": round(used / (1024 ** 3), 2),
        "free_gb": round(free / (1024 ** 3), 2),
        "pct": round(pct, 1)
    }

def get_mem_info():
    try:
        with open("/proc/meminfo") as f:
            meminfo = dict(line.split(":") for line in f.read().splitlines() if ":" in line)
        total = int(meminfo["MemTotal"].split()[0])
        avail = int(meminfo["MemAvailable"].split()[0])
        used = total - avail
        pct = (used / total) * 100
        return {
            "total_gb": round(total / (1024 ** 2), 2),
            "used_gb": round(used / (1024 ** 2), 2),
            "avail_gb": round(avail / (1024 ** 2), 2),
            "pct": round(pct, 1)
        }
    except Exception:
        return {"total_gb": 0, "used_gb": 0, "avail_gb": 0, "pct": 0}

def emergency_cleanup():
    actions = []
    # 1. Drop OS caches
    try:
        subprocess.run(["sudo", "sh", "-c", "echo 3 > /proc/sys/vm/drop_caches"], capture_output=True, timeout=10)
        actions.append("drop_caches")
    except Exception:
        pass

    # 2. Prune stopped docker containers and dangling volumes
    try:
        subprocess.run(["docker", "container", "prune", "-f"], capture_output=True, timeout=10)
        subprocess.run(["docker", "volume", "prune", "-f"], capture_output=True, timeout=10)
        actions.append("docker_prune")
    except Exception:
        pass

    # 3. Clean journald logs
    try:
        subprocess.run(["sudo", "journalctl", "--vacuum-size=100M"], capture_output=True, timeout=10)
        actions.append("vacuum_journal")
    except Exception:
        pass

    # 4. Clean tmp
    try:
        subprocess.run(["sudo", "rm", "-rf", "/tmp/*", "/var/tmp/*"], capture_output=True, timeout=10)
        actions.append("clean_tmp")
    except Exception:
        pass

    return actions

def check_and_log(threshold_disk_pct=80, threshold_mem_pct=85):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    disk = get_disk_info()
    mem = get_mem_info()

    status = "OK"
    cleaned = []

    if disk["pct"] >= threshold_disk_pct or mem["pct"] >= threshold_mem_pct:
        status = f"WARNING_HIGH_USAGE (Disk: {disk['pct']}%, RAM: {mem['pct']}%)"
        cleaned = emergency_cleanup()
        disk = get_disk_info()
        mem = get_mem_info()

    log_entry = (
        f"[{now}] DISK: {disk['used_gb']}G/{disk['total_gb']}G ({disk['pct']}%, free {disk['free_gb']}G) | "
        f"RAM: {mem['used_gb']}G/{mem['total_gb']}G ({mem['pct']}%, avail {mem['avail_gb']}G) | "
        f"STATUS: {status}"
    )
    if cleaned:
        log_entry += f" | ACTIONS: {', '.join(cleaned)}"

    print(log_entry, flush=True)

    # Maintain recent entries in disk_check.txt (keep last 500 lines)
    existing_lines = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                existing_lines = f.readlines()
        except Exception:
            existing_lines = []

    existing_lines.append(log_entry + "\n")
    if len(existing_lines) > 500:
        existing_lines = existing_lines[-500:]

    with open(LOG_FILE, "w") as f:
        f.writelines(existing_lines)

    return disk, mem

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Disk and Memory Watcher")
    parser.add_argument("--interval", type=int, default=60, help="Check interval in seconds (default: 60s)")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--threshold-disk", type=int, default=80, help="Disk threshold percentage to trigger cleanup (default: 80)")
    parser.add_argument("--threshold-mem", type=int, default=85, help="Memory threshold percentage to trigger cleanup (default: 85)")
    args = parser.parse_args()

    if args.once:
        check_and_log(args.threshold_disk, args.threshold_mem)
        return

    print(f"[DISK MONITOR] Starting daemon (interval: {args.interval}s, disk threshold: {args.threshold_disk}%, log: {LOG_FILE})", flush=True)
    while True:
        try:
            check_and_log(args.threshold_disk, args.threshold_mem)
        except Exception as e:
            print(f"[DISK MONITOR ERROR] {e}", flush=True)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
