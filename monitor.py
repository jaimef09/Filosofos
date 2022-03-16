# -*- coding: utf-8 -*-

from multiprocessing import Condition, Lock
from multiprocessing import Array, Manager, Value

class Table:
    def __init__(self, NPHIL, manager):
        self.mutex = Lock()
        self.freefork = Condition(self.mutex)
        self.num_phil = None
        self.eating = Value('i',0)
        self.phil = manager.list([False for _ in range(NPHIL)])
        self.NPHIL = NPHIL
    
    def set_current_phil(self,i):
        self.num_phil = i
        
    def others_not_eating(self):
        return ((not self.phil[(self.num_phil-1)%self.NPHIL]) and (not self.phil[(self.num_phil+1)%self.NPHIL]))
    
    def wants_eat(self,i):
        self.mutex.acquire()
        self.freefork.wait_for(self.others_not_eating)
        self.phil[i] = True
        self.eating.value += 1
        self.mutex.release()
        
    def wants_think(self,i):
        self.mutex.acquire()
        self.phil[i] = False
        self.eating.value -= 1
        self.freefork.notify_all()
        self.mutex.release()
        

class CheatMonitor:
    def __init__(self):
        self.mutex = Lock()
        self.eating = Value('i',0)
        self.other_eating = Condition(self.mutex)
        
    def is_eating(self,i):
        self.mutex.acquire()
        self.eating.value += 1
        self.other_eating.notify_all()
        self.mutex.release()
    
    def can_think(self):
        return self.eating.value > 1
    
    def wants_think(self,i):
        self.mutex.acquire()
        self.other_eating.wait_for(self.can_think, 0.5)
        self.eating.value -= 1
        self.mutex.release()
        
class AnticheatTable:
    def __init__(self, NPHIL, manager):
        self.mutex = Lock()
        self.freefork = Condition(self.mutex)
        self.num_phil = None
        self.eating = Value('i',0)
        self.phil = manager.list([False for _ in range(NPHIL)])
        self.chungry = Condition(self.mutex)
        self.hungry = manager.list([False for _ in range(NPHIL)])
        self.NPHIL = NPHIL
    
    def set_current_phil(self,i):
        self.num_phil = i
        
    def others_not_eating(self):
        return ((not self.phil[(self.num_phil-1)%self.NPHIL]) and (not self.phil[(self.num_phil+1)%self.NPHIL]))
    
    def can_eat(self):
        return not self.hungry[(self.num_phil+1)%self.NPHIL]
    
    def wants_eat(self,i):
        self.mutex.acquire()
        self.chungry.wait_for(self.can_eat)
        self.hungry[i] = True
        self.freefork.wait_for(self.others_not_eating)
        self.phil[i] = True
        self.eating.value += 1
        self.hungry[i] = False
        self.chungry.notify_all()
        self.mutex.release()
        
    def wants_think(self,i):
        self.mutex.acquire()
        self.phil[i] = False
        self.eating.value -= 1
        self.freefork.notify_all()
        self.mutex.release()
