import time
import psutil 
import os 
# V doors = [0B] * 100
# L(i) 0.<100
#    L(j) (i .< 100).step(i + 1)
#       doors[j] = !doors[j]
#    print(‘Door ’(i + 1)‘: ’(I doors[i] {‘open’} E ‘close’))

#setup resoures tracking
process = psutil.Process(os.getpid())

door_number = 100
def solve_door():
    doors = [False] * door_number 

    for i in range(door_number ):
        for j in range(i , door_number  , i+1):
            doors[j] = not doors[j]
    
    return doors

final_door = solve_door()
start_time = time.perf_counter()

start_mem = process.memory_info().rss / (1024*1024) # convert to MB
for idx, open_state in enumerate(final_door):
    status = "open" if open_state else "closed"
    if open_state:
        print(f"Doors {idx+1}: {status}")

end_time = time.perf_counter()
end_mem = process.memory_info().rss / (1024*1024)
cpu_usage = psutil.cpu_percent(interval=None)

#calculate duration and memory usage
duration = end_time - start_time
memory_usage = end_mem - start_mem

#Power estimation
#(CPU % 100) * Avg CPU TDP(W.) * Time(sec.)
est_joules = (cpu_usage/100 )* 25 * duration


print(f"Process duration : {duration:.4f} sec.")
print(f"Memory usage :{memory_usage:.4f} MB")
print(f"CPU usage : {cpu_usage:.4f} %")
print(f"Est. power : {est_joules:.8f} Joules")