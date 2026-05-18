# Door Problem Benchmark

## 🚪 Task Overview

The Door Problem is a classic algorithmic puzzle that tests performance on complex state management and iterative logic across different programming languages.

## 📖 Problem Description

### The Scenario

Imagine you have **1,000,000 doors** in a long corridor, all initially **closed**. You make multiple passes through the corridor:

- **Pass 1**: You visit every door and toggle it (all doors are now **open**)
- **Pass 2**: You visit every 2nd door and toggle it (doors 2, 4, 6, 8, ... are now **closed**)
- **Pass 3**: You visit every 3rd door and toggle it (doors 3, 6, 9, 12, ... toggle)
- **Pass 4**: You visit every 4th door and toggle it (doors 4, 8, 12, 16, ... toggle)
- **...continue for 1,000,000 passes**

After all passes, determine which doors are **open** and which are **closed**.

### Mathematical Insight

A door at position `n` gets toggled by every divisor of `n`. So:
- Door 1: Toggled 1 time (divisor: 1) → **OPEN**
- Door 4: Toggled 3 times (divisors: 1, 2, 4) → **OPEN** (2 toggles cancel, 3rd opens it)
- Door 9: Toggled 3 times (divisors: 1, 3, 9) → **OPEN** (2 toggles cancel, 3rd opens it)
- Door 6: Toggled 4 times (divisors: 1, 2, 3, 6) → **CLOSED** (even toggles = closed)

**Result**: Only doors at perfect square positions remain **open** (1, 4, 9, 16, 25, ...)

## 🎯 Why This Benchmark Matters

### Performance Aspects Tested

1. **Loop Efficiency**
   - Nested loops (O(n²) complexity)
   - Iterator optimization
   - Loop unrolling capabilities

2. **Memory Management**
   - Large array allocation (1,000,000 elements)
   - Access patterns and cache efficiency
   - Data structure choice (array vs set vs bitfield)

3. **Conditional Logic**
   - Boolean state toggling
   - Tight loop performance
   - Branch prediction

4. **Compiler Optimizations**
   - Loop optimization
   - Dead code elimination
   - Vectorization capabilities

### Real-World Applications

- **State Machine Simulation**: Managing millions of state changes
- **Resource Allocation**: Toggle resources in and out
- **Event Processing**: Processing cascading events
- **Permission Systems**: Toggle permissions for multiple users/resources

## 📊 Implementation Variants

### Version 1: Standard Door Array

**Algorithm**:
```
for pass = 1 to 1000000:
    for door = pass to 1000000 step pass:
        toggle door[door]
```

**Time Complexity**: O(n²) where n = 1,000,000
**Space Complexity**: O(n) for boolean array

### Version 2: Optimized with Bitfield

Uses bit flags instead of boolean array for better memory:
- 8 doors per byte instead of 1 byte per door
- Reduced memory: ~125KB instead of 1MB
- Faster iterations and comparisons

### Version 3: Direct Calculation

Skip simulation, calculate which doors are open:
```
open_doors = []
for i = 1 to sqrt(1000000):
    open_doors.append(i * i)
```

**Time Complexity**: O(√n) - Much faster!
**Trade-off**: Requires mathematical insight

## 📁 Project Structure

```
door/
├── door.py                 # Python implementation (standard)
├── door.js                 # Node.js implementation
├── door.go                 # Go implementation
├── door.php                # PHP implementation
├── door.java               # Java implementation
├── doorNoprint.py          # Python optimized (no output)
├── doorNoprint.js          # Node.js optimized
├── doorNoprint.php         # PHP optimized
├── doorNoprint.go          # Go optimized (if exists)
├── doorNoprint.py          # Python optimized
├── Dockerfile.python       # Python container
├── Dockerfile.nodejs       # Node.js container
├── Dockerfile.go           # Go container
├── Dockerfile.php          # PHP container
├── Dockerfile.java         # Java container
├── main                    # Runner script (runs all implementations)
├── README.md               # This file
└── myenv/                  # Virtual environment (Python)
```

## 🚀 Running the Benchmark

### Option 1: Run All Implementations

```bash
cd benchmark/interactive_function/door
./main
```

This runs all language implementations and compares results.

### Option 2: Run Individual Language

**Python:**
```bash
python3 door.py
```

**Node.js:**
```bash
node door.js
```

**Go:**
```bash
go run door.go
```

**PHP:**
```bash
php door.php
```

**Java:**
```bash
javac door.java && java door
```

### Option 3: Run Optimized Versions (No Output)

**Python:**
```bash
python3 doorNoprint.py
```

Optimized versions skip printing results, focusing on pure computation time.

### Option 4: Docker Execution

**Build:**
```bash
docker build -f Dockerfile.python -t door-python .
docker build -f Dockerfile.nodejs -t door-nodejs .
docker build -f Dockerfile.go -t door-go .
docker build -f Dockerfile.php -t door-php .
docker build -f Dockerfile.java -t door-java .
```

**Run:**
```bash
docker run door-python
docker run door-nodejs
docker run door-go
docker run door-php
docker run door-java
```

## 📈 Expected Results & Performance

### Typical Execution Times (1,000,000 doors)

Based on hardware and optimization level:

| Language | Approach | Time | Notes |
|----------|----------|------|-------|
| Go | Compiled | 0.5 - 2s | Fastest, excellent optimization |
| Java | JVM + JIT | 1 - 3s | Good after warmup |
| Node.js | V8 engine | 2 - 5s | Good optimization |
| Python | Interpreted | 5 - 15s | Slower without PyPy |
| PHP | Scripted | 10 - 20s | Slowest on this task |

**Note**: First run may be slower due to JIT warmup. Multiple runs show better times.

### Output Example

```
=== Door Problem Benchmark ===
Doors: 1000000
Analyzing door states...

Open doors found: 1000
First 20 open doors: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400]

Execution time: 2.345 seconds
Memory used: 1.2 MB
```

## 🔍 Key Observations

### Performance Factors

1. **Nested Loop Optimization**
   - Go: Excellent loop unrolling
   - Java: JIT optimizes after warmup
   - Node.js: V8 handles well
   - Python: Slowest due to interpretation

2. **Memory Access Patterns**
   - Sequential access is optimal
   - Cache-friendly patterns important
   - Array allocation crucial

3. **Language Features Impact**
   - Compiled languages: 5-10x faster
   - JIT languages: 2-5x slower than compiled
   - Interpreted: 10-50x slower

4. **Optimization Techniques**
   - Pre-calculation: Skips simulation entirely
   - Bitfield: Reduces memory 8x
   - Vectorization: SIMD instructions (if used)

## 💡 Optimization Tips

### For Python
```python
# Use numpy for vectorization
import numpy as np
doors = np.zeros(1000001, dtype=bool)

# Or use bitarray for memory efficiency
from bitarray import bitarray
doors = bitarray(1000001)
```

### For JavaScript
```javascript
// Use TypedArray for better performance
const doors = new Uint8Array(1000001);

// Or boolean array with aggressive optimization
const doors = new Array(1000001).fill(false);
```

### For Go
```go
// Use array instead of slice if size is known
var doors [1000001]bool

// Or use byte array for 8x memory savings
doors := make([]byte, (1000001+7)/8)
```

### For Java
```java
// Use BitSet for memory efficiency and speed
BitSet doors = new BitSet(1000001);

// Or boolean array
boolean[] doors = new boolean[1000001];
```

### For PHP
```php
// Use SPL_FIXED_ARRAY for better performance
$doors = new SplFixedArray(1000001);

// SplFixedArray is ~2x faster than arrays
```

## 🧪 Variations to Try

### 1. Different Door Counts
Test with different sizes:
- 100 doors (very fast)
- 10,000 doors (medium)
- 1,000,000 doors (standard)
- 10,000,000 doors (stress test)

### 2. Without Output
Removes I/O overhead:
```bash
# Compare
time python3 door.py          # With output
time python3 doorNoprint.py   # Without output
```

### 3. Warm-up Iterations
Run multiple times to test JIT warmup:
```python
for run in range(5):
    benchmark_doors()  # Second+ runs faster
```

### 4. Memory Profile
Monitor memory usage:
```bash
# Linux
time -v python3 door.py

# Or use memory profiler
python3 -m memory_profiler door.py
```

## 📊 Analysis Metrics

### Metrics to Track

1. **Execution Time**
   - Wall clock time
   - CPU time vs I/O time

2. **Memory Usage**
   - Peak memory
   - Memory per door

3. **Throughput**
   - Operations per second
   - Door toggles per second

4. **Efficiency**
   - Time per door
   - Memory efficiency

### Collecting Results

```bash
# Time measurement
time python3 door.py

# Memory profiling (Python)
python3 -m memory_profiler door.py

# Detailed timing (Linux)
time -v python3 door.py

# CPU profiling (Python)
python3 -m cProfile door.py
```

## 🎓 Learning Outcomes

This benchmark teaches:

1. **Algorithm Complexity**
   - Nested loops = O(n²)
   - Direct calculation = O(√n)
   - Trade-offs between approaches

2. **Language Characteristics**
   - Compilation vs interpretation
   - JIT optimization benefits
   - Memory management differences

3. **Optimization Techniques**
   - Loop optimization
   - Memory efficiency (bitfield)
   - Mathematical shortcuts

4. **Performance Analysis**
   - Profiling tools
   - Bottleneck identification
   - Optimization validation

## 🔧 Troubleshooting

### Issue: Out of Memory

**Solution**: Use smaller door count or optimize memory usage
```python
# Instead of boolean array, use bitarray
from bitarray import bitarray
doors = bitarray(1000001)
```

### Issue: Very Slow Execution

**Solution**: 
- Use optimized version (doorNoprint.*)
- Try compiled language (Go)
- Check system load
- Increase available RAM

### Issue: Different Results Between Languages

**Possible causes**:
- Rounding errors in floating-point
- Integer overflow (use 64-bit)
- Initialization differences

**Solution**: 
- Verify logic matches
- Check data types
- Add debug output

## 📚 References

- **Algorithm Analysis**: https://en.wikipedia.org/wiki/Analysis_of_algorithms
- **Big O Notation**: https://en.wikipedia.org/wiki/Big_O_notation
- **Perfect Squares**: https://en.wikipedia.org/wiki/Square_number
- **Number Divisors**: https://en.wikipedia.org/wiki/Divisor

## 📝 Implementation Checklist

- [ ] Read and understand the problem
- [ ] Choose language (or implement in all)
- [ ] Create basic algorithm
- [ ] Test with small numbers (10, 100 doors)
- [ ] Verify correct results (open doors = perfect squares)
- [ ] Run with 1,000,000 doors
- [ ] Measure execution time
- [ ] Profile memory usage
- [ ] Identify bottlenecks
- [ ] Optimize if needed
- [ ] Compare across languages
- [ ] Document findings

## 🎯 Next Steps

1. **Run the benchmark** and observe times
2. **Compare across languages** using provided implementations
3. **Try optimizations** (bitfield, pre-calculation)
4. **Profile the code** to find bottlenecks
5. **Analyze results** and draw conclusions about language performance

---

**Last Updated**: May 18, 2025
**Difficulty Level**: Medium
**Time to Complete**: 5-30 minutes per language
**Prerequisite Knowledge**: Basic loops, arrays, boolean logic
