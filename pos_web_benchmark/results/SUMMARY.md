# Web Framework Benchmark: Comprehensive Summary

Multi-language performance evaluation across **Docker Containerized** and **Bare Metal (Host)** environments.

Statistical metrics include Arithmetic Mean ($\bar{X}$), Standard Deviation ($\sigma$), 95% Confidence Interval (95% CI), and Latency Percentiles ($p_{50}, p_{90}, p_{95}, p_{99}$).

## Executive Comparison: Docker vs Bare Metal (`/raw/1table` - Light Tier)

| Suite | Language | Docker (Req/s ± SD) | Bare Metal (Req/s ± SD) | Docker p50 / p95 (ms) | BME p50 / p95 (ms) | Overhead / Gain |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **get_no_index** | **Go** | 4,780.33 | - | 4.49ms / 5.78ms | - | N/A |
| **get_no_index** | **Java** | 9,975.97 | - | 1.95ms / 2.46ms | - | N/A |
| **get_no_index** | **Node.js** | 9,736.03 | - | 2.08ms / 2.58ms | - | N/A |
| **get_no_index** | **PHP** | 22,133.54 | - | 0.90ms / 1.11ms | - | N/A |
| **get_no_index** | **Python** | 1,533.77 | - | 12.94ms / 16.60ms | - | N/A |

---

| **get_with_index** | **Go** | 4,783.00 | - | 4.49ms / 5.80ms | - | N/A |
| **get_with_index** | **Java** | 9,782.76 | - | 1.99ms / 2.50ms | - | N/A |
| **get_with_index** | **Node.js** | 9,837.01 | - | 2.06ms / 2.55ms | - | N/A |
| **get_with_index** | **PHP** | 22,522.87 | - | 0.89ms / 1.10ms | - | N/A |
| **get_with_index** | **Python** | 1,543.17 | - | 12.89ms / 16.40ms | - | N/A |

---

| **post** | **Go** | 31,507.46 | - | 0.58ms / 1.02ms | - | N/A |
| **post** | **Java** | 26,542.69 | - | 0.71ms / 1.00ms | - | N/A |
| **post** | **Node.js** | 28,300.84 | - | 0.67ms / 0.91ms | - | N/A |
| **post** | **PHP** | 27,518.46 | - | 0.70ms / 0.96ms | - | N/A |
| **post** | **Python** | 8,822.72 | - | 2.21ms / 2.98ms | - | N/A |

---

## Suite: `get_no_index` — Docker (Container)

# Benchmark Results Summary: get_no_index_dkr.json

## Tier: POC / Small internal system (-t2 -c20 -d30s)

### Endpoint: `/raw/1table`
| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **PHP** | 22,133.54 | [22,133.5 - 22,133.5] | 0.91 ± 0.75ms | 0.90ms | 1.05ms | 1.11ms | 1.26ms | 54.95ms | 0 |
| #2 | **Java** | 9,975.97 | [9,976.0 - 9,976.0] | 2.05 ± 1.13ms | 1.95ms | 2.32ms | 2.46ms | 5.47ms | 29.57ms | 0 |
| #3 | **Node.js** | 9,736.03 | [9,736.0 - 9,736.0] | 2.15 ± 2.29ms | 2.08ms | 2.43ms | 2.58ms | 3.08ms | 90.41ms | 0 |
| #4 | **Go** | 4,780.33 | [4,780.3 - 4,780.3] | 4.16 ± 1.26ms | 4.49ms | 5.51ms | 5.78ms | 6.79ms | 13.60ms | 0 |
| #5 | **Python** | 1,533.77 | [1,533.8 - 1,533.8] | 13.03 ± 2.47ms | 12.94ms | 15.84ms | 16.60ms | 20.25ms | 47.16ms | 0 |

