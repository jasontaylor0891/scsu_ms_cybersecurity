#!/usr/bin/python

import threading
import time
import sys
import statistics

class cpu_benchmark(threading.Thread):

    #init method to set default variables
    def __init__(self, operation_type):

        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.operation_type=operation_type
        self.terminate = True
        self.number_of_operations = 0

    #Method to set the terminate flag
    def set_terminate_flag(self, flag):
        self.terminate = flag

    #Method to return the number of operations
    def get_number_operations(self):
        return self.number_of_operations

    #Method to calculate the number of floting-point or integer operations
    def run(self):
        f=0.0
        i=0

        self.lock.acquire()
        if self.operation_type:
            while self.terminate:
                f +=1.0
            self.number_of_operations = f
        else:
            while self.terminate:
                i +=1
            self.number_of_operations = i
        self.lock.release()    
        

#Display usage for this script
def display_help():
    print("\nusage: cpu_benchmark.py test_time number_of_threads\n")

#Function used to mesure wait time.
def time_thread(sleep_time):
    time.sleep(sleep_time)

#Main Function
def main(test_time, num_threads):

    sum_flops = []
    sum_iops = []
    
    for _ in range(3):
        
        #Calculating FLOPS:
        thread_list = []
        flops = []
        iops = []

        start_time = time.time()
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

        end_time = time.time()
        total_time = (end_time - start_time)
 
        #Get the number of operations and calculate FLOPS
        time.sleep(1)
        for t in thread_list:
            flops.append(t.get_number_operations() // int(total_time))

        #Append the summed floting-point operations per second to the sum_flops list
        sum_flops.append(sum(flops))

        #Calculating IOPS:

        thread_list = []
        flops = []
        iops = []

        start_time = time.time()
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

        end_time = time.time()
        total_time = (end_time - start_time)

        #Get the number of operations and calculate IOPS
        time.sleep(1)
        for t in thread_list:
            iops.append(t.get_number_operations() // int(total_time))
        
        #Append the summed interger operations per second to the sum_iops list
        sum_iops.append(sum(iops))

    #Display output from the test runs
    print("##############################################")
    print(f"# Test time (seconds): {test_time}")
    print(f"# Number of threads  : {num_threads}")
    print("##############################################")

    flops_mean=statistics.mean(sum_flops)
    iops_mean=statistics.mean(sum_iops)

    print(f"Giga FLOPS: {flops_mean / 1000000000}")
    print(f"Giga IOPS : {iops_mean / 1000000000}")

    print(f"Mean flops: {flops_mean}")
    print(f"Mean iops : {iops_mean}")

    print(f"Standard deviation flops: {statistics.stdev(sum_flops)}")
    print(f"Standard deviation iops : {statistics.stdev(sum_iops)}")
    print("##############################################")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        display_help()
    else:
        main(sys.argv[1], sys.argv[2])