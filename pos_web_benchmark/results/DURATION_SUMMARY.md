# Benchmark Execution Duration & Workload Summary

> **Generated at**: 2026-10-20 19:54:04

This document outlines the exact execution duration, iteration volume, and computational workload for both benchmark environments in this repository.

## 1. High-Level Comparison Matrix

| Benchmark Suite | Database Target | Dataset Size | Total Wrk Runs | Pure Load Time | Estimated Total Wall-Clock |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Main Web Benchmark** | MySQL 8.0 | 100,000 Records across 4 tables | 14,400 runs | 431.78 hrs (17.99 days) | 18d 15h 46m 40s (18.66 days) |
| **Pos Web Benchmark (Full 20-Run)** | PostgreSQL 16 | 11,110,000 Records across 4 tables | 3,152 / 12,000 runs (26.3%) | 97.33h recorded (Planned: 380.0h / 15.8 days) | 16d 9h 20m 0s (~16.4 days total) |

---

## 2. Main Web Benchmark (MySQL 100k) Breakdown

| Suite / Environment | Test Runs | Pure Load Time (Hours) | Estimated Wall-Clock Time | Status |
| :--- | :--- | :--- | :--- | :--- |
| `get_no_index_bme` | 2,400 | 63.89 hrs | 2d 18h 33m 20s | Completed |
| `get_no_index_dkr` | 2,400 | 76.00 hrs | 3d 6h 40m 0s | Completed |
| `get_with_index_bme` | 2,400 | 63.89 hrs | 2d 18h 33m 20s | Completed |
| `get_with_index_dkr` | 2,400 | 76.00 hrs | 3d 6h 40m 0s | Completed |
| `post_bme` | 2,400 | 76.00 hrs | 3d 6h 40m 0s | Completed |
| `post_dkr` | 2,400 | 76.00 hrs | 3d 6h 40m 0s | Completed |
| **Total Main Web** | **14,400** | **431.78 hrs** | **18d 15h 46m 40s** | **100% Finished** |


## 3. Pos Web Benchmark (PostgreSQL 11.11M) Breakdown

* **Pipeline Started**: `2026-10-05 01:21:16 `

* **Current Wall-Clock Elapsed**: `15d 18h 32m 48s`


| Planned Suite / Environment | Total Planned Runs | Pure Load Time (Hours) | Planned Wall-Clock Duration |
| :--- | :--- | :--- | :--- |
| `get_no_index_dkr` (GET No Index (Docker)) | 2,000 | 63.33 hrs | 2d 17h 33m 8s (~2.7 days) |
| `get_no_index_bme` (GET No Index (Bare Metal)) | 2,000 | 63.33 hrs | 2d 17h 33m 8s (~2.7 days) |
| `get_with_index_dkr` (GET With Index (Docker)) | 2,000 | 63.33 hrs | 2d 17h 33m 8s (~2.7 days) |
| `get_with_index_bme` (GET With Index (Bare Metal)) | 2,000 | 63.33 hrs | 2d 17h 33m 8s (~2.7 days) |
| `post_dkr` (POST Transactional (Docker)) | 2,000 | 63.33 hrs | 2d 17h 33m 8s (~2.7 days) |
| `post_bme` (POST Transactional (Bare Metal)) | 2,000 | 63.33 hrs | 2d 17h 33m 8s (~2.7 days) |
| **Total Pos Web Pipeline** | **12,000** | **380.00 hrs (15.83 days)** | **16d 9h 20m 0s (~16.39 days)** |


## 4. Workload Tier Durations per Run Cycle

| Load Tier | Threads | Connections | Duration | Warmup | Runs/EP | Wall-Clock per Endpoint |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `poc` | 2 | 20 | 30s | 3s + 1s | 20 runs | 680s (11.3 mins) |
| `small` | 4 | 100 | 60s | 3s + 1s | 20 runs | 1,280s (21.3 mins) |
| `general` | 8 | 500 | 60s | 3s + 1s | 20 runs | 1,280s (21.3 mins) |
| `high` | 8 | 2,000 | 120s | 3s + 1s | 20 runs | 2,480s (41.3 mins) |
| `stress` | 16 | 10,000 | 300s | 3s + 1s | 20 runs | 6,080s (101.3 mins) |
| **Total 5 Tiers** | - | - | **570s** | **20s** | **20 runs** | **11,800s (~3.28 hours)** |

