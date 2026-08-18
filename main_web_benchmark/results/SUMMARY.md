# 📊 Web Benchmark Comprehensive Results Summary

Generated from 3 test suite result datasets.

## 📁 Suite: `get_no_index (Docker)`

# Benchmark Results Summary: get_no_index_dkr.json

## 🎯 Tier: Minimum (Light) (-t2 -c100 -d10s)

### Endpoint: `/raw/1table`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 16,002.61 | 6.94ms | 77.51ms | 0 |
| 🥈  | **Go** | 10,988.10 | 10.67ms | 92.46ms | 0 |
| 🥉  | **Java** | 9,231.73 | 12.24ms | 232.36ms | 0 |
| 4.  | **Python** | 2,515.54 | 40.03ms | 124.72ms | 0 |
| 5.  | **Node.js** | 2,041.90 | 49.18ms | 295.95ms | 0 |

### Endpoint: `/raw/2join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 6,773.97 | 18.64ms | 195.42ms | 0 |
| 🥈  | **Go** | 6,390.75 | 15.85ms | 83.28ms | 0 |
| 🥉  | **Java** | 5,889.99 | 17.17ms | 96.12ms | 0 |
| 4.  | **Python** | 2,917.55 | 34.19ms | 104.59ms | 0 |
| 5.  | **Node.js** | 2,701.73 | 37.02ms | 141.64ms | 0 |

### Endpoint: `/raw/3join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 278.71 | 352.91ms | 1998.21ms | 55 |
| 🥈  | **Java** | 276.22 | 354.11ms | 715.42ms | 0 |
| 🥉  | **Go** | 274.64 | 355.21ms | 692.12ms | 0 |
| 4.  | **Node.js** | 273.64 | 356.99ms | 757.60ms | 0 |
| 5.  | **Python** | 268.77 | 363.73ms | 721.17ms | 0 |

### Endpoint: `/raw/4join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 904.02 | 124.88ms | 961.99ms | 0 |
| 🥈  | **Go** | 736.83 | 134.03ms | 320.66ms | 0 |
| 🥉  | **Java** | 727.80 | 136.31ms | 343.77ms | 0 |
| 4.  | **Python** | 651.11 | 153.37ms | 489.18ms | 0 |
| 5.  | **Node.js** | 635.70 | 155.54ms | 392.27ms | 0 |

## 🎯 Tier: Medium (Standard) (-t10 -c1000 -d30s)

### Endpoint: `/raw/1table`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 16,258.17 | 62.61ms | 393.58ms | 0 |
| 🥈  | **Go** | 13,054.31 | 144.19ms | 1999.49ms | 375 |
| 🥉  | **Java** | 11,471.38 | 90.62ms | 1289.16ms | 0 |
| 4.  | **Python** | 2,317.14 | 427.89ms | 782.82ms | 0 |
| 5.  | **Node.js** | 2,056.05 | 414.50ms | 1988.10ms | 615 |

### Endpoint: `/raw/2join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 6,838.59 | 153.89ms | 1325.69ms | 0 |
| 🥈  | **Go** | 6,390.91 | 207.48ms | 1999.32ms | 1293 |
| 🥉  | **Java** | 5,856.41 | 171.73ms | 1346.61ms | 0 |
| 4.  | **Python** | 2,743.71 | 361.64ms | 633.26ms | 0 |
| 5.  | **Node.js** | 2,617.35 | 340.37ms | 1990.67ms | 570 |

### Endpoint: `/raw/3join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 280.18 | 1126.23ms | 1999.89ms | 2997 |
| 🥈  | **Go** | 277.80 | 973.01ms | 1999.62ms | 3679 |
| 🥉  | **Java** | 276.84 | 985.38ms | 1999.34ms | 7666 |
| 4.  | **Node.js** | 267.07 | 1549.69ms | 1999.70ms | 7413 |
| 5.  | **Python** | 264.40 | 1353.48ms | 1998.10ms | 6822 |

### Endpoint: `/raw/4join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 904.60 | 613.18ms | 1999.14ms | 5287 |
| 🥈  | **Java** | 730.92 | 1333.08ms | 1986.86ms | 14 |
| 🥉  | **Go** | 730.66 | 616.85ms | 1999.18ms | 3350 |
| 4.  | **Python** | 648.68 | 1155.28ms | 1999.50ms | 4513 |
| 5.  | **Node.js** | 614.90 | 1440.45ms | 1999.96ms | 3248 |

## 🎯 Tier: Maximum (Stress) (-t20 -c10000 -d30s)

### Endpoint: `/raw/1table`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 15,494.73 | 621.56ms | 1999.60ms | 1556 |
| 🥈  | **Go** | 13,950.35 | 407.90ms | 1999.96ms | 26568 |
| 🥉  | **Java** | 11,354.82 | 685.67ms | 1999.38ms | 2985 |
| 4.  | **Python** | 2,218.18 | 633.89ms | 1999.80ms | 5350 |
| 5.  | **Node.js** | 2,005.32 | 589.88ms | 1986.36ms | 1147 |

### Endpoint: `/raw/2join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 6,275.77 | 1204.53ms | 1999.96ms | 38139 |
| 🥈  | **Go** | 5,849.14 | 580.10ms | 1999.96ms | 36621 |
| 🥉  | **Java** | 5,364.46 | 1416.72ms | 1995.08ms | 4062 |
| 4.  | **Node.js** | 2,436.20 | 516.88ms | 1999.95ms | 1531 |
| 5.  | **Python** | 2,355.07 | 498.66ms | 1999.35ms | 14078 |

### Endpoint: `/raw/3join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **Python** | 254.30 | 1121.09ms | 1999.76ms | 6981 |
| 🥈  | **PHP** | 244.34 | 1008.27ms | 1976.67ms | 13074 |
| 🥉  | **Java** | 240.95 | 1071.42ms | 1999.24ms | 12853 |
| 4.  | **Go** | 239.06 | 1216.68ms | 1995.56ms | 12913 |
| 5.  | **Node.js** | 233.48 | 1447.56ms | 1998.36ms | 11772 |

### Endpoint: `/raw/4join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **Go** | 234.33 | 1135.61ms | 1995.93ms | 12200 |
| 🥈  | **Python** | 174.25 | 855.59ms | 1990.60ms | 9811 |
| 🥉  | **PHP** | 66.99 | 1621.97ms | 1993.98ms | 8997 |
| 4.  | **Java** | 3.89 | 321.19ms | 321.19ms | 5482 |
| 5.  | **Node.js** | 0.00 | 0.00ms | 0.00ms | 6517 |

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
