# 📊 Web Framework Benchmark: Comprehensive Summary

Multi-language performance evaluation across **Docker Containerized** and **Bare Metal (Host)** environments.

## ⚡ Executive Comparison: Docker vs Bare Metal (`/raw/1table` - Light Tier)

| Suite | Language | Docker (Req/s) | Bare Metal (Req/s) | Docker Latency | BME Latency | Overhead / Gain |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **get_no_index** | **Go** | 10,988.10 | 11,928.00 | 10.67ms | 9.30ms | +8.6% BME |
| **get_no_index** | **Java** | 9,231.73 | 11,958.11 | 12.24ms | 8.37ms | +29.5% BME |
| **get_no_index** | **Node.js** | 2,041.90 | 7,016.52 | 49.18ms | 16.30ms | +243.6% BME |
| **get_no_index** | **PHP** | 16,002.61 | 15,762.22 | 6.94ms | 7.27ms | -1.5% BME |
| **get_no_index** | **Python** | 2,515.54 | 1,624.44 | 40.03ms | 61.24ms | -35.4% BME |
| **get_with_index** | **Go** | 11,025.25 | - | 10.59ms | - | N/A |
| **get_with_index** | **Java** | 8,825.93 | - | 12.83ms | - | N/A |
| **get_with_index** | **Node.js** | 2,070.42 | - | 48.43ms | - | N/A |
| **get_with_index** | **PHP** | 17,290.74 | - | 6.46ms | - | N/A |
| **get_with_index** | **Python** | 2,521.69 | - | 39.48ms | - | N/A |
| **post** | **Go** | 7,123.85 | - | 14.05ms | - | N/A |
| **post** | **Java** | 5,708.88 | - | 17.63ms | - | N/A |
| **post** | **Node.js** | 7,297.44 | - | 13.94ms | - | N/A |
| **post** | **PHP** | 4,506.78 | - | 23.91ms | - | N/A |
| **post** | **Python** | 7,045.07 | - | 14.41ms | - | N/A |

---

## 📁 Suite: `get_no_index` — 🖥️ Bare Metal (Host)

# Benchmark Results Summary: get_no_index_bme.json

## 🎯 Tier: Minimum (Light) (-t2 -c100 -d10s)

### Endpoint: `/raw/1table`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 15,762.22 | 7.27ms | 63.12ms | 0 |
| 🥈  | **Java** | 11,958.11 | 8.37ms | 82.29ms | 0 |
| 🥉  | **Go** | 11,928.00 | 9.30ms | 71.29ms | 0 |
| 4.  | **Node.js** | 7,016.52 | 16.30ms | 312.95ms | 0 |
| 5.  | **Python** | 1,624.44 | 61.24ms | 142.13ms | 0 |

### Endpoint: `/raw/2join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **Go** | 5,057.66 | 20.11ms | 106.94ms | 0 |
| 🥈  | **PHP** | 4,846.69 | 26.28ms | 249.46ms | 0 |
| 🥉  | **Java** | 4,760.66 | 21.31ms | 105.33ms | 0 |
| 4.  | **Node.js** | 4,687.83 | 21.73ms | 119.10ms | 0 |
| 5.  | **Python** | 1,914.72 | 51.95ms | 106.87ms | 0 |

### Endpoint: `/raw/3join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 318.95 | 326.91ms | 1811.64ms | 0 |
| 🥈  | **Java** | 314.57 | 312.12ms | 537.97ms | 0 |
| 🥉  | **Python** | 305.79 | 320.55ms | 673.58ms | 0 |
| 4.  | **Go** | 305.74 | 320.09ms | 586.61ms | 0 |
| 5.  | **Node.js** | 305.11 | 321.28ms | 620.05ms | 0 |

### Endpoint: `/raw/4join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 937.90 | 121.01ms | 950.05ms | 0 |
| 🥈  | **Java** | 747.31 | 132.62ms | 359.14ms | 0 |
| 🥉  | **Go** | 738.14 | 134.05ms | 275.60ms | 0 |
| 4.  | **Node.js** | 736.60 | 134.39ms | 289.33ms | 0 |
| 5.  | **Python** | 696.35 | 142.21ms | 313.33ms | 0 |

## 🎯 Tier: Medium (Standard) (-t10 -c1000 -d30s)

