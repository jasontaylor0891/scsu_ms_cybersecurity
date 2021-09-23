#!/usr/bin/python

#
#   When developing cpu_benchmark.py I found a significant difference in the number of
#   Operations for a local variable compared to a class variable.  I created this test script 
#   to look at the differences between the two.
#


import threading
import time
import statistics

class iteration_test(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.terminate = True
        self.number_of_operations = 0

    def set_terminate_flag(self, flag):
        self.terminate = flag

    def get_number_operations(self):
        return self.number_of_operations

    def run(self):
        while self.terminate: 
            self.number_of_operations +=1

def time_thread(sleep_time):
    global flag
    time.sleep(sleep_time)
    flag=False
    
def main():
    
    global flag
    num_ops = 0
    

    run_time = 60

    flag=True

    t1 = threading.Thread(target=time_thread, args=(run_time,))
    t1.start()
        
    while flag:
        num_ops += 1
    print(f"{num_ops}")


    test = iteration_test()
    test.start()

    flag=True
    t2 = threading.Thread(target=time_thread, args=(run_time,))
    t2.start()
    t2.join()
        
    test.set_terminate_flag(False)

    print(f"{test.get_number_operations()}")
    
 


if __name__ == "__main__":
    main()



