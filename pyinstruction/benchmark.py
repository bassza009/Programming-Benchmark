import psutil 
import os 

#setup resoures tracking
process = psutil.Process(os.getpid())

start_mem = process.memory_info().rss / (1024*1024) # convert to MB

#---------------------------instruction---------------------------------


#--------------------------------------------------------------------------

end_mem = process.memory_info().rss / (1024*1024)
cpu_usage = psutil.cpu_percent(interval=None)

#calculate duration and memory usage
memory_usage = end_mem - start_mem

#Power estimation
#(CPU % 100) * Avg CPU TDP(W.) * Time(sec.)
est_joules = (cpu_usage/100 )* 25 * duration