import time

def main():
    n = 1000000
    arr = [n - i for i in range(n)]

    print(f"Starting Bubble Sort (Python): {n} items")
    

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    
    print(f"Sample Result [0]: {arr[0]}")
    

if __name__ == "__main__":
    main()