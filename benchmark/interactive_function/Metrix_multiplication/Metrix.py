def main():
    n = 1000
    a = [float(i % n) for i in range(n * n)]
    b = [float(i // n) for i in range(n * n)]
    result = [0.0] * (n * n)

    for i in range(n):
        row_offset = i * n
        for j in range(n):
            sum_val = 0.0
            for k in range(n):
                sum_val += a[row_offset + k] * b[k * n + j]
            result[row_offset + j] = sum_val

    print(f"Sample Result [0]: {result[0]:.2f}")


if __name__ == "__main__":
    main()