### Endpoint: `/raw/2join`
| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **Java** | 466.95 | [466.9 - 466.9] | 42.79 ± 14.68ms | 34.08ms | 64.59ms | 67.46ms | 73.22ms | 100.27ms | 0 |
| #2 | **Go** | 436.17 | [436.2 - 436.2] | 45.81 ± 18.11ms | 37.46ms | 69.74ms | 81.06ms | 89.08ms | 101.58ms | 0 |
| #3 | **PHP** | 399.17 | [399.2 - 399.2] | 50.59 ± 21.79ms | 56.30ms | 74.45ms | 82.17ms | 119.40ms | 249.48ms | 0 |
| #4 | **Node.js** | 378.83 | [378.8 - 378.8] | 52.72 ± 20.82ms | 61.10ms | 79.23ms | 85.19ms | 91.50ms | 159.57ms | 0 |
| #5 | **Python** | 362.53 | [362.5 - 362.5] | 55.09 ± 18.17ms | 57.59ms | 79.15ms | 84.45ms | 94.72ms | 138.75ms | 0 |

### Endpoint: `/raw/3join`
| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **PHP** | 399.95 | [399.9 - 399.9] | 50.18 ± 18.57ms | 49.02ms | 70.64ms | 74.89ms | 101.93ms | 210.23ms | 0 |
| #2 | **Java** | 390.99 | [391.0 - 391.0] | 51.10 ± 18.37ms | 40.11ms | 76.28ms | 81.23ms | 93.77ms | 114.02ms | 0 |
| #3 | **Python** | 385.80 | [385.8 - 385.8] | 51.78 ± 18.14ms | 43.67ms | 78.51ms | 88.99ms | 100.12ms | 119.37ms | 0 |
| #4 | **Go** | 379.47 | [379.5 - 379.5] | 52.64 ± 21.23ms | 42.68ms | 79.84ms | 92.29ms | 101.32ms | 112.88ms | 0 |
| #5 | **Node.js** | 338.15 | [338.1 - 338.1] | 59.09 ± 23.66ms | 68.23ms | 90.88ms | 97.39ms | 103.55ms | 174.56ms | 0 |

### Endpoint: `/raw/4join`
| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **PHP** | 383.28 | [383.3 - 383.3] | 52.24 ± 19.16ms | 41.51ms | 74.53ms | 78.61ms | 100.51ms | 216.32ms | 0 |
| #2 | **Java** | 380.42 | [380.4 - 380.4] | 52.49 ± 18.51ms | 41.64ms | 77.89ms | 83.47ms | 95.63ms | 116.64ms | 0 |
| #3 | **Go** | 353.23 | [353.2 - 353.2] | 56.54 ± 22.46ms | 52.34ms | 90.04ms | 98.16ms | 102.69ms | 114.33ms | 0 |
| #4 | **Node.js** | 344.38 | [344.4 - 344.4] | 58.00 ± 23.22ms | 64.38ms | 83.47ms | 95.88ms | 105.78ms | 194.17ms | 0 |
| #5 | **Python** | 343.40 | [343.4 - 343.4] | 58.18 ± 19.81ms | 53.82ms | 87.43ms | 93.50ms | 103.22ms | 130.19ms | 0 |

---

## Suite: `get_with_index` — Docker (Container)

# Benchmark Results Summary: get_with_index_dkr.json

## Tier: POC / Small internal system (-t2 -c20 -d30s)

### Endpoint: `/raw/1table`
| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **PHP** | 22,522.87 | [22,522.9 - 22,522.9] | 0.90 ± 0.72ms | 0.89ms | 1.04ms | 1.10ms | 1.25ms | 55.04ms | 0 |
| #2 | **Node.js** | 9,837.01 | [9,837.0 - 9,837.0] | 2.13 ± 2.32ms | 2.06ms | 2.40ms | 2.55ms | 3.06ms | 94.08ms | 0 |
| #3 | **Java** | 9,782.76 | [9,782.8 - 9,782.8] | 2.09 ± 1.08ms | 1.99ms | 2.37ms | 2.50ms | 5.44ms | 23.66ms | 0 |
| #4 | **Go** | 4,783.00 | [4,783.0 - 4,783.0] | 4.15 ± 1.28ms | 4.49ms | 5.53ms | 5.80ms | 6.85ms | 10.17ms | 0 |
| #5 | **Python** | 1,543.17 | [1,543.2 - 1,543.2] | 12.95 ± 2.36ms | 12.89ms | 15.91ms | 16.40ms | 19.23ms | 47.01ms | 0 |

