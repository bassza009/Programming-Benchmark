# Benchmark Suite - Interactive & Recursive Functions

Complete benchmarking suite for testing algorithm performance across multiple programming languages.

##  Benchmark Overview

This folder contains two categories of algorithm benchmarks:

1. **Interactive Functions** - Direct algorithm implementations
2. **Recursive Functions** - Function recursion performance testing

Each benchmark is implemented in **5 programming languages**:
-  **Python** - Interpreted, dynamic typing
-  **Node.js** - Event-driven, JavaScript engine
-  **Go** - Compiled, concurrent
-  **PHP** - Scripted, web-focused
-  **Java** - Virtual machine, JIT compilation

---

##  Folder Structure

```
benchmark/
├── interactive_function/          # Direct algorithm implementations
│   ├── bubble_sort/              # Sorting algorithm
│   ├── door/                     # State toggling puzzle
│   ├── Metrix_multiplication/    # Matrix math operations
│   ├── primeNumCount/            # Prime number finding
│   └── prisoners/                # Logic puzzle
├── Recursive_function/            # Recursion-focused tasks
│   ├── factorial/                # Recursive calculation
│   └── fibonacci/                # Recursive sequence
├── README.md                      # This file
└── run_all.sh                     # Run all benchmarks script
```

---

##  Interactive Functions (5 Tasks)

### 1.  Bubble Sort
**Location**: `interactive_function/bubble_sort/`

**What it does**:
- Implements bubble sort algorithm to sort an array
- Tests basic sorting performance
- Measures loop and comparison efficiency

**Performance Focus**:
- Loop optimization
- Array access patterns
- Comparison operations

**Typical Results** (sorting 10,000 elements):
- Go: ~50ms
- Java: ~100ms
- Node.js: ~200ms
- Python: ~500ms
- PHP: ~1000ms

**Quick Start**:
```bash
cd interactive_function/bubble_sort
./main                  # Run all languages
python3 bubble.py       # Run Python only
```

**Files**:
- `bubble.{py,js,go,php,java}` - Language implementations
- `Dockerfile.*` - Container definitions

---

### 2.  Door Problem
**Location**: `interactive_function/door/`

**What it does**:
- Classic algorithmic puzzle: toggle doors based on pattern
- 1,000,000 doors, toggle by multiples
- Determines which doors remain open

**Performance Focus**:
- Nested loop efficiency
- Memory management
- Compiler optimization

**Key Insight**:
- Result: Only doors at perfect squares remain open (1, 4, 9, 16, 25, ...)
- Reason: Each door toggled by divisors, odd divisors = open

**Typical Results** (1,000,000 doors):
- Go: 1-2 seconds
- Java: 2-3 seconds
- Node.js: 3-5 seconds
- Python: 8-15 seconds
- PHP: 15-25 seconds

**Quick Start**:
```bash
cd interactive_function/door
./main              # Run all languages
node door.js        # Run Node.js only
./doorNoprint.py    # Run optimized version
```

**See also**: [Door README](interactive_function/door/README.md) for detailed analysis

---

### 3.  Matrix Multiplication
**Location**: `interactive_function/Metrix_multiplication/`

**What it does**:
- Multiplies large matrices (typically 500x500 or larger)
- Tests floating-point arithmetic
- CPU-intensive computation

**Performance Focus**:
- Floating-point operations
- Cache efficiency
- Memory bandwidth
- Compiler vectorization

**Typical Results** (multiplying 500x500 matrices):
- Go: 200-500ms
- Java: 300-800ms
- Node.js: 500-1500ms
- Python: 1-3 seconds
- PHP: 5-15 seconds

**Quick Start**:
```bash
cd interactive_function/Metrix_multiplication
./main                  # Run all languages
python3 Metrix.py       # Run Python only
```

**Files**:
- `Metrix.py`, `Metrix.js`, `Metrixtestarray.php`, `Metrixv2.go`, `Metrix.java`
- `results/` - Output matrices and timing data

---

### 4.  Prime Number Count
**Location**: `interactive_function/primeNumCount/`

**What it does**:
- Finds all prime numbers up to 1,000,000
- Uses optimized prime-checking algorithm
- Tests integer arithmetic performance

**Performance Focus**:
- Integer operations
- Algorithm optimization
- Loop efficiency
- Conditional logic

**Typical Results** (primes up to 1,000,000):
- Go: 50-200ms
- Java: 100-300ms
- Node.js: 200-600ms
- Python: 500-1500ms
- PHP: 1-5 seconds

**Result**: ~78,498 primes found

**Quick Start**:
```bash
cd interactive_function/primeNumCount
./main              # Run all languages
go run prime.go      # Run Go only
```

---

### 5.  Prisoners Problem
**Location**: `interactive_function/prisoners/`

**What it does**:
- Simulates a logic puzzle with prisoners and colored caps
- Tests complex conditional logic
- Evaluates decision tree performance

