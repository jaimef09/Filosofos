# -*- coding: utf-8 -*-

from monitor import AnticheatTable as Table, CheatMonitor
from multiprocessing import Process, Manager
import time
import random

NPHIL = 5

def delay(n):
	time.sleep(random.random()/n)
	
def philosopher_task(num:int, table:Table, cheat:CheatMonitor):
    table.set_current_phil(num)
    cont = 0
    while cont<=100:
        print(f"Philosopher {num} thinking {cont}")
        print(f"Philosopher {num} wants to eat {cont}")
        table.wants_eat(num)
        if num == 0 or num == 2:
            cheat.is_eating(num)
        print(f"Philosopher {num} eating {cont}")
        if num == 0 or num == 2:
            cheat.wants_think(num)
        table.wants_think(num)
        print(f"Philosopher {num} stops eating {cont}")
        cont += 1
        
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
    
