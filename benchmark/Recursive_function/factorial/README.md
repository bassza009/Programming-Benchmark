# Factorial Benchmark

## 📊 Task Overview

Factorial is a recursive function benchmark that measures recursion performance, function call overhead, and stack management across different programming languages.

## 🎯 Problem Description

### The Algorithm

Factorial of n (written as n!) is the product of all positive integers less than or equal to n:

```
n! = n × (n-1) × (n-2) × ... × 2 × 1

0! = 1 (by definition)
1! = 1
2! = 2 × 1 = 2
3! = 3 × 2 × 1 = 6
4! = 4 × 3 × 2 × 1 = 24
5! = 5 × 4 × 3 × 2 × 1 = 120
...
20! = 2,432,902,008,176,640,000
```

### Recursive Definition

```
factorial(n) = 1              if n ≤ 1
factorial(n) = n × factorial(n-1)   otherwise
```

### Base Case

```
factorial(0) = 1
factorial(1) = 1
```

## 🎓 Why This Benchmark Matters

### What It Tests

1. **Recursive Call Overhead**
   - Function call performance
   - Return address management
   - Call stack operations

2. **Stack Management**
   - Stack frame allocation
   - Local variable storage
   - Stack memory usage

3. **Tail-Call Optimization**
   - Some languages optimize tail calls
   - Stack vs iteration comparison
   - Compiler capabilities

4. **Register Allocation**
   - How efficiently compilers use registers
   - Return value handling
   - Parameter passing

### Real-World Applications

- **Combinatorics**: Calculating permutations and combinations
- **Probability**: Probability calculations
- **Math Libraries**: Standard library functions
- **Teaching**: Fundamental recursion concept
- **Algorithm Complexity**: Understanding recursive time

## 📁 Project Structure

```
factorial/
├── factorial.py           # Python implementation
├── factorial.js           # Node.js implementation
├── factorial.go           # Go implementation
├── factorial.php          # PHP implementation
├── factorial.java         # Java implementation
├── Dockerfile.python      # Python container
├── Dockerfile.nodejs      # Node.js container
├── Dockerfile.go          # Go container
├── Dockerfile.php         # PHP container
├── Dockerfile.java        # Java container
├── main                   # Runner script
├── sda                    # Additional test data
└── README.md              # This file
```

## 🚀 Running the Benchmark

### Option 1: Run All Implementations

```bash
cd benchmark/Recursive_function/factorial
./main
```

### Option 2: Run Individual Language

**Python**:
```bash
python3 factorial.py
```

**Node.js**:
```bash
node factorial.js
```

**Go**:
```bash
go run factorial.go
```

**PHP**:
```bash
php factorial.php
```

**Java**:
```bash
javac factorial.java
java factorial
```

### Option 3: Docker Execution

```bash
docker build -f Dockerfile.python -t factorial-py .
docker run factorial-py
```

## 📈 Expected Results

### Typical Execution Times

Computing **factorial(30)**:

| Language | Time | Speed | Notes |
|----------|------|-------|-------|
| Go | < 1ms | 1x (fastest) | Compiled, optimal |
| Java | 1-5ms | 2-5x | JIT after warmup |
| Node.js | 2-10ms | 5-10x | V8 optimization |
| Python | 5-20ms | 10-20x | Interpretation overhead |
| PHP | 10-50ms | 20-50x | Slowest |

**Result**: 30! = 265,252,859,812,191,058,636,308,480,000,000

### Typical Results Table

| n | Result | Digits |
|---|--------|--------|
| 5 | 120 | 3 |
| 10 | 3,628,800 | 7 |
| 20 | 2,432,902,008,176,640,000 | 19 |
| 30 | 265,252,859,812,191,058,636,308,480,000,000 | 33 |

### Output Example

```
=== Factorial Benchmark ===
Computing: factorial(30)

Execution time: 0.0034 seconds
Result: 265252859812191058636308480000000

Number of recursive calls: 30
Maximum stack depth: 30
```

## 🔍 Algorithm Variants

### 1. Pure Recursion (Naive)

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

**Characteristics**:
- Simple and elegant
- Recursive call for each number
- O(n) stack depth
- Linear time O(n)

### 2. Tail-Recursive

```python
def factorial_tail(n, acc=1):
    if n <= 1:
        return acc
    return factorial_tail(n - 1, n * acc)
```

**Compiler Optimization**:
- Some languages (Go, Scheme) optimize tail calls
- Converts to loop automatically
- Constant O(1) stack depth (if optimized)
- Same time complexity but better memory

### 3. Iterative

```python
def factorial_iterative(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

**Characteristics**:
- Fastest approach (baseline)
- No recursion overhead
- O(1) stack depth
- Most efficient

### 4. Memoized

```python
cache = {}

def factorial_memo(n):
    if n in cache:
        return cache[n]
    if n <= 1:
        return 1
    result = n * factorial_memo(n - 1)
    cache[n] = result
    return result
