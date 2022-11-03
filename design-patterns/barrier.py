"""

Write a program in which n people follow some communication (random time to travel) to the restaurant. The order can
be placed only after the arrival of all people. There is consumption (again random time) and departure from the table
when everyone is done.

"""

import threading
import time
from random import randint


def new_thread(name, activity):
    print("Person {}: started {}".format(name, activity))
    secondsToSleep = randint(1, 10)
    time.sleep(secondsToSleep)
    print("Person {}: finished {}".format(name, activity))


def action(n, new_thread, activity_type):
    for i in range(n):
        t = threading.Thread(target=new_thread, args=(i, activity_type))
        threads.append(t)
        t.start()
        time.sleep(0.23)
    
    for index, thread in enumerate(threads):
        thread.join()
      
        
def meals():
    time.sleep(0.5)
    print('-- Everybody arrived --')
    time.sleep(1)
    print('-- Meals have been ordered --')
    time.sleep(1)
    print('-- Meals delivered --')
    time.sleep(0.5)


if __name__ == "__main__":

    n = 5
    threads = []
    
    action(n, new_thread, 'transport')
    meals()
    action(n, new_thread, 'dinner')
        
    print('-- Everybody left the table --')
   
    
