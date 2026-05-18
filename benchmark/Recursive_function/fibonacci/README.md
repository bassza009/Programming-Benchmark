# Fibonacci Benchmark

## 📊 Task Overview

Fibonacci is a recursive algorithm benchmark that demonstrates exponential time complexity (O(2^n)) and the dramatic importance of optimization through memoization, dynamic programming, and algorithmic improvements.

## 🎯 Problem Description

### The Sequence

The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones:

```
F(0) = 0
F(1) = 1
F(2) = 1
F(3) = 2
F(4) = 3
F(5) = 5
F(6) = 8
F(7) = 13
F(8) = 21
F(9) = 34
F(10) = 55
...
```

### Mathematical Definition

```
F(n) = 0                    if n = 0
F(n) = 1                    if n = 1
F(n) = F(n-1) + F(n-2)     otherwise
```

### Real-World Occurrences

- Flower petals and seed spirals
- Spiral galaxies
- DNA molecule dimensions
- Stock market patterns
- Evolutionary trees

## 🎓 Why This Benchmark Matters

### What It Tests

1. **Exponential Algorithm Performance**
   - Demonstrates O(2^n) complexity in practice
   - Shows why optimization matters
   - Reveals language performance under load

2. **Recursion Efficiency**
   - Recursive call overhead
   - Stack usage
   - Function call throughput

3. **Memoization Benefits**
   - Cache effectiveness
   - Optimization impact (50-1000x faster!)
   - Memory vs computation trade-offs

4. **Dynamic Programming**
   - Building solutions bottom-up
   - State space reduction
   - Optimal substructure

### Real-World Applications

- **Time Complexity Analysis**: Teaching algorithm analysis
- **Optimization**: Demonstrating need for optimization
- **Dynamic Programming**: Classic DP example
- **Memoization**: Practical caching techniques
- **Algorithm Selection**: When to use which approach

## 📁 Project Structure

```
fibonacci/
├── fibonacci.py           # Python implementation
├── fibonacci.js           # Node.js implementation
├── fibonacci.go           # Go implementation
├── fibonacci.php          # PHP implementation
├── fibonacci.java         # Java implementation
├── Dockerfile.python      # Python container
├── Dockerfile.nodejs      # Node.js container
├── Dockerfile.go          # Go container
├── Dockerfile.php         # PHP container
├── Dockerfile.java        # Java container
├── main                   # Runner script
└── README.md              # This file
```

## 🚀 Running the Benchmark

### Option 1: Run All Implementations

```bash
cd benchmark/Recursive_function/fibonacci
./main
```

### Option 2: Run Individual Language

**Python**:
```bash
python3 fibonacci.py
```

**Node.js**:
```bash
node fibonacci.js
```

**Go**:
```bash
go run fibonacci.go
```

**PHP**:
```bash
php fibonacci.php
```

**Java**:
```bash
javac fibonacci.java
java fibonacci
```

### Option 3: Docker Execution

```bash
docker build -f Dockerfile.python -t fib-py .
docker run fib-py
```

## ⚠️ Warning: VERY SLOW!

**DO NOT run naive fibonacci for n > 40!**

Typical times for naive recursive algorithm:
- fib(35): 5-10 seconds
- fib(40): 1-5 minutes
- fib(45): Hours
- fib(50): Days or more!

## 📈 Expected Results

### Typical Execution Times (Naive Recursion)

Computing **fibonacci(35)**:

| Language | Time | Result | Notes |
|----------|------|--------|-------|
| Go | 100-500ms | 9,227,465 | Compiled |
| Java | 200-1000ms | 9,227,465 | JIT after warmup |
| Node.js | 500-2000ms | 9,227,465 | V8 engine |
| Python | 1-5 seconds | 9,227,465 | Interpreted |
| PHP | 5-15 seconds | 9,227,465 | Slowest |

**Result**: fib(35) = 9,227,465

### Complexity Explosion

| n | Recursive Calls | Time (Go) | Time (Python) |
|---|---|---|---|
| 20 | 21,891 | 1ms | 10ms |
| 30 | 2,178,309 | 10ms | 1s |
| 35 | 29,860,703 | 200ms | 15s |
| 40 | 401,537,335 | 3s | 3m |
| 45 | 1,836,311,903 | 20s | 20m |

**Observation**: Calls grow exponentially - doubling n roughly squares the time!

### Output Example

```
=== Fibonacci Benchmark ===
Computing: fibonacci(35)

Method: Naive Recursion
Result: 9227465
Execution time: 0.2345 seconds
Number of function calls: 29,860,703
Calls per second: 123.4M calls/sec
```

## 🔍 Algorithm Variants

### 1. Naive Recursion (SLOW!)

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

**Characteristics**:
- **Terrible time complexity: O(2^n)**
- Much repeated calculation
- Simple to understand
- Perfect for demonstrating why optimization matters

**Recursion tree for fib(5)**:
```
                  fib(5)
                 /      \
            fib(4)        fib(3)
           /      \       /      \
        fib(3)   fib(2) fib(2)  fib(1)
        /    \    /   \   /   \
    fib(2) fib(1) fib(1) fib(0) fib(1) fib(0)
    /    \
fib(1)  fib(0)

Note: fib(3) calculated twice, fib(2) three times!
```

### 2. Memoization (Fast!)

```python
cache = {}

def fibonacci_memo(n):
    if n in cache:
        return cache[n]
    if n <= 1:
        return n
    result = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    cache[n] = result
    return result
```

**Characteristics**:
- **Linear time complexity: O(n)**
- Each value calculated once and cached
- Much faster - 1000x+ speedup!
- Still recursive but with cache

**Performance**: fib(35) < 1ms!

### 3. Dynamic Programming (Fastest!)

```python
def fibonacci_dp(n):
    if n <= 1:
        return n
    
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr
```

**Characteristics**:
- **Linear time complexity: O(n)**
- **Constant space complexity: O(1)**
- No recursion - pure iteration
- Fastest approach for this problem

**Performance**: fib(35) < 0.1ms!

### 4. Mathematical Formula (Matrix Exponentiation)

```python
def fibonacci_matrix(n):
    def matrix_mult(A, B):
        return [
            [A[0][0]*B[0][0] + A[0][1]*B[1][0], 
             A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0],
             A[1][0]*B[0][1] + A[1][1]*B[1][1]]
        ]
    
    def matrix_pow(M, p):
        if p == 1:
            return M
        if p % 2 == 0:
            half = matrix_pow(M, p // 2)
            return matrix_mult(half, half)
        return matrix_mult(M, matrix_pow(M, p - 1))
    
    if n == 0:
        return 0
    
    M = [[1, 1], [1, 0]]
    result = matrix_pow(M, n)
    return result[0][1]
```

**Characteristics**:
- **Logarithmic time complexity: O(log n)**
- Fastest for very large n
- More complex to implement
- Uses mathematical property of Fibonacci

**Performance**: fib(1,000,000) possible (but needs big integers)!

## 💡 Comparison of Approaches

### Performance Comparison

Computing **fibonacci(35)**:

| Approach | Time | Relative | Notes |
|----------|------|----------|-------|
| Iterative DP | 0.001ms | 1x | Fastest |
| Memoization | 0.01ms | 10x | Fast, recursive |
| Naive (Go) | 200ms | 200,000x | Very slow |
| Naive (Python) | 3000ms | 3,000,000x | Extremely slow |

### Speed-up Summary

```
Optimization      Speedup
Memoization       1000x - 10,000x
DP (iterative)    10,000x - 100,000x
Matrix method     100,000x+ (for very large n)
```

## 🧪 Variations to Test

### 1. Different n Values

```
- fib(20): Very fast (< 1ms)
- fib(30): Fast (10-100ms naive)
- fib(35): Medium (seconds naive) ⚠️ Default
- fib(40): Slow (minutes naive) ⚠️ Don't try naive!
- fib(100): Very large number (use DP)
```

### 2. Different Approaches

Compare in same language:
- Naive recursion
- Memoization
- Dynamic programming
- Matrix method

### 3. Large n Values

```python
# With DP or matrix method (not naive!)
fib_100 = 354,224,848,179,261,915,075
fib_1000 = (huge number with 209 digits)
fib_1000000 = (number with ~209,000 digits!)
```

### 4. Multiple Runs

```python
# Warm up (especially for JIT)
for _ in range(10):
    fibonacci(35)
```

## 📊 Performance Analysis

### Recursion Call Count

**For naive fibonacci(n)**:

```
fib(n) requires approximately 2^n function calls

f(5) = 15 calls
f(10) = 177 calls
f(20) = 21,891 calls
f(30) = 2,178,309 calls
f(35) = 29,860,703 calls
f(40) = 401,537,335 calls
```

### Time Complexity Explained

**Naive**: O(2^n)
- Each call spawns 2 more calls
- Exponential growth
- Doubles roughly every +3 in n

**Memoization**: O(n)
- Each unique value computed once
- 35 values to compute = 35 iterations

**DP**: O(n)
- Iterative, no recursion overhead
- Usually faster than memoization

**Matrix**: O(log n)
- Binary exponentiation
- Fastest for very large n

## 🎓 Learning Outcomes

This benchmark teaches:

1. **Time Complexity Impact**
   - O(2^n) is **very slow**
   - Dramatic difference between 2^n and n
   - Importance of algorithm choice

2. **Optimization Techniques**
   - Memoization: 1000x speedup
   - DP: 10,000x speedup
   - Shows why optimization matters

3. **Recursion Overhead**
   - Naive recursion is expensive
   - Stack usage grows exponentially
   - Iteration often better

4. **Algorithm Design**
   - Different approaches to same problem
   - Trade-offs between complexity and implementation
   - Mathematical insights (matrix method)

5. **Practical Performance**
   - Computer science fundamentals matter
   - Algorithm choice > language choice
   - Proper implementation essential

## 🔧 Troubleshooting

### Issue: Naive Recursion Too Slow

**Solutions**:
- Use smaller n (20 or 25)
- Use memoized or DP version
- Use compiled language (Go)
- Be patient (n=35 takes minutes)

### Issue: Stack Overflow (for very large n)

**Causes**:
- Naive recursion goes too deep
- Solution: Use DP (iterative) instead

### Issue: Results Don't Match

**Check**:
- Base cases (fib(0)=0, fib(1)=1)
- Integer overflow for large n
- Different n values

## 📚 References

- **Fibonacci**: https://en.wikipedia.org/wiki/Fibonacci_number
- **Time Complexity**: https://en.wikipedia.org/wiki/Time_complexity
- **Memoization**: https://en.wikipedia.org/wiki/Memoization
- **Dynamic Programming**: https://en.wikipedia.org/wiki/Dynamic_programming

## 🎯 Next Steps

1. Run fib(35) with naive approach - observe slowness
2. Compare with memoized version - huge speedup!
3. Try DP approach - fastest
4. Measure execution times precisely
5. Try different n values
6. Implement matrix method
7. Reflect on algorithm importance

---

**Last Updated**: May 18, 2025
**Difficulty Level**: Medium
**Time to Complete**: 10-30 minutes per language
**Prerequisite Knowledge**: Recursion, algorithm complexity, optimization
**⚠️ WARNING**: Naive fibonacci(40+) takes extremely long!
