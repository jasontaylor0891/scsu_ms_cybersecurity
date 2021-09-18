#!/usr/bin/python

import concurrent.futures
import threading
import time
import sys



def time_thread(sleep_time):
    global flag
    print(f"{flag}")
    time.sleep(sleep_time)
    flag=False
    print(f"{flag}")

def flops_counter():
    global flag
    flag=True
    i=0
    print("got here")
    flops_thread = threading.Thread(target=time_thread, args=(10),)
    flops_thread.start()
    while flag:
        i+=1.0
    return i


def iops_counter():
    print("iops counter function.")

def display_help():
    print("\nusage: cpu_benchmark.py sample_time number_of_threads\n")


def main(test_time, num_threads):
    print(f"Test time: {test_time} \nNumber of threads: {num_threads}")

    
    flops_num_ops = 0.0

    #flops_thread = threading.Thread(target=time_thread, args=(int(test_time),))
    #flops_thread.start()

    start = time.perf_counter()
        
    #while flag:
    with concurrent.futures.ThreadPoolExecutor() as flops:
        results = [flops.submit(flops_counter) for _ in range(2)]
        
        
    finish = time.perf_counter()
    print(f"Finished in {round(finish-start, 2)} second(s)")
    print(f"{flops_num_ops}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        display_help()
    else:
        main(sys.argv[1], sys.argv[2])