#!/usr/bin/python

import threading
import time
import statistics

def time_thread(sleep_time):
    global flag
    time.sleep(sleep_time)
    flag=False
    
def main():
    
    global flag
    flops = []
    iops = []

    run_time = 60

    for _ in range(3):
    
        flops_num_ops=0.0
        iops_num_ops=0
        flag=True

        flops_thread = threading.Thread(target=time_thread, args=(run_time,))
        flops_thread.start()
        
        while flag:
            flops_num_ops += 1.0

        flops.append(flops_num_ops // run_time)

        flag=True
        iops_thread = threading.Thread(target=time_thread, args=(run_time,))
        iops_thread.start()
        
        while flag:
            iops_num_ops += 1
 
        iops.append(iops_num_ops // run_time) 

    print(f"Output flops list: {flops}")
    print(f"Output iops list: {iops}")

    print(f"Mean flops: {statistics.mean(flops)}")
    print(f"Mean iops: {statistics.mean(iops)}")

    print(f"Standard deviation flops: {statistics.stdev(flops)}")
    print(f"Standard deviation iops: {statistics.stdev(iops)}")

if __name__ == "__main__":
    main()



