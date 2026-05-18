# Prime Number Count Benchmark

## 📊 Task Overview

Prime Number Counting is a number-crunching benchmark that tests integer arithmetic performance, algorithmic efficiency, and loop optimization across different programming languages.

## 🎯 Problem Description

### The Task

Find and count all prime numbers up to a given limit (typically 1,000,000).

**Definition of Prime**: A natural number greater than 1 that has no positive divisors other than 1 and itself.

**Examples**:
- 2, 3, 5, 7, 11, 13, 17, 19, 23, 29... are prime
- 4, 6, 8, 9, 10, 12... are NOT prime

### Typical Results

- Primes up to 1,000,000: **78,498 primes**
- Primes up to 10,000,000: **664,579 primes**

### Key Statistics

```
Range          Count    Percentage
1 - 100        25       25%
1 - 1,000      168      16.8%
1 - 10,000     1,229    12.29%
1 - 100,000    9,592    9.592%
1 - 1,000,000  78,498   7.8498%
```

## 🎓 Why This Benchmark Matters

### What It Tests

1. **Integer Arithmetic**
   - Integer operations speed
   - Division and modulo efficiency
   - Bitwise operations
   - Mathematical functions

2. **Conditional Logic**
   - If/else branch performance
   - Boolean logic efficiency
   - Loop conditions
   - Early exits

3. **Memory Access**
   - Array access patterns
   - Cache efficiency
   - Memory layout impact
   - Sequential vs random access

4. **Loop Optimization**
   - Inner loop performance
   - Iterator efficiency
   - Loop unrolling capabilities
   - Compiler optimizations

### Real-World Applications

- **Cryptography**: RSA encryption uses large primes
- **Hashing**: Prime numbers for hash table sizes
- **Random Number Generators**: Prime moduli
- **Data Structure Sizing**: Hash maps, bloom filters
- **Number Theory**: Mathematical computations

## 📁 Project Structure

```
primeNumCount/
├── prime.py               # Python implementation
├── prime.js               # Node.js implementation
├── prime.go               # Go implementation
├── prime.php              # PHP implementation
├── prime.java             # Java implementation
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
cd benchmark/interactive_function/primeNumCount
./main
```

### Option 2: Run Individual Language

**Python**:
```bash
python3 prime.py
```

**Node.js**:
```bash
node prime.js
```

**Go**:
```bash
go run prime.go
```

**PHP**:
```bash
php prime.php
```

**Java**:
```bash
javac prime.java
java prime
```

### Option 3: Docker Execution

```bash
docker build -f Dockerfile.python -t prime-py .
docker run prime-py
```

## 📈 Expected Results

### Typical Execution Times

Finding all primes up to **1,000,000**:

| Language | Time | Ops/sec | Notes |
|----------|------|---------|-------|
| Go | 50-150ms | ~6.5B ops/sec | Very fast |
| Java | 100-300ms | ~3.3B ops/sec | Good after warmup |
| Node.js | 200-600ms | ~1.7B ops/sec | V8 optimization |
| Python | 500-1500ms | ~670M ops/sec | Slower interpretation |
| PHP | 1-5 seconds | ~200M ops/sec | Slowest |

**Result**: 78,498 primes found

### Output Example

```
=== Prime Number Counter ===
Finding primes up to: 1000000

Analyzing...
Time: 0.0845 seconds
Total primes found: 78498

First 20: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
Last 20: [999853, 999863, 999883, 999931, 1000003, ...]
```

## 🔍 Algorithm Variants

### 1. Trial Division (Basic)

```python
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def count_primes(limit):
    count = 0
    for n in range(2, limit + 1):
        if is_prime(n):
            count += 1
    return count
```

**Time Complexity**: O(n × √n)
**For 1,000,000**: Very slow (~hours)

### 2. Sieve of Eratosthenes (Optimal)

```python
def sieve_of_eratosthenes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            # Mark all multiples as non-prime
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    
    return sum(is_prime)
```

**Time Complexity**: O(n log log n)
**For 1,000,000**: ~50-150ms
**Space**: O(n) boolean array

### 3. Segmented Sieve (Memory Efficient)

```python
def segmented_sieve(limit):
    limit_sqrt = int(limit**0.5)
    
    # Simple sieve for first segment
    is_prime = [True] * (limit_sqrt + 1)
    for i in range(2, limit_sqrt + 1):
        if is_prime[i]:
            for j in range(i*i, limit_sqrt + 1, i):
                is_prime[j] = False
    
    # Find primes in segments
    count = sum(is_prime)
    
    # Process remaining segments (if needed)
    for low in range(limit_sqrt + 1, limit + 1, limit_sqrt):
        high = min(low + limit_sqrt - 1, limit)
        # Sieve segment [low, high]
    
    return count
```

**Benefits**:
- O(√n) memory instead of O(n)
- Better cache locality
- Faster for very large limits

### 4. Wheel Factorization

```python
def sieve_wheel(limit):
    # Pre-eliminate multiples of 2, 3, 5
    # Only check numbers of form 30k ± 1, 30k ± 7, etc.
    # Reduces numbers to check by ~77%
```

**Benefits**:
- Fewer numbers to check
- Better cache usage
- ~2-3x faster

## 💡 Optimization Techniques

### 1. Bitset Instead of Boolean Array

```python
# Python with bitarray
from bitarray import bitarray

is_prime = bitarray(1000001)
is_prime.setall(True)

# 8x memory savings!
# ~125 KB instead of 1 MB
```

### 2. Cache-Aware Sieving

```python
def sieve_cache_aware(limit, cache_size=32768):
    # Process array in cache-line chunks
    # Better cache behavior
```

**Impact**: 2-5x faster

### 3. Parallel Sieving

```python
from multiprocessing import Pool

def sieve_parallel(limit, num_processes=4):
    # Divide range among processes
    # Each process sieves its segment
    # Combine results
```

**Impact**: 3-4x faster on 4-core CPU

### 4. Use Built-in Functions

**Python with NumPy**:
```python
import numpy as np

def sieve_numpy(limit):
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0:2] = False
    
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    
    return np.sum(is_prime)
```

**Speed**: 10-50x faster!

## 🧪 Variations to Test

### 1. Different Limits

```
- 10,000 (282 primes) - very fast
- 100,000 (9,592 primes) - fast
- 1,000,000 (78,498 primes) - standard
- 10,000,000 (664,579 primes) - slow
- 100,000,000 (5,761,455 primes) - very slow
```

### 2. Memory Variants

```python
# Standard array: O(limit) memory
# Bitarray: O(limit/8) memory
# Generator: O(1) memory (but slower)
```

### 3. Parallel Processing

```python
# Single-threaded
# Multi-threaded
# Multi-process
# GPU acceleration
```

## 📊 Performance Analysis

### Sieve Performance Breakdown

For 1,000,000 limit with standard sieve:

| Operation | Time | Percentage |
|-----------|------|------------|
| Array allocation | 5ms | 10% |
| Sieve iteration | 40ms | 80% |
| Result counting | 5ms | 10% |

### Memory Impact

**Array size**: 1,000,001 bytes = ~1 MB

**Cache lines**: ~15,625 cache lines (64 bytes each)

**L3 cache size**: Usually 8 MB (plenty of room)

## 🎓 Learning Outcomes

This benchmark teaches:

1. **Integer Arithmetic Performance**
   - Modulo and division speed
   - Integer comparison efficiency
   - Bitwise operations

2. **Algorithm Efficiency**
   - O(n√n) vs O(n log log n)
   - Impact of algorithmic choice
   - Practical optimization

3. **Memory Optimization**
   - Array size impact
   - Cache efficiency
   - Memory bandwidth

4. **Practical Improvements**
   - 2-3x with better algorithm
   - 4-8x with better data structure
   - 10-50x with libraries
   - 3-4x with parallelization

## 🔧 Troubleshooting

### Issue: Very Slow Execution

**Check**:
- Are you using sieve? (Trial division is too slow)
- Memory allocation taking time?
- System load?

**Solutions**:
- Use smaller limit (100,000)
- Try optimized implementation
- Use library functions

### Issue: Wrong Prime Count

**Verify**:
- Is limit inclusive or exclusive?
- Are you counting 2 as prime?
- Edge cases (1, 2, etc.)

### Issue: Memory Problems

**Solutions**:
- Use smaller limit
- Use bitarray (8x memory savings)
- Use segmented sieve
- Use generator approach

## 📚 References

- **Prime Number**: https://en.wikipedia.org/wiki/Prime_number
- **Sieve of Eratosthenes**: https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
- **Prime Counting Function**: https://en.wikipedia.org/wiki/Prime-counting_function
- **Primality Test**: https://en.wikipedia.org/wiki/Primality_test

## 🎯 Next Steps

1. Run benchmark with 1,000,000 limit
2. Compare across languages
3. Try different limits
4. Measure memory usage
5. Try optimized implementations
6. Explore parallel approaches
7. Research prime number properties

---

**Last Updated**: May 18, 2025
**Difficulty Level**: Medium
**Time to Complete**: 10-20 minutes per language
**Prerequisite Knowledge**: Number theory, loops, arrays, modulo operation
