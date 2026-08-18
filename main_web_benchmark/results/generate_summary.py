#!/usr/bin/env python3
import os
import glob
import json
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COMPARE_SCRIPT = os.path.join(os.path.dirname(SCRIPT_DIR), "compare_results.py")
SUMMARY_FILE = os.path.join(SCRIPT_DIR, "SUMMARY.md")

def generate_summary():
    json_files = sorted(glob.glob(os.path.join(SCRIPT_DIR, "*.json")))
    if not json_files:
        print("No result JSON files found in", SCRIPT_DIR)
        return

    output = []
    output.append("# 📊 Web Benchmark Comprehensive Results Summary\n")
    output.append(f"Generated from {len(json_files)} test suite result datasets.\n")

    for fpath in json_files:
        fname = os.path.basename(fpath)
        title = fname.replace("_dkr.json", " (Docker)").replace("_bme.json", " (Bare Metal)").replace(".json", "")
        output.append(f"## 📁 Suite: `{title}`\n")
        
        try:
            res = subprocess.run(["python3", COMPARE_SCRIPT, fpath], capture_output=True, text=True, check=True)
            output.append(res.stdout.strip())
            output.append("\n---\n")
        except Exception as e:
            output.append(f"Error reading {fname}: {e}\n")

    summary_text = "\n".join(output)
    with open(SUMMARY_FILE, "w") as f:
        f.write(summary_text)

    print(f"Summary written to {SUMMARY_FILE}")

if __name__ == "__main__":
    generate_summary()
