# Bubble Sort Benchmark

##  Task Overview

Bubble Sort is a fundamental sorting algorithm used to benchmark basic algorithmic performance, loop efficiency, and comparison operations across different programming languages.

##  Problem Description

### The Algorithm

Bubble Sort repeatedly steps through a list, compares adjacent elements, and swaps them if they're in the wrong order. This process continues until the list is sorted.

**Algorithm Steps**:
1. Compare the first two elements
2. If first > second, swap them
3. Move to the next pair
4. Repeat until end of list
5. Do another complete pass if any swaps were made
6. Stop when no swaps occur in a complete pass

### Pseudocode

```
procedure bubbleSort(A : list of sortable items)
    n := length(A)
    repeat
        swapped := false
        for i := 1 to n - 1 do
            if A[i] > A[i + 1] then
                swap(A[i], A[i + 1])
                swapped := true
            end if
        end for
        n := n - 1
    until not swapped
end procedure
```

### Time Complexity

- **Best Case**: O(n) - Already sorted array, single pass
- **Average Case**: O(n²) - Random array
- **Worst Case**: O(n²) - Reverse sorted array

**Space Complexity**: O(1) - Sorts in place, minimal extra memory

##  Why This Benchmark Matters

### What It Tests

1. **Basic Loop Performance**
   - Nested loop efficiency
   - Loop iteration overhead
   - Iterator optimization

2. **Comparison Operations**
   - How fast languages compare values
   - Branch prediction impact
   - Conditional logic performance

3. **Array Access**
   - Array indexing speed
   - Cache efficiency
   - Memory access patterns

4. **Element Swapping**
   - Variable assignment speed
   - Temporary storage requirements
   - Language-specific swap efficiency

### Real-World Relevance

- **Teaching Tool**: Foundation for learning sorting algorithms
- **Small Datasets**: Still used for very small arrays in production
- **Comparison Baseline**: Reference for comparing language performance
- **Cache Analysis**: Shows memory access patterns
- **Education**: Teaching algorithm analysis and Big O notation

##  Project Structure

```
bubble_sort/
├── bubble.py              # Python implementation
├── bubble.js              # Node.js implementation
├── bubble.go              # Go implementation
├── bubble.php             # PHP implementation
├── bubble.java            # Java implementation
├── Dockerfile.python      # Python container
├── Dockerfile.nodejs      # Node.js container
├── Dockerfile.go          # Go container
├── Dockerfile.php         # PHP container
├── Dockerfile.java        # Java container
├── main                   # Runner script (all languages)
└── README.md              # This file
```

##  Running the Benchmark

### Option 1: Run All Implementations

```bash
cd benchmark/interactive_function/bubble_sort
./main
```

### Option 2: Run Individual Language

**Python**:
```bash
python3 bubble.py
```

**Node.js**:
```bash
node bubble.js
```

**Go**:
```bash
go run bubble.go
```

**PHP**:
```bash
php bubble.php
```

**Java**:
```bash
javac bubble.java
java bubble
```

### Option 3: Docker Execution

```bash
# Build
docker build -f Dockerfile.python -t bubble-py .

# Run
docker run bubble-py
```

##  Expected Results

### Typical Sorting Times

Sorting **10,000 random elements**:

| Language | Time | Relative Speed |
|----------|------|-----------------|
| Go | 10-20ms | 1x (fastest) |
| Java | 20-40ms | 2-4x |
| Node.js | 30-80ms | 3-8x |
| Python | 100-300ms | 10-30x |
| PHP | 200-500ms | 20-50x |

**Factors affecting results**:
- CPU speed
- Memory bandwidth
- JIT compilation (Java first run slower)
- Optimization flags
- System load

### Output Example

```
=== Bubble Sort Benchmark ===
Array size: 10000
Initial array: [random values]

Sorting...
Time: 0.0234 seconds

Sorted successfully: [1, 2, 3, 4, 5, ...]
```

##  Algorithm Analysis

### Passes Through Array

For an array of size n:
- **Best case**: 1 pass (already sorted)
- **Worst case**: n passes (reverse sorted)

