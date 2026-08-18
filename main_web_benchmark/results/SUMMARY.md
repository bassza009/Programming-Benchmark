# Web Framework Benchmark: Comprehensive Summary

Multi-language performance evaluation across **Docker Containerized** and **Bare Metal (Host)** environments.

## Executive Comparison: Docker vs Bare Metal (`/raw/1table` - Light Tier)

| Suite | Language | Docker (Req/s) | Bare Metal (Req/s) | Docker Latency | BME Latency | Overhead / Gain |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **get_no_index** | **Go** | 10,988.10 | 11,928.00 | 10.67ms | 9.30ms | +8.6% BME |
| **get_no_index** | **Java** | 9,231.73 | 11,958.11 | 12.24ms | 8.37ms | +29.5% BME |
| **get_no_index** | **Node.js** | 2,041.90 | 7,016.52 | 49.18ms | 16.30ms | +243.6% BME |
| **get_no_index** | **PHP** | 16,002.61 | 15,762.22 | 6.94ms | 7.27ms | -1.5% BME |
| **get_no_index** | **Python** | 2,515.54 | 1,624.44 | 40.03ms | 61.24ms | -35.4% BME |
| **get_with_index** | **Go** | 10,958.75 | 11,824.33 | 10.71ms | 9.34ms | +7.9% BME |
| **get_with_index** | **Java** | 10,133.17 | 11,760.51 | 10.80ms | 8.51ms | +16.1% BME |
| **get_with_index** | **Node.js** | 2,046.80 | 11,071.53 | 49.07ms | 9.10ms | +440.9% BME |
| **get_with_index** | **PHP** | 17,011.24 | 16,817.10 | 7.51ms | 6.27ms | -1.1% BME |
| **get_with_index** | **Python** | 2,557.69 | 1,908.37 | 41.69ms | 52.19ms | -25.4% BME |
| **post** | **Go** | 7,123.85 | - | 14.05ms | - | N/A |
| **post** | **Java** | 5,708.88 | - | 17.63ms | - | N/A |
| **post** | **Node.js** | 7,297.44 | - | 13.94ms | - | N/A |
| **post** | **PHP** | 4,506.78 | - | 23.91ms | - | N/A |
| **post** | **Python** | 7,045.07 | - | 14.41ms | - | N/A |

---

## Suite: `get_no_index` — Bare Metal (Host)

Error reading get_no_index_bme.json: Command '['python3', 'D:\\github\\Programming-Benchmark\\main_web_benchmark\\compare_results.py', 'D:\\github\\Programming-Benchmark\\main_web_benchmark\\results\\get_no_index_bme.json']' returned non-zero exit status 9009.

## Suite: `get_no_index` — Docker (Container)

Error reading get_no_index_dkr.json: Command '['python3', 'D:\\github\\Programming-Benchmark\\main_web_benchmark\\compare_results.py', 'D:\\github\\Programming-Benchmark\\main_web_benchmark\\results\\get_no_index_dkr.json']' returned non-zero exit status 9009.

## Suite: `get_with_index` — Bare Metal (Host)

Error reading get_with_index_bme.json: Command '['python3', 'D:\\github\\Programming-Benchmark\\main_web_benchmark\\compare_results.py', 'D:\\github\\Programming-Benchmark\\main_web_benchmark\\results\\get_with_index_bme.json']' returned non-zero exit status 9009.

## Suite: `get_with_index` — Docker (Container)

Error reading get_with_index_dkr.json: Command '['python3', 'D:\\github\\Programming-Benchmark\\main_web_benchmark\\compare_results.py', 'D:\\github\\Programming-Benchmark\\main_web_benchmark\\results\\get_with_index_dkr.json']' returned non-zero exit status 9009.

## Suite: `post` — Docker (Container)

Error reading post_dkr.json: Command '['python3', 'D:\\github\\Programming-Benchmark\\main_web_benchmark\\compare_results.py', 'D:\\github\\Programming-Benchmark\\main_web_benchmark\\results\\post_dkr.json']' returned non-zero exit status 9009.
