import time

def main():
    n = 1000
    matrix_a = [float(i % n) for i in range(n * n)]
    matrix_b = [float(i // n) for i in range(n * n)]
    result = [0.0] * (n * n)

    print(f"Starting Matrix Multiplication (Python - Flat): {n}x{n}")
    # start = time.perf_counter()

    for i in range(n):
        for j in range(n):
            sum_val = 0.0
            for k in range(n):
                sum_val += matrix_a[i * n + k] * matrix_b[k * n + j]
            result[i * n + j] = sum_val

    # end = time.perf_counter()
    print(f"Sample Result [0]: {result[0]:.6f}")
    # print(f"Time: {end - start:.4f} sec")

if __name__ == "__main__":
    main()