### Comparisons Made

- **Total comparisons**: ~n²/2 on average
- **10,000 elements**: ~50 million comparisons
- **1,000,000 elements**: 500 billion comparisons (very slow!)

### Memory Usage

- **Extra space**: O(1) - only swap variable needed
- **In-place sorting**: Yes
- **Stable sort**: Yes (equal elements maintain order)

##  Optimization Techniques

### 1. Early Termination

Stop if no swaps occurred in a pass:

```python
def bubble_sort_optimized(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:  # Exit early if sorted
            break
    return arr
```

### 2. Reduce Comparisons

Track the position of last swap:

```python
def bubble_sort_optimized2(arr):
    n = len(arr)
    while n > 1:
        new_n = 0
        for i in range(n - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                new_n = i + 1
        n = new_n
    return arr
```

### 3. Language-Specific Optimizations

**Python - Use sorted()**:
```python
# Don't implement bubble sort - use built-in
arr = sorted(arr)
```

**JavaScript - Array methods**:
```javascript
arr.sort((a, b) => a - b);
```

**Go - sort package**:
```go
sort.Ints(arr)
```

##  Variations to Test

### 1. Different Array Sizes

```
- 100 elements (very fast)
- 1,000 elements (fast)
- 10,000 elements (medium)
- 100,000 elements (slow)
- 1,000,000 elements (very slow)
```

### 2. Different Data Types

- Random numbers
- Already sorted
- Reverse sorted
- Nearly sorted (almost done)
- Duplicates

### 3. Different Input Distributions

```
- Uniform random [0, 1000]
- Normal distribution
- Exponential distribution
- Small range duplicates
```

##  Performance Analysis

### Metrics to Measure

1. **Execution Time**
   - Wall clock time
   - CPU time
   - Time per comparison

2. **Memory Usage**
   - Peak memory
   - Cache misses
   - Memory bandwidth

3. **Efficiency**
   - Time per element
   - Comparisons per second
   - Actual operations vs theoretical

### Profiling Commands

**Time measurement**:
```bash
time python3 bubble.py
```

**Memory profiling (Python)**:
```bash
python3 -m memory_profiler bubble.py
```

**CPU profiling (Python)**:
```bash
python3 -m cProfile bubble.py
```

##  Learning Outcomes

This benchmark teaches:

1. **Algorithm Analysis**
   - Quadratic time complexity (O(n²))
   - Comparison operations
   - Pass structure

2. **Language Performance**
   - Loop efficiency differences
   - Compiler optimizations
   - Interpretation overhead

3. **Optimization Strategies**
   - Early termination
   - Algorithm variants
   - Built-in function usage

4. **Performance Measurement**
   - Timing tools
   - Profiling techniques
   - Statistical analysis

##  Troubleshooting

### Issue: Array Not Sorted Correctly

**Check**:
- Comparison operator (> vs <)
- Swap logic
- Loop bounds

### Issue: Very Slow Execution

**Solutions**:
- Use smaller array
- Use faster language (Go)
- Try optimized variant
- Check system load

### Issue: Different Results

**Check**:
- Integer overflow
- Floating-point precision
- Random seed (for reproducibility)
- Stability of sort

##  References

- **Bubble Sort**: https://en.wikipedia.org/wiki/Bubble_sort
- **Sorting Algorithms**: https://en.wikipedia.org/wiki/Sorting_algorithm
- **Comparison Sort**: https://en.wikipedia.org/wiki/Comparison_sort
- **Big O Notation**: https://en.wikipedia.org/wiki/Big_O_notation

##  Next Steps

1. Run the benchmark with default size
2. Measure execution time
3. Try different array sizes
4. Compare across languages
5. Try optimization techniques
6. Analyze the results
7. Read about better sorting algorithms (Quick Sort, Merge Sort)

---

**Last Updated**: May 18, 2025
**Difficulty Level**: Easy
**Time to Complete**: 5-10 minutes per language
**Prerequisite Knowledge**: Basic loops, arrays, comparisons