### Endpoint: `/raw/2join`
| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **PHP** | 13,006.40 | [13,006.4 - 13,006.4] | 1.55 ± 0.77ms | 1.54ms | 1.80ms | 1.85ms | 1.98ms | 52.20ms | 0 |
| #2 | **Java** | 9,553.07 | [9,553.1 - 9,553.1] | 2.09 ± 0.45ms | 2.03ms | 2.51ms | 2.67ms | 3.24ms | 13.73ms | 0 |
| #3 | **Node.js** | 8,682.81 | [8,682.8 - 8,682.8] | 2.32 ± 1.05ms | 2.27ms | 2.77ms | 2.91ms | 3.28ms | 93.69ms | 0 |
| #4 | **Go** | 5,659.89 | [5,659.9 - 5,659.9] | 3.51 ± 1.28ms | 3.54ms | 5.16ms | 5.47ms | 6.05ms | 8.93ms | 0 |
| #5 | **Python** | 1,508.03 | [1,508.0 - 1,508.0] | 13.26 ± 2.25ms | 13.06ms | 15.86ms | 16.23ms | 19.07ms | 45.97ms | 0 |

### Endpoint: `/raw/3join`
| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **Java** | 3,580.99 | [3,581.0 - 3,581.0] | 5.58 ± 1.05ms | 5.34ms | 6.90ms | 7.44ms | 9.01ms | 15.48ms | 0 |
| #2 | **Go** | 3,577.97 | [3,578.0 - 3,578.0] | 5.59 ± 1.50ms | 5.34ms | 7.54ms | 8.38ms | 10.26ms | 18.19ms | 0 |
| #3 | **PHP** | 2,841.21 | [2,841.2 - 2,841.2] | 7.05 ± 2.27ms | 6.66ms | 10.13ms | 10.47ms | 11.68ms | 59.45ms | 0 |
| #4 | **Node.js** | 2,318.99 | [2,319.0 - 2,319.0] | 8.64 ± 2.50ms | 8.89ms | 11.21ms | 11.67ms | 13.09ms | 100.64ms | 0 |
| #5 | **Python** | 1,473.81 | [1,473.8 - 1,473.8] | 13.57 ± 3.06ms | 13.10ms | 17.34ms | 19.14ms | 22.67ms | 50.61ms | 0 |

### Endpoint: `/raw/4join`
| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **Go** | 3,085.37 | [3,085.4 - 3,085.4] | 6.48 ± 1.80ms | 6.14ms | 8.95ms | 10.03ms | 11.91ms | 18.30ms | 0 |
| #2 | **Java** | 2,861.28 | [2,861.3 - 2,861.3] | 6.99 ± 1.38ms | 6.66ms | 8.70ms | 9.49ms | 11.39ms | 27.10ms | 0 |
| #3 | **PHP** | 2,632.64 | [2,632.6 - 2,632.6] | 7.61 ± 2.48ms | 7.02ms | 11.50ms | 12.23ms | 13.51ms | 71.38ms | 0 |
| #4 | **Node.js** | 2,032.21 | [2,032.2 - 2,032.2] | 9.86 ± 2.94ms | 9.95ms | 13.15ms | 13.68ms | 15.22ms | 68.38ms | 0 |
| #5 | **Python** | 1,305.66 | [1,305.7 - 1,305.7] | 15.31 ± 3.54ms | 14.67ms | 19.66ms | 21.81ms | 26.06ms | 46.59ms | 0 |

---

## Suite: `post` — Docker (Container)

# Benchmark Results Summary: post_dkr.json

## Tier: POC / Small internal system (-t2 -c20 -d30s)

### Endpoint: `/raw/post/1table`
| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **Go** | 31,507.46 | [31,507.5 - 31,507.5] | 0.63 ± 0.27ms | 0.58ms | 0.80ms | 1.02ms | 1.52ms | 15.97ms | 0 |
| #2 | **Node.js** | 28,300.84 | [28,300.8 - 28,300.8] | 0.82 ± 2.66ms | 0.67ms | 0.81ms | 0.91ms | 1.31ms | 103.34ms | 0 |
| #3 | **PHP** | 27,518.46 | [27,518.5 - 27,518.5] | 0.75 ± 0.89ms | 0.70ms | 0.87ms | 0.96ms | 1.41ms | 58.93ms | 0 |
| #4 | **Java** | 26,542.69 | [26,542.7 - 26,542.7] | 0.78 ± 0.83ms | 0.71ms | 0.92ms | 1.00ms | 1.32ms | 21.03ms | 0 |
| #5 | **Python** | 8,822.72 | [8,822.7 - 8,822.7] | 2.26 ± 0.42ms | 2.21ms | 2.79ms | 2.98ms | 3.40ms | 20.23ms | 0 |

