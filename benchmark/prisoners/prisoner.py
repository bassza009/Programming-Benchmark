import random
import time

def play_random(n, num_prisoners=100):
    pardoned = 0
    sampler = list(range(num_prisoners))
    for _ in range(n):
        in_drawer = list(range(num_prisoners))
        random.shuffle(in_drawer)
        success = True
        for prisoner in range(num_prisoners):
            # สุ่มเลือก 50 ใบ
            revealed = random.sample(sampler, num_prisoners // 2)
            if prisoner not in [in_drawer[i] for i in revealed]:
                success = False
                break
        if success:
            pardoned += 1
    return (pardoned / n) * 100

def play_optimal(n, num_prisoners=100):
    pardoned = 0
    in_drawer = list(range(num_prisoners))
    for _ in range(n):
        random.shuffle(in_drawer)
        success = True
        for prisoner in range(num_prisoners):
            reveal = prisoner
            found = False
            for go in range(num_prisoners // 2):
                card = in_drawer[reveal]
                if card == prisoner:
                    found = True
                    break
                reveal = card
            if not found:
                success = False
                break
        if success:
            pardoned += 1
    return (pardoned / n) * 100

def run_benchmark(n):
    results = []
    
    # ทดสอบ Optimal
    start = time.perf_counter()
    win_opt = play_optimal(n)
    time_opt = time.perf_counter() - start
    results.append(["Optimal Strategy", f"{win_opt:6.2f}%", f"{time_opt:8.4f}s"])

    # ทดสอบ Random
    start = time.perf_counter()
    win_rand = play_random(n)
    time_rand = time.perf_counter() - start
    results.append(["Random Strategy", f"{win_rand:6.2f}%", f"{time_rand:8.4f}s"])

    # พิมพ์ตารางแบบ Manual (คล้าย console.table)
    header = ["Strategy", "Win Rate", "Time Used"]
    print(f"\nSimulation count: {n:,}")
    print("-" * 45)
    print(f"{header[0]:<20} | {header[1]:<10} | {header[2]:<10}")
    print("-" * 45)
    for row in results:
        print(f"{row[0]:<20} | {row[1]:<10} | {row[2]:<10}")
    print("-" * 45)

if __name__ == '__main__':
    # แนะนำให้ใช้ 10,000 รอบก่อน เพราะแบบ Random ใน Python จะช้ากว่า JS พอสมควรครับ
    run_benchmark(10000)