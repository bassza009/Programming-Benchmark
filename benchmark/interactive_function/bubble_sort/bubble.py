def main():
    n = 10000
    arr = [n - i for i in range(n)]

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp

    print(f"Sample Result [0]: {arr[0]}, [{n - 1}]: {arr[n - 1]}")


if __name__ == "__main__":
    main()