### Endpoint: `/raw/post/2table`
| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **Go** | 16,085.64 | [16,085.6 - 16,085.6] | 1.24 ± 0.33ms | 1.16ms | 1.50ms | 1.93ms | 2.68ms | 8.86ms | 0 |
| #2 | **Java** | 15,636.68 | [15,636.7 - 15,636.7] | 1.28 ± 0.61ms | 1.24ms | 1.56ms | 1.66ms | 1.96ms | 22.07ms | 0 |
| #3 | **Node.js** | 14,139.78 | [14,139.8 - 14,139.8] | 1.44 ± 1.06ms | 1.39ms | 1.60ms | 1.73ms | 2.13ms | 97.47ms | 0 |
| #4 | **PHP** | 13,092.98 | [13,093.0 - 13,093.0] | 1.54 ± 1.00ms | 1.41ms | 2.22ms | 2.69ms | 3.08ms | 66.45ms | 0 |
| #5 | **Python** | 5,937.10 | [5,937.1 - 5,937.1] | 3.46 ± 1.93ms | 3.30ms | 4.04ms | 4.31ms | 5.22ms | 62.41ms | 0 |

### Endpoint: `/raw/post/3table`
| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **Java** | 13,524.88 | [13,524.9 - 13,524.9] | 1.46 ± 0.29ms | 1.44ms | 1.78ms | 1.89ms | 2.16ms | 10.25ms | 0 |
| #2 | **Go** | 12,708.62 | [12,708.6 - 12,708.6] | 1.57 ± 0.42ms | 1.45ms | 2.07ms | 2.52ms | 3.29ms | 6.71ms | 0 |
| #3 | **PHP** | 11,181.41 | [11,181.4 - 11,181.4] | 1.80 ± 0.75ms | 1.79ms | 2.04ms | 2.10ms | 2.29ms | 61.81ms | 0 |
| #4 | **Node.js** | 10,494.52 | [10,494.5 - 10,494.5] | 1.93 ± 1.20ms | 1.83ms | 2.31ms | 2.44ms | 2.93ms | 113.39ms | 0 |
| #5 | **Python** | 5,037.29 | [5,037.3 - 5,037.3] | 4.06 ± 1.84ms | 3.87ms | 4.59ms | 4.83ms | 5.71ms | 66.61ms | 0 |

### Endpoint: `/raw/post/4table`
| Rank | Language | Requests/sec (Mean ± SD) | 95% CI (Req/s) | Latency Mean ± SD | p50 | p90 | p95 | p99 | Max | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **Java** | 12,805.47 | [12,805.5 - 12,805.5] | 1.55 ± 0.35ms | 1.50ms | 1.88ms | 2.01ms | 2.35ms | 16.55ms | 0 |
| #2 | **Go** | 10,592.01 | [10,592.0 - 10,592.0] | 1.88 ± 0.52ms | 1.71ms | 2.64ms | 3.12ms | 3.72ms | 6.58ms | 0 |
| #3 | **PHP** | 8,773.15 | [8,773.1 - 8,773.1] | 2.29 ± 1.01ms | 2.07ms | 3.44ms | 4.10ms | 4.84ms | 67.00ms | 0 |
| #4 | **Node.js** | 8,495.46 | [8,495.5 - 8,495.5] | 2.38 ± 1.02ms | 2.34ms | 2.79ms | 2.94ms | 3.59ms | 52.61ms | 0 |
| #5 | **Python** | 4,543.08 | [4,543.1 - 4,543.1] | 4.52 ± 2.23ms | 4.31ms | 4.99ms | 5.25ms | 6.92ms | 70.11ms | 0 |

---
