def main():
    n = 1000000
    doors = [False] * (n + 1)

    for pass_num in range(1, n + 1):
        for d in range(pass_num, n + 1, pass_num):
            doors[d] = not doors[d]

    open_count = 0
    for i in range(1, n + 1):
        if doors[i]:
            open_count += 1
    print(f"Open doors: {open_count}")


if __name__ == "__main__":
    main()
