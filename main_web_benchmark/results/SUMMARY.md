# 📊 Web Benchmark Comprehensive Results Summary

Generated from 3 test suite result datasets.

## 📁 Suite: `get_no_index (Docker)`

# Benchmark Results Summary: get_no_index_dkr.json

## 🎯 Tier: Minimum (Light) (-t2 -c100 -d10s)

### Endpoint: `/raw/1table`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **Go** | 11,050.36 | 10.64ms | 86.38ms | 0 |
| 🥈  | **Java** | 8,862.32 | 12.36ms | 130.60ms | 0 |
| 🥉  | **PHP** | 3,945.37 | 29.54ms | 251.27ms | 39493 |
| 4.  | **Python** | 2,371.56 | 42.60ms | 209.73ms | 0 |
| 5.  | **Node.js** | 1,326.70 | 78.05ms | 545.75ms | 0 |

### Endpoint: `/raw/2join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **Go** | 7,164.93 | 14.24ms | 93.96ms | 0 |
| 🥈  | **Java** | 6,762.66 | 14.95ms | 89.06ms | 0 |
| 🥉  | **PHP** | 3,104.36 | 35.12ms | 246.72ms | 31102 |
| 4.  | **Python** | 2,005.45 | 50.24ms | 155.99ms | 0 |
| 5.  | **Node.js** | 1,432.18 | 38.36ms | 156.26ms | 128448 |

### Endpoint: `/raw/3join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 3,041.09 | 37.96ms | 316.91ms | 30454 |
| 🥈  | **Go** | 261.59 | 379.03ms | 1639.52ms | 0 |
| 🥉  | **Java** | 259.74 | 376.95ms | 624.43ms | 0 |
| 4.  | **Python** | 189.72 | 512.49ms | 1508.63ms | 0 |
| 5.  | **Node.js** | 0.00 | 0.00ms | 0.00ms | 1 |

### Endpoint: `/raw/4join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 3,222.86 | 36.29ms | 268.25ms | 32265 |
| 🥈  | **Go** | 737.73 | 134.26ms | 320.75ms | 0 |
| 🥉  | **Java** | 727.17 | 136.39ms | 373.16ms | 0 |
| 4.  | **Python** | 420.24 | 237.11ms | 736.93ms | 0 |
| 5.  | **Node.js** | 0.00 | 0.00ms | 0.00ms | 1 |

---

## 📁 Suite: `get_with_index (Docker)`

# Benchmark Results Summary: get_with_index_dkr.json

## 🎯 Tier: Minimum (Light) (-t2 -c100 -d10s)

### Endpoint: `/raw/1table`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 17,290.74 | 6.46ms | 67.95ms | 0 |
| 🥈  | **Go** | 11,025.25 | 10.59ms | 87.97ms | 0 |
| 🥉  | **Java** | 8,825.93 | 12.83ms | 198.85ms | 0 |
| 4.  | **Python** | 2,521.69 | 39.48ms | 120.24ms | 0 |
| 5.  | **Node.js** | 2,070.42 | 48.43ms | 311.15ms | 0 |

### Endpoint: `/raw/2join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 5,319.85 | 21.79ms | 178.40ms | 0 |
| 🥈  | **Go** | 5,134.39 | 19.72ms | 103.95ms | 0 |
| 🥉  | **Java** | 4,473.91 | 22.94ms | 200.01ms | 0 |
| 4.  | **Python** | 2,794.40 | 35.87ms | 121.76ms | 0 |
| 5.  | **Node.js** | 2,454.18 | 40.80ms | 178.42ms | 0 |

### Endpoint: `/raw/3join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 3,713.40 | 31.52ms | 287.63ms | 0 |
| 🥈  | **Go** | 3,273.10 | 32.62ms | 296.70ms | 0 |
| 🥉  | **Java** | 3,076.09 | 34.24ms | 224.71ms | 0 |
| 4.  | **Python** | 2,035.89 | 50.24ms | 182.47ms | 0 |
| 5.  | **Node.js** | 1,850.64 | 53.98ms | 220.75ms | 0 |

### Endpoint: `/raw/4join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 3,863.85 | 30.34ms | 274.26ms | 0 |
| 🥈  | **Java** | 3,650.21 | 28.65ms | 208.09ms | 0 |
| 🥉  | **Go** | 3,601.68 | 29.38ms | 198.21ms | 0 |
| 4.  | **Python** | 1,890.68 | 53.74ms | 188.25ms | 0 |
| 5.  | **Node.js** | 1,688.02 | 58.95ms | 195.26ms | 0 |

---

## 📁 Suite: `post (Docker)`

# Benchmark Results Summary: post_dkr.json

## 🎯 Tier: Minimum (Light) (-t2 -c100 -d10s)

### Endpoint: `/raw/post/1table`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **Node.js** | 7,297.44 | 13.94ms | 131.60ms | 0 |
| 🥈  | **Go** | 7,123.85 | 14.05ms | 55.39ms | 0 |
| 🥉  | **Python** | 7,045.07 | 14.41ms | 93.95ms | 0 |
| 4.  | **Java** | 5,708.88 | 17.63ms | 96.46ms | 0 |
| 5.  | **PHP** | 4,506.78 | 23.91ms | 135.78ms | 0 |

### Endpoint: `/raw/post/2table`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **Go** | 4,962.62 | 20.38ms | 119.03ms | 0 |
| 🥈  | **Python** | 4,836.32 | 20.87ms | 116.57ms | 0 |
| 🥉  | **Java** | 4,539.56 | 22.01ms | 81.70ms | 0 |
| 4.  | **Node.js** | 4,327.39 | 23.20ms | 108.80ms | 0 |
| 5.  | **PHP** | 3,375.61 | 37.14ms | 292.37ms | 0 |

### Endpoint: `/raw/post/3table`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **Python** | 4,395.94 | 22.75ms | 92.53ms | 0 |
| 🥈  | **Go** | 4,008.93 | 25.09ms | 115.53ms | 0 |
| 🥉  | **Java** | 3,896.54 | 25.85ms | 121.49ms | 0 |
| 4.  | **Node.js** | 3,830.39 | 26.06ms | 87.94ms | 0 |
| 5.  | **PHP** | 2,520.47 | 44.71ms | 316.47ms | 0 |

### Endpoint: `/raw/post/4table`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **Python** | 3,684.23 | 27.18ms | 105.08ms | 0 |
| 🥈  | **Java** | 3,256.14 | 30.69ms | 110.19ms | 0 |
| 🥉  | **Node.js** | 2,907.82 | 34.41ms | 117.53ms | 0 |
| 4.  | **Go** | 2,818.92 | 35.83ms | 151.44ms | 0 |
| 5.  | **PHP** | 2,484.42 | 48.57ms | 410.79ms | 0 |

---