### Endpoint: `/raw/1table`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 16,986.43 | 58.92ms | 224.52ms | 0 |
| 🥈  | **Go** | 14,278.26 | 144.64ms | 1996.46ms | 488 |
| 🥉  | **Java** | 13,148.71 | 79.38ms | 1764.95ms | 0 |
| 4.  | **Node.js** | 10,410.97 | 109.50ms | 1999.59ms | 38 |
| 5.  | **Python** | 2,199.80 | 450.30ms | 698.99ms | 0 |

### Endpoint: `/raw/2join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 5,091.11 | 200.57ms | 1228.26ms | 0 |
| 🥈  | **Go** | 4,985.96 | 219.87ms | 1998.35ms | 1662 |
| 🥉  | **Java** | 4,598.11 | 213.55ms | 547.46ms | 0 |
| 4.  | **Node.js** | 4,486.93 | 221.34ms | 1101.88ms | 0 |
| 5.  | **Python** | 2,423.18 | 408.94ms | 703.44ms | 0 |

### Endpoint: `/raw/3join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 313.49 | 1057.08ms | 1999.84ms | 5785 |
| 🥈  | **Java** | 311.83 | 1015.61ms | 1996.80ms | 8470 |
| 🥉  | **Go** | 310.95 | 951.28ms | 1999.76ms | 3831 |
| 4.  | **Node.js** | 300.10 | 1479.41ms | 1999.92ms | 8467 |
| 5.  | **Python** | 292.57 | 1407.92ms | 1999.99ms | 6739 |

### Endpoint: `/raw/4join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 912.98 | 821.92ms | 1999.89ms | 2815 |
| 🥈  | **Go** | 743.57 | 605.86ms | 1997.93ms | 3507 |
| 🥉  | **Java** | 735.55 | 1305.91ms | 1996.36ms | 2 |
| 4.  | **Node.js** | 708.49 | 1336.36ms | 1999.59ms | 1011 |
| 5.  | **Python** | 643.09 | 1249.09ms | 2000.00ms | 4054 |

## 🎯 Tier: Maximum (Stress) (-t20 -c10000 -d30s)

### Endpoint: `/raw/1table`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 16,471.48 | 597.21ms | 1738.09ms | 0 |
| 🥈  | **Go** | 15,635.48 | 376.88ms | 1999.98ms | 24899 |
| 🥉  | **Java** | 13,046.57 | 519.44ms | 1802.39ms | 1752 |
| 4.  | **Node.js** | 8,675.44 | 379.06ms | 1985.33ms | 4745 |
| 5.  | **Python** | 2,004.71 | 468.81ms | 1999.85ms | 25522 |

### Endpoint: `/raw/2join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 5,101.99 | 1395.56ms | 2000.00ms | 61865 |
| 🥈  | **Go** | 4,900.73 | 628.78ms | 1999.95ms | 34982 |
| 🥉  | **Java** | 4,531.62 | 1696.31ms | 1999.98ms | 2122 |
| 4.  | **Node.js** | 4,268.16 | 1371.84ms | 2000.00ms | 86220 |
| 5.  | **Python** | 2,232.18 | 422.93ms | 1998.30ms | 21502 |

### Endpoint: `/raw/3join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **PHP** | 314.41 | 991.84ms | 1994.88ms | 9115 |
| 🥈  | **Java** | 310.44 | 1023.20ms | 1996.88ms | 8676 |
| 🥉  | **Go** | 309.87 | 1083.31ms | 1999.37ms | 8171 |
| 4.  | **Node.js** | 298.40 | 1459.40ms | 1997.01ms | 8537 |
| 5.  | **Python** | 297.49 | 1327.73ms | 1998.82ms | 7926 |

### Endpoint: `/raw/4join`
| Rank | Language | Requests/sec | Avg Latency (ms) | Max Latency (ms) | Errors |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥇  | **Go** | 381.85 | 1051.63ms | 1999.45ms | 9766 |
| 🥈  | **Python** | 193.70 | 748.90ms | 1975.32ms | 4687 |
| 🥉  | **Java** | 189.54 | 287.27ms | 810.08ms | 5603 |
| 4.  | **PHP** | 173.18 | 1541.46ms | 1983.90ms | 5153 |
| 5.  | **Node.js** | 64.23 | 0.00ms | 0.00ms | 1933 |

---

## 📁 Suite: `get_no_index` — 🐳 Docker (Container)

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

## 📁 Suite: `get_with_index` — 🐳 Docker (Container)

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

## 📁 Suite: `post` — 🐳 Docker (Container)

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
