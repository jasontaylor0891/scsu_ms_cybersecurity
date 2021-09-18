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
        #print(f"{self.number_of_operations}")
        

def display_help():
    print("\nusage: cpu_benchmark.py sample_time number_of_threads\n")

def time_thread(sleep_time):
    time.sleep(sleep_time)

def main(test_time, num_threads):

    t1 = cpu_benchmark(False)
    t2 = cpu_benchmark(False)

    t1.start()
    t2.start()

    flops_thread = threading.Thread(target=time_thread, args=(int(test_time),))
    flops_thread.start()
    flops_thread.join()

    #cpu_benchmark.set_terminate_flag(False)
    t1.set_terminate_flag(False)
    t2.set_terminate_flag(False)

    print(t1.get_number_operations())
    print(t2.get_number_operations())
    print("done")
    #t2.start()

    
    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        display_help()
    else:
        main(sys.argv[1], sys.argv[2])