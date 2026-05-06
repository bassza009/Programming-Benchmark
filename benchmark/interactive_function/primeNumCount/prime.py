def count_primes(limit):
    count = 0
    for i in range(2, limit + 1):
        is_prime = True
        for j in range(2, int(i ** 0.5) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count

# ทดสอบที่ 200,000 เพื่อให้เห็นความต่างของเวลา
print(f"Primes count: {count_primes(10000000)}")