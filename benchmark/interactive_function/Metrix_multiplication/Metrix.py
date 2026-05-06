import math

def main():
    n = 1000
    a = [0.0] * (n * n)
    b = [0.0] * (n * n)
    res = [0.0] * (n * n)

    for i in range(n * n):
        a[i] = float(i % n)
        b[i] = float(i // n)

    print(f"Starting Matrix Multiplication (Python): {n}x{n}")

    for i in range(n):
        for j in range(n):
            sum_val = 0.0
            for k in range(n):
                sum_val += a[i * n + k] * b[k * n + j]
            res[i * n + j] = sum_val

    print(f"Sample Result [0]: {res[0]:.6f}")

if __name__ == "__main__":
    main()