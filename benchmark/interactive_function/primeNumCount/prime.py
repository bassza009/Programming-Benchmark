def count_primes(limit):
    count = 0
    for i in range(2, limit + 1):
        is_prime = True
        j = 2
        while j * j <= i:
            if i % j == 0:
                is_prime = False
                break
            j += 1
        if is_prime:
            count += 1
    return count


def main():
    n = 1000000
    result = count_primes(n)
    print(f"Primes count: {result}")


if __name__ == "__main__":
    main()
