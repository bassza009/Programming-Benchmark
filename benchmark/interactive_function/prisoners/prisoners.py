def play_optimal(n):
    pardoned = 0
    in_drawer = [i for i in range(100)]
    seed = 42

    for _ in range(n):
        for i in range(99, 0, -1):
            seed = (seed * 1664525 + 1013904223) & 0x7FFFFFFF
            j = seed % (i + 1)
            temp = in_drawer[i]
            in_drawer[i] = in_drawer[j]
            in_drawer[j] = temp

        all_found = True
        for prisoner in range(100):
            reveal = prisoner
            found = False
            for _step in range(50):
                card = in_drawer[reveal]
                if card == prisoner:
                    found = True
                    break
                reveal = card
            if not found:
                all_found = False
                break
        if all_found:
            pardoned += 1
    return (pardoned / n) * 100.0


def main():
    n = 1000000
    print(f"Optimal play wins: {play_optimal(n):.4f}%")


if __name__ == "__main__":
    main()