```

**Benefits**:
- Caches previous results
- Useful if computing multiple factorials
- Same time per unique n, O(1) lookup for repeats

## 💡 Optimization Techniques

### 1. Use Iterative Over Recursive

```python
# Instead of:
def fac(n):
    if n <= 1:
        return 1
    return n * fac(n - 1)

# Use:
def fac(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

**Speedup**: 5-10x faster

### 2. Tail-Call Elimination

```go
// In Go (compiled language that optimizes tail calls)
func Factorial(n, acc int) int {
    if n <= 1 {
        return acc
    }
    return Factorial(n-1, n*acc)  // Tail call - optimized to loop
}
```

**Benefit**: Prevents stack overflow for large n

### 3. Use Math Library

```python
import math
result = math.factorial(30)  # Highly optimized!
```

**Speed**: Often 50-100x faster

### 4. Use Big Integer Libraries

```python
# For large factorials (n > 20)
from decimal import Decimal

def large_factorial(n):
    result = Decimal(1)
    for i in range(2, n + 1):
        result *= i
    return result
```

## 🧪 Variations to Test

### 1. Different Values of n

```
- 10 (very fast)
- 20 (fast)
- 30 (medium - standard)
- 40 (slow - may overflow on some)
- 50 (very slow - integer overflow likely)
```

### 2. Multiple Calls

```python
# Warm-up first to trigger JIT
for _ in range(100):
    factorial(30)
```

**Observation**: Second+ calls are faster due to JIT

### 3. Deep Recursion

```
Test how deep recursion stacks each language supports:
- Python: Typically 1,000 recursions
- Java: Higher limit
- Go: Handles very deep recursion
```

### 4. Tail vs Non-tail

Compare:
- Regular recursion
- Tail-recursive
- Iterative

## 📊 Performance Analysis

### Recursion Overhead

For factorial(30):
- 30 recursive calls needed
- Each call: function prologue, parameter passing, return
- Stack frame per call: ~20-100 bytes

**Overhead**:
- Interpreted (Python): ~100-500μs per call
- JIT (Java): ~10-50μs per call (after warmup)
- Compiled (Go): ~1-5μs per call

### Stack Usage

**Per recursive call**:
- Return address: 8 bytes
- Local variables: 8 bytes (n, result)
- Compiler overhead: 4-20 bytes
- Total per frame: ~32 bytes

**For factorial(30)**:
- 30 frames × 32 bytes = ~960 bytes
- Negligible for modern systems

**Danger zone**:
- factorial(5000) × 32 bytes = ~160 KB (usually OK)
- factorial(50000) × 32 bytes = ~1.6 MB (approaching limit)
- factorial(100000) = ~3.2 MB (likely stack overflow)

## 🎓 Learning Outcomes

This benchmark teaches:

1. **Recursion Performance**
   - Recursive call overhead
   - Stack usage impact
   - Tail-call optimization importance

2. **Function Call Mechanisms**
   - Parameter passing
   - Return value handling
   - Stack frame management

3. **Compiler Optimizations**
   - Tail-call elimination
   - JIT compilation benefits
   - Compiled vs interpreted differences

4. **Language Characteristics**
   - Go: Excellent recursion support
   - Java: Good after JIT warmup
   - Python: Higher overhead
   - PHP: No tail-call optimization

5. **Practical Optimization**
   - Iteration vs recursion trade-offs
   - When to use each approach
   - Library function benefits

## 🔧 Troubleshooting

### Issue: Stack Overflow

**For large n**:
- Use iterative version
- Increase stack size (if possible)
- Use tail-recursive version (if supported)

### Issue: Wrong Results

**Check**:
- Integer overflow (factorial grows very fast)
- Use arbitrary precision numbers (BigInteger, etc.)
- Verify base case

### Issue: Very Slow

**Solutions**:
- Use iterative approach
- Reduce n value
- Use compiled language (Go)
- Try math library functions

### Issue: Inconsistent Results

**Causes**:
- JIT warmup (Java runs slower on first call)
- Solution: Run multiple times
- System load affecting measurements

## 📚 References

- **Factorial**: https://en.wikipedia.org/wiki/Factorial
- **Recursion**: https://en.wikipedia.org/wiki/Recursion_(computer_science)
- **Tail-Call Optimization**: https://en.wikipedia.org/wiki/Tail_call
- **Big O Notation**: https://en.wikipedia.org/wiki/Big_O_notation

## 🎯 Next Steps

1. Run factorial(30) benchmark
2. Compare across languages
3. Try different n values
4. Measure JIT warmup (Java)
5. Compare recursive vs iterative
6. Test tail-call optimization (Go)
7. Try large n values (watch for overflow)

---

**Last Updated**: May 18, 2025
**Difficulty Level**: Easy
**Time to Complete**: 5-10 minutes per language
**Prerequisite Knowledge**: Recursion, function calls, mathematical operations
