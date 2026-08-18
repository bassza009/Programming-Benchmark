# Project Antigravity Agent Guidelines & Rules

## Mandatory Rules for Benchmark Data & Reporting

Whenever you run benchmarks, modify benchmark results, or update dataset configurations in this repository, you **MUST** follow these 3 core requirements:

### 1. Synchronize README and Push to GitHub Every Time Data Changes
* Whenever benchmark output data (`.json`, `.csv`, `SUMMARY.md`) changes, immediately update both [README.md](file:///D:/github/Programming-Benchmark/README.md) and [README_TH.md](file:///D:/github/Programming-Benchmark/README_TH.md) to reflect the new figures.
* Immediately commit all changes and push upstream to GitHub:
  ```bash
  git add .
  git commit -m "benchmarks: update results, sync report docx, and mirror READMEs"
  git push origin main
  ```

### 2. Update the Research Report (.docx and .md)
* Keep the academic research report [Programming_Benchmark_Report.md](file:///D:/github/Programming-Benchmark/Programming_Benchmark_Report.md) and [Programming_Benchmark_Report.docx](file:///D:/github/Programming-Benchmark/Programming_Benchmark_Report.docx) synchronized with the latest experimental findings.
* Run `python scripts/sync_benchmark_report.py --docx` to recompile the Word Document (`.docx`).

### 3. Follow the Standard Gathering Method for the Report
* **Raw Metric Collection**: Extract metrics from multi-run tests (`wrk` output with `--runs 3` or `--runs 5`).
* **Statistical Aggregation**: Run `python main_web_benchmark/results/generate_summary.py` to calculate statistical means ($\bar{T}$ Requests/sec, $\bar{L}$ Latency ms, Total Socket Errors).
* **Factorial Comparative Synthesis**:
  - Containerization Overhead ($\text{Gain}_{\text{BME}} = \frac{\bar{T}_{\text{BME}} - \bar{T}_{\text{DKR}}}{\bar{T}_{\text{DKR}}} \times 100\%$)
  - Indexing Speedup Ratio ($\frac{\bar{T}_{\text{WithIndex}}}{\bar{T}_{\text{NoIndex}}}$)
  - Concurrency Saturation & Breakdown Thresholds across tiers (POC $\rightarrow$ Stress).
* Format aggregated matrices into academic comparison tables for the report and READMEs.
