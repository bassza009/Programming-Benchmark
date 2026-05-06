import random

def play_optimal(n):
    pardoned = 0
    in_drawer = list(range(100))
    for _ in range(n):
        random.shuffle(in_drawer)
        all_found = True
        for prisoner in range(100):
            reveal = prisoner
            found = False
            for _go in range(50):
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
    return (pardoned / n) * 100

if __name__ == '__main__':
    n = 1000000
    print(f"Optimal play wins (Python): {play_optimal(n):.1f}%")