#!/usr/bin/python

import threading
import time
import sys

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
    f_ops = []
    i_ops = []
    
    
    for _ in range(3):
        
        #Calculating FLOPS:
        thread_list = []

        #Create number of threads defined in num_threads from user input.
        for _ in range(int(num_threads)):
            threads = cpu_benchmark(True)
            threads.start()
            thread_list.append(threads)
        
        #Create the timer and wait.  Test time is defined from user input
        timer_thread = threading.Thread(target=time_thread, args=(int(test_time),))
        timer_thread.start()
        timer_thread.join()

        #After test time is over send update the termination flag to stop the counter.
        for t in thread_list:
            t.set_terminate_flag(False)

        #Get the number of operations and calculate FLOPS
        for t in thread_list:
            f_ops.append(t.get_number_operations())
            flops.append(t.get_number_operations() / int(test_time))

        
        #Calculating IOPS:

        thread_list = []

        #Create number of threads defined in num_threads from user input.
        for _ in range(int(num_threads)):
            threads = cpu_benchmark(False)
            threads.start()
            thread_list.append(threads)
        
        #Create the timer and wait.  Test time is defined from user input
        timer_thread = threading.Thread(target=time_thread, args=(int(test_time),))
        timer_thread.start()
        timer_thread.join()

        #After test time is over send update the termination flag to stop the counter.
        for t in thread_list:
            t.set_terminate_flag(False)

        #Get the number of operations and calculate IOPS
        for t in thread_list:
            i_ops.append(t.get_number_operations())
            iops.append(t.get_number_operations() / int(test_time))

    print("FLOPS Output")    
    print(f"{f_ops}")
    print(f"{flops}")
    print("\n\nIOPS Output")
    print(f"{i_ops}")
    print(f"{iops}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        display_help()
    else:
        main(sys.argv[1], sys.argv[2])