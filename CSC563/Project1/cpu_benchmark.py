#!/usr/bin/python

import threading
import time
import sys
import statistics

class cpu_benchmark(threading.Thread):
    
    def __init__(self, operation_type):
        threading.Thread.__init__(self)
        self.operation_type=operation_type
        self.terminate = True

    def set_terminate_flag(self, flag):
        self.terminate = flag

    def get_number_operations(self):
        return self.number_of_operations

    def run(self):
        if self.operation_type:
            self.number_of_operations = 0.0
            while self.terminate:
                self.number_of_operations +=1.0
        else:
            self.number_of_operations = 0
            while self.terminate:
                self.number_of_operations +=1

#Display usage for this script
def display_help():
    print("\nusage: cpu_benchmark.py sample_time number_of_threads\n")

#Function used to mesure wait time.
def time_thread(sleep_time):
    time.sleep(sleep_time)

def main(test_time, num_threads):

    flops = []
    iops = []
    
    for _ in range(3):
        
        #Calculating FLOPS:
        thread_list = []

        #Create number of threads defined in num_threads from user input.
        for _ in range(int(num_threads)):
            threads = cpu_benchmark(True)
            thread_list.append(threads)
            threads.start()
        
        #Create the timer and wait.  Test time is defined from user input
        timer_thread = threading.Thread(target=time_thread, args=(int(test_time),))
        timer_thread.start()
        timer_thread.join()

        #After test time is over send update the termination flag to stop the counter.
        for t in thread_list:
            t.set_terminate_flag(False)

        #Get the number of operations and calculate FLOPS
        for t in thread_list:
            flops.append(t.get_number_operations() // int(test_time))

        
        #Calculating IOPS:

        thread_list = []

        #Create number of threads defined in num_threads from user input.
        for _ in range(int(num_threads)):
            threads = cpu_benchmark(False)
            thread_list.append(threads)
            threads.start()

        #Create the timer and wait.  Test time is defined from user input
        timer_thread = threading.Thread(target=time_thread, args=(int(test_time),))
        timer_thread.start()
        timer_thread.join()

        #After test time is over send update the termination flag to stop the counter.
        for t in thread_list:
            t.set_terminate_flag(False)

        #Get the number of operations and calculate IOPS
        for t in thread_list:
            iops.append(t.get_number_operations() // int(test_time))

    print(f"Test lenght: {test_time}")
    print(f"Number of threads: {num_threads}")

    print(f"Output flops list: {flops}")
    print(f"Output iops list: {iops}")

    print(f"Mean flops: {statistics.mean(flops)}")
    print(f"Mean iops: {statistics.mean(iops)}")

    print(f"Standard deviation flops: {statistics.stdev(flops)}")
    print(f"Standard deviation iops: {statistics.stdev(iops)}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        display_help()
    else:
        main(sys.argv[1], sys.argv[2])