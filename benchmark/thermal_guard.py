#!/usr/bin/env python3
"""
thermal_guard.py
Hardware protection and thermal monitoring module for Programming-Benchmark.
Monitors CPU package/core temperatures via coretemp hwmon and enforces
cooldown pauses to protect motherboard VRMs, MOSFETs, and power delivery capacitors.
"""

import os
import glob
import time

MAX_SAFE_TEMP = 75.0        # Degrees Celsius (Pauses execution if exceeded)
TARGET_COOLDOWN_TEMP = 58.0 # Degrees Celsius (Resumes when cooled down to this)

def get_cpu_temp():
    """Returns max temperature from coretemp (Package / Cores) in Celsius."""
    max_temp = 0.0
    for hwmon in glob.glob("/sys/class/hwmon/hwmon*"):
        name_path = os.path.join(hwmon, "name")
        if os.path.exists(name_path):
            try:
                with open(name_path, "r") as f:
                    name = f.read().strip()
            except Exception:
                continue
            if name == "coretemp":
                for tfile in glob.glob(os.path.join(hwmon, "temp*_input")):
                    try:
                        with open(tfile, "r") as tf:
                            val = float(tf.read().strip()) / 1000.0
                            if val > max_temp:
                                max_temp = val
                    except Exception:
                        pass
    if max_temp == 0.0:
        for tz in glob.glob("/sys/class/thermal/thermal_zone*/temp"):
            try:
                with open(tz, "r") as f:
                    val = float(f.read().strip()) / 1000.0
                    if val > max_temp:
                        max_temp = val
            except Exception:
                pass
    return max_temp

def check_and_cool(tier_key=None, max_allowed=MAX_SAFE_TEMP, target_cooldown=TARGET_COOLDOWN_TEMP):
    """
    Checks CPU temperature and pauses if CPU or VRMs are running too hot.
    """
    cur_temp = get_cpu_temp()
    if cur_temp >= max_allowed:
        print(f"\n  [!] [THERMAL GUARD] CPU Temp = {cur_temp:.1f}°C (Exceeds {max_allowed:.1f}°C safe limit!)", flush=True)
        print(f"      Pausing benchmark to protect hardware & capacitors until CPU <= {target_cooldown:.1f}°C...", flush=True)
        while cur_temp > target_cooldown:
            time.sleep(5)
            cur_temp = get_cpu_temp()
            print(f"      Cooling down... Current CPU Temp: {cur_temp:.1f}°C (Target: <= {target_cooldown:.1f}°C)", flush=True)
        print(f"  [+] [THERMAL GUARD] Cooled down to {cur_temp:.1f}°C. Resuming benchmark.\n", flush=True)
    return cur_temp

def get_cooldown_sleep(tier_key):
    """
    Dynamic cooldown sleep between runs to prevent VRM capacitor thermal exhaustion.
    """
    if tier_key == "stress":
        return 15.0  # 15s pause after 300s of 16-thread/10k-conn stress
    elif tier_key == "high":
        return 8.0   # 8s pause after 120s of high load
    elif tier_key == "general":
        return 4.0
    return 2.0

if __name__ == "__main__":
    t = get_cpu_temp()
    print(f"Current Max CPU Temp: {t:.1f}°C")
    print(f"Thermal limits configured: Max Allowed = {MAX_SAFE_TEMP}°C | Target Cooldown = {TARGET_COOLDOWN_TEMP}°C")
