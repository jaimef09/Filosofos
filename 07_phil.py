# -*- coding: utf-8 -*-

from multiprocessing import Process
from multiprocessing import Condition, Semaphore, Lock
from multiprocessing import Array, Manager, Value
import time
import random

from monitor import Table, CheatMonitor

NPHIL = 5
K = 100



def delay(n):
    time.sleep (random.random()/n)
    
def philosopher_task(num:int, table:Table, cheat:CheatMonitor):
    table.set_current_phil(num)
    while True:
        print(f"Philosopher {num} thinking")
        print(f"Philosopher {num} wants to eat")
        table.wants_eat(num)
        if num == 0 or num == 2:
            cheat.is_eating(num)
        print(f"Philosopher {num} eating")
        if num == 0 or num == 2:
            cheat.wants_think(num)
        table.wants_think(num)
        print(f"Philosopher {num} stops eating")

def main():
    manager = Manager()
    table = Table(NPHIL, manager)
    cheat = CheatMonitor()
    philosophers = [Process(target=philosopher_task, args = (i,table,cheat))
                    for i in range(NPHIL)]
    for i in range(NPHIL):
        philosophers[i].start()
    for i in range(NPHIL):
        philosophers[i].join()
        
if __name__ == '__main__':
    main()