**Performance Focus**:
- Complex branching logic
- Conditional performance
- State management

**Puzzle**:
- N prisoners must guess cap color
- Optimize strategy for survival
- Performance: How fast can solution be calculated?

**Quick Start**:
```bash
cd interactive_function/prisoners
./main                  # Run all languages
java prisoners          # Run Java
```

**Files**:
- `prisoners.{py,js,go,php,java}` - Implementations
- `php.json` - Configuration data

---

##  Recursive Functions (2 Tasks)

### 6.  Factorial
**Location**: `Recursive_function/factorial/`

**What it does**:
- Calculates factorial using pure recursion
- Tests recursive call overhead
- Measures stack efficiency

**Algorithm**:
```
factorial(n) = 1          if n ≤ 1
factorial(n) = n × factorial(n-1)   otherwise
```

**Performance Focus**:
- Function call overhead
- Stack management
- Tail-call optimization
- Recursion depth

**Typical Results** (factorial of 30):
- Go: < 1ms (compiled, optimized)
- Java: 1-5ms (JIT after warmup)
- Node.js: 2-10ms (V8 engine)
- Python: 5-20ms (interpreted)
- PHP: 10-50ms (scripted)

**Quick Start**:
```bash
cd Recursive_function/factorial
./main              # Run all languages
python3 factorial.py
```

**Files**:
- `factorial.{py,js,go,php,java}` - Recursive implementations
- `Dockerfile.*` - Container definitions

---

### 7.  Fibonacci
**Location**: `Recursive_function/fibonacci/`

**What it does**:
- Calculates Fibonacci numbers using naive recursion
- Tests exponential time complexity impact
- Demonstrates importance of optimization

**Algorithm**:
```
fib(0) = 0
fib(1) = 1
fib(n) = fib(n-1) + fib(n-2)    otherwise
```

**Performance Focus**:
- Exponential recursion
- Duplicate computation
- Memoization benefits
- Optimization strategies

**Complexity**:
- Naive: O(2^n) - **Very slow for n > 40**
- With memoization: O(n) - **Much faster**
- Dynamic programming: O(n) with O(1) space

**Typical Results** (fibonacci(35)):
- Go: 100-500ms
- Java: 200-1000ms
- Node.js: 500-2000ms
- Python: 1-5 seconds
- PHP: 5-15 seconds

**Observation**: Shows massive performance differences for exponential algorithms

**Quick Start**:
```bash
cd Recursive_function/fibonacci
./main              # Run all languages
node fibonacci.js   # Run Node.js only
```

**Files**:
- `fibonacci.{py,js,go,php,java}` - Recursive implementations
- `Dockerfile.*` - Container definitions

---

##  Running Benchmarks

### Run All Benchmarks

```bash
# From root benchmark directory
./run_all.sh

# Or from anywhere
cd benchmark && bash ./run_all.sh
```

### Run Individual Category

```bash
# All interactive benchmarks
cd interactive_function
for dir in */; do
    echo "Running $dir..."
    cd "$dir"
    ./main
    cd ..
done

# All recursive benchmarks
cd ../Recursive_function
for dir in */; do
    echo "Running $dir..."
    cd "$dir"
    ./main
    cd ..
done
```

### Run Specific Benchmark

```bash
# Door benchmark
cd interactive_function/door
./main

# Or specific language
python3 door.py
node door.js
go run door.go
```

### Run with Docker

```bash
cd interactive_function/door

# Build and run Python
docker build -f Dockerfile.python -t door-py .
docker run door-py

# Build and run Go (fastest)
docker build -f Dockerfile.go -t door-go .
docker run door-go
```

---

##  Performance Comparison

### Language Ranking (by speed)

**For Compute-Heavy Tasks**:
1.  **Go** - Compiled, optimized (1x baseline)
2.  **Java** - JVM + JIT (1.5-3x Go)
3.  **Node.js** - V8 engine (2-5x Go)
4.  **Python** - Interpreted (5-15x Go)
5.  **PHP** - Scripted (10-25x Go)

**Factors Affecting Performance**:
- JIT warmup (Java faster after 2-3 runs)
- Algorithm complexity
- Memory efficiency
- Language runtime overhead

### Expected Performance Ratios

| Task | Go | Java | Node.js | Python | PHP |
|------|----|----|---------|--------|-----|
| Bubble Sort | 1x | 2x | 4x | 10x | 20x |
| Door Problem | 1x | 2-3x | 3-5x | 8-15x | 15-25x |
| Matrix Multiply | 1x | 2-3x | 3-5x | 5-10x | 10-20x |
| Prime Count | 1x | 2-3x | 4-8x | 10-15x | 15-30x |
| Fibonacci(35) | 1x | 2-5x | 5-10x | 10-20x | 15-30x |

---

##  Analysis Tools

### Measuring Performance

**Time a specific task**:
```bash
# Using time command
time python3 door.py

# Detailed timing (Linux)
time -v python3 door.py

# Multiple runs (average)
for i in {1..5}; do
    echo "Run $i:"
    time python3 door.py
done
```

**Memory profiling** (Python):
```bash
# Install profiler
pip3 install memory-profiler

# Profile execution
python3 -m memory_profiler door.py
```

**CPU profiling** (Python):
```bash
# Profile CPU usage
python3 -m cProfile door.py | head -20
```

---

##  Learning Outcomes

### What These Benchmarks Teach

1. **Language Characteristics**
   - Compilation vs interpretation impact
   - JIT compilation benefits
   - Runtime overhead differences

2. **Algorithm Efficiency**
   - Big O notation impact
   - Exponential vs polynomial complexity
   - Optimization opportunities

3. **Performance Optimization**
   - Loop optimization
   - Memory access patterns
   - Compiler capabilities

4. **Recursion Understanding**
   - Recursive call overhead
   - Stack usage
   - Memoization benefits
   - Tail-call optimization

5. **Practical Skills**
   - Profiling and measurement
   - Bottleneck identification
   - Language selection criteria

---

##  Customization

### Modify Benchmark Parameters

**Increase Problem Size** (in source files):
- Door: Change `1000000` to `10000000`
- Bubble Sort: Increase array size
- Fibonacci: Calculate higher number (careful: very slow!)
- Prime Count: Search up to 10,000,000

**Example - Python Door with 10M doors**:
```python
doors = [False] * 10000001  # 10 million doors

for pass_num in range(1, 10000001):
    for door_num in range(pass_num, 10000001, pass_num):
        doors[door_num] = not doors[door_num]
```

### Add Optimizations

**Python with NumPy** (matrix multiplication):
```python
import numpy as np
A = np.random.rand(500, 500)
B = np.random.rand(500, 500)
C = np.dot(A, B)
```

**JavaScript with TypedArray** (door problem):
```javascript
const doors = new Uint8Array(1000001);
// Much faster than boolean array
```

---

##  Troubleshooting

### Common Issues

**"Out of Memory"**
- Use smaller problem size
- Check system RAM
- Try compiled language (Go)

**"Very Slow Execution"**
- Run optimized version (if available)
- Try compiled language (Go)
- Check system load

**"Different Results"**
- Verify algorithm is identical
- Check data types (integer overflow?)
- Add debug output

### Docker Issues

```bash
# Remove all benchmark images
docker rmi $(docker images | grep -E 'bubble|door|matrix|prime|prisoner|factorial|fibonacci' | awk '{print $3}')

# Rebuild without cache
docker-compose build --no-cache

# Check logs
docker-compose logs -f
```

---

##  References

### Complexity Analysis
- [Big O Notation](https://en.wikipedia.org/wiki/Big_O_notation)
- [Algorithm Analysis](https://en.wikipedia.org/wiki/Analysis_of_algorithms)
- [Time Complexity](https://en.wikipedia.org/wiki/Time_complexity)

### Language Optimization
- [JIT Compilation](https://en.wikipedia.org/wiki/Just-in-time_compilation)
- [Memory Management](https://en.wikipedia.org/wiki/Memory_management)
- [Loop Unrolling](https://en.wikipedia.org/wiki/Loop_unrolling)

### Benchmarking
- [Software Performance Testing](https://en.wikipedia.org/wiki/Software_performance_testing)
- [Profiling](https://en.wikipedia.org/wiki/Profiling_(computer_programming))
- [Statistical Analysis](https://easyperf.net/blog/)

---

##  Quick Reference

### Run Each Benchmark

| Benchmark | Path | Command |
|-----------|------|---------|
| Bubble Sort | `interactive_function/bubble_sort/` | `./main` |
| Door | `interactive_function/door/` | `./main` |
| Matrix | `interactive_function/Metrix_multiplication/` | `./main` |
| Prime | `interactive_function/primeNumCount/` | `./main` |
| Prisoners | `interactive_function/prisoners/` | `./main` |
| Factorial | `Recursive_function/factorial/` | `./main` |
| Fibonacci | `Recursive_function/fibonacci/` | `./main` |

### Run Specific Language

| Language | Command |
|----------|---------|
| Python | `python3 *.py` |
| Node.js | `node *.js` |
| Go | `go run *.go` |
| PHP | `php *.php` |
| Java | `javac *.java && java ClassName` |

---

##  Next Steps

1. **Run all benchmarks** and observe results
2. **Compare performance** across languages
3. **Identify patterns** in language performance
4. **Try optimizations** for slower languages
5. **Profile code** to find bottlenecks
6. **Analyze results** and draw conclusions
7. **Document findings** in results folder

---

##  Support

For detailed information on specific benchmarks:
- See individual README.md files in each folder
- Check source code comments
- Review results in `results/` folder

---

**Last Updated**: May 18, 2025
**Status**: Active Development
**Total Benchmarks**: 7
**Languages Supported**: 5 (Python, Node.js, Go, PHP, Java)
