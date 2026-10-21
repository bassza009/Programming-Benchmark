import sys

sys.setrecursionlimit(2000)


def factorial(n):
    if n <= 1:
        return 1.0
    return float(n) * factorial(n - 1)


def main():
    n = 100
    print(f"{factorial(n):.6e}")


if __name__ == "__main__":
    main()
