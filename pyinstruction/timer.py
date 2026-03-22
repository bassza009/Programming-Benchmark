import time 

#mesuring time

start_time = time.perf_counter()
time.sleep(1)  #หยุดการทำงานหน่วยเป็น วินาที
end_time = time.perf_counter()
duration = end_time - start_time

print(f"Task processing {duration:.4f} sec.")
