# Matrix Multiplication Benchmark

## 📊 Task Overview

Matrix Multiplication is a compute-intensive benchmark that tests floating-point arithmetic performance, memory bandwidth, and compiler vectorization capabilities across different programming languages.

## 🎯 Problem Description

### The Algorithm

Matrix multiplication of two square matrices A and B to produce result matrix C:

```
C[i][j] = Σ(k=0 to n-1) A[i][k] × B[k][j]
```

The matrices can be of any dimensions, so long as the number of columns of the first matrix is equal to the number of rows of the second matrix.

### Example (3×3 matrices)

```
    [1  2  3]       [9  8  7]
A = [4  5  6]   B = [6  5  4]
    [7  8  9]       [3  2  1]

    [1*9+2*6+3*3  1*8+2*5+3*2  ...]
C = [4*9+5*6+6*3  4*8+5*5+6*2  ...]
    [7*9+8*6+9*3  7*8+8*5+9*2  ...]
```

### Time Complexity

- **Standard Algorithm**: O(n³) where n is matrix dimension
- **Example**: 500×500 = 125 million multiplications

**Note**: Faster algorithms exist (Strassen: O(n^2.807), but overhead isn't worth for small matrices)

### Space Complexity

- **Standard**: O(n²) for result matrix + input matrices
- **In-place**: Not practical for matrix multiplication

## 🎓 Why This Benchmark Matters

### What It Tests

1. **Floating-Point Operations**
   - FPU (Floating Point Unit) performance
   - Multiplication efficiency
   - Addition efficiency
   - Precision handling

2. **Memory Performance**
   - Cache efficiency (crucial!)
   - Memory bandwidth utilization
   - Access patterns
   - L1/L2/L3 cache behavior

3. **Compiler Optimizations**
   - Loop unrolling
   - Vectorization (SIMD)
   - Prefetching
   - Register allocation

4. **Data Access Patterns**
   - Row-major vs column-major
   - Cache misses
   - Memory alignment
   - Stride patterns

### Real-World Applications

- **Scientific Computing**: Linear algebra operations
- **Graphics**: 3D transformations (matrix operations)
- **Machine Learning**: Neural network computations
- **Physics Simulations**: Numerical methods
- **Cryptography**: Matrix operations for encryption

## 📁 Project Structure

```
Metrix_multiplication/
├── Metrix.py              # Python implementation
├── Metrix.js              # Node.js implementation
├── Metrix.php             # PHP implementation
├── Metrixv2.go            # Go implementation (optimized)
├── Metrix.java            # Java implementation
├── Metrixtestarray.php    # PHP test with arrays
├── Dockerfile.python      # Python container
├── Dockerfile.nodejs      # Node.js container
├── Dockerfile.go          # Go container
├── Dockerfile.php         # PHP container
├── Dockerfile.java        # Java container
├── main                   # Runner script
├── results/               # Output matrices and timing
└── README.md              # This file
```

## 🚀 Running the Benchmark

### Option 1: Run All Implementations

```bash
cd benchmark/interactive_function/Metrix_multiplication
./main
```

### Option 2: Run Individual Language

**Python**:
```bash
python3 Metrix.py
```

**Node.js**:
```bash
node Metrix.js
```

**Go**:
```bash
go run Metrixv2.go
```

**PHP**:
```bash
php Metrix.php
```

**Java**:
```bash
javac Metrix.java
java Metrix
```

### Option 3: Docker Execution

```bash
docker build -f Dockerfile.python -t matrix-py .
docker run matrix-py
```

## 📈 Expected Results

### Typical Execution Times

Multiplying **500×500 matrices**:

| Language | Time | Operations | Ops/sec |
|----------|------|------------|---------|
| Go | 200-400ms | 125M | 312-625M ops/sec |
| Java | 300-600ms | 125M | 208-417M ops/sec |
| Node.js | 500-1500ms | 125M | 83-250M ops/sec |
| Python | 1-3 seconds | 125M | 42-125M ops/sec |
| PHP | 5-15 seconds | 125M | 8-25M ops/sec |

**Factors**:
- Matrix size (larger = more computation)
- CPU speed
- Cache architecture
- Compiler optimization
- System load

### Output Example

```
=== Matrix Multiplication Benchmark ===
Matrix size: 500x500
Memory per matrix: 1.0 MB

Multiplying matrices...
Time: 0.325 seconds
Result matrix created successfully
Sample result[0][0]: 1234567.89
```

## 🔍 Algorithm Variants

### 1. Standard Triple-Nested Loop

```python
def matrix_multiply(A, B, n):
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C
```

**Characteristics**:
- Simple and clear
- Poor cache locality (B accessed in column order)
- Time: O(n³)

### 2. Transposed B Matrix

```python
def matrix_multiply_transpose(A, B, n):
    BT = transpose(B)  # Transpose B once
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * BT[j][k]
    return C
```

**Benefits**:
- Better cache locality
- Faster memory access (sequential reads)
- 2-10x faster than standard

### 3. Cache-Oblivious (Divide & Conquer)

```python
def matrix_multiply_recursive(A, B, n):
    if n <= 64:  # Base case: small matrix
        return matrix_multiply(A, B, n)
    
    # Divide matrices into quadrants
    # Recursively multiply sub-matrices
    # Combine results
```

**Benefits**:
- Optimal cache behavior
- Works for any cache size
- Still O(n³) but with better constants

### 4. Using Libraries

```python
import numpy as np
C = np.dot(A, B)  # Highly optimized!
```

**Speed**: Often 10-100x faster using BLAS (Basic Linear Algebra Subprograms)

## 💡 Optimization Techniques

### 1. Loop Ordering

Different loop orders have different performance:

```python
# Version 1: ijk (poor cache for B)
for i in range(n):
    for j in range(n):
        for k in range(n):
            C[i][j] += A[i][k] * B[k][j]

# Version 2: kij (better for B)
for k in range(n):
    for i in range(n):
        for j in range(n):
            C[i][j] += A[i][k] * B[k][j]

# Version 3: jki (optimized)
for j in range(n):
    for k in range(n):
        for i in range(n):
            C[i][j] += A[i][k] * B[k][j]
```

### 2. Block Matrix Multiplication

Process matrices in cache-friendly blocks:

```python
def matrix_multiply_blocked(A, B, n, block_size):
    C = [[0] * n for _ in range(n)]
    
    for i0 in range(0, n, block_size):
        for j0 in range(0, n, block_size):
            for k0 in range(0, n, block_size):
                # Multiply blocks
                for i in range(i0, min(i0 + block_size, n)):
                    for j in range(j0, min(j0 + block_size, n)):
                        for k in range(k0, min(k0 + block_size, n)):
                            C[i][j] += A[i][k] * B[k][j]
    return C
```

**Optimal block size**: Usually matches CPU cache line size (typically 64 bytes)

### 3. SIMD Vectorization

Use vector instructions (if compiler supports):

```c
// C code with SIMD hints
for (int i = 0; i < n; i += 4) {
    __m256 sum = _mm256_setzero_ps();
    for (int k = 0; k < n; k++) {
        sum = _mm256_fmadd_ps(_mm256_set1_ps(A[i][k]), 
                              _mm256_loadu_ps(&B[k][j]), sum);
    }
    _mm256_storeu_ps(&C[i][j], sum);
}
```

**Impact**: 4-8x faster with proper SIMD

### 4. NumPy (Python)

```python
import numpy as np

# Convert lists to numpy arrays
A_np = np.array(A, dtype=np.float32)
B_np = np.array(B, dtype=np.float32)

# Use optimized BLAS
C_np = np.dot(A_np, B_np)

# Back to Python list if needed
C = C_np.tolist()
```

**Speedup**: 50-100x faster!

## 🧪 Variations to Test

### 1. Different Matrix Sizes

```
- 100×100 = 1 million operations (very fast)
- 300×300 = 27 million operations
- 500×500 = 125 million operations (standard)
- 1000×1000 = 1 billion operations (slow)
- 2000×2000 = 8 billion operations (very slow)
```

### 2. Different Data Types

```
- float32 (faster, less precision)
- float64 (standard precision)
- integer (typically slower)
```

### 3. Non-Square Matrices

```
- Rectangular: 500×1000 × 1000×500
- Tall: 100×1000 × 1000×100
- Wide: 1000×100 × 100×1000
```

## 📊 Performance Analysis

### Memory Bandwidth Impact

**500×500 float32 matrices**:
- Data: 3 × 500² × 4 bytes = 3 MB
- Operations: 500³ = 125 million
- Ratio: ~24,000 operations per byte
- **Result**: Cache miss latency is minimal

### Cache Behavior

Typical cache performance:
- L1 cache: 32 KB (holds ~2000 floats)
- L2 cache: 256 KB (holds ~16,000 floats)
- L3 cache: 8 MB (holds ~500,000 floats)
- Main memory: > 1 ns access penalty

### Metrics to Track

1. **Execution Time**: Wall clock time
2. **Floating-Point Operations**: 2 per multiply + accumulate
3. **Throughput**: Operations per second
4. **Cache Misses**: L1, L2, L3 miss rates
5. **Memory Bandwidth**: Gigabytes per second used

## 🎓 Learning Outcomes

This benchmark teaches:

1. **Floating-Point Arithmetic**
   - FPU performance
   - Precision considerations
   - Numerical stability

2. **Cache Optimization**
   - Access patterns matter
   - Cache locality importance
   - Block algorithms

3. **Compiler Capabilities**
   - Optimization effectiveness
   - Vectorization support
   - Loop transformations

4. **Algorithm Variants**
   - Different approaches
   - Trade-offs
   - Optimization techniques

5. **Practical Performance**
   - Real-world speedups
   - Library usage benefits
   - Hardware limitations

## 🔧 Troubleshooting

### Issue: Out of Memory

**Solutions**:
- Use smaller matrices (100×100)
- Check available RAM
- Use sparse matrix format

### Issue: Wrong Results

**Check**:
- Float precision (rounding errors)
- Algorithm implementation
- Matrix dimensions

### Issue: Very Different Performance

**Possible Causes**:
- CPU frequency scaling
- Thermal throttling
- System background load
- Compiler optimization flags

## 📚 References

- **Matrix Multiplication**: https://en.wikipedia.org/wiki/Matrix_multiplication
- **BLAS**: https://en.wikipedia.org/wiki/Basic_Linear_Algebra_Subprograms
- **Cache Optimization**: https://en.wikipedia.org/wiki/CPU_cache
- **Strassen Algorithm**: https://en.wikipedia.org/wiki/Strassen_algorithm

## 🎯 Next Steps

1. Run benchmark with 500×500 matrices
2. Compare across languages
3. Try different matrix sizes
4. Profile memory and cache usage
5. Try optimized implementations
6. Measure SIMD impact (if available)
7. Explore library functions (NumPy, etc.)

---

**Last Updated**: May 18, 2025
**Difficulty Level**: Medium
**Time to Complete**: 10-20 minutes per language
**Prerequisite Knowledge**: Matrix math, nested loops, floating-point arithmetic
