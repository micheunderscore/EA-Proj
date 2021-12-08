import random
import threading
import time
from queue import Queue


# COPY HERE
# Class Objects =====================================
# Counter Class
class Counter(threading.Thread):
    IDLE = 0
    BUSY = 1
    OUT_OF_ORDER = 2

    def __init__(self, id, efficiency):
        threading.Thread.__init__(self)
        self.id = id
        self.customer = None
        self.status = Counter.IDLE
        self.efficiency = efficiency
        self.progress = 0
    
    def run(self):
        while simTime < simEnd:
            time.sleep(1)

            if self.status == Counter.BUSY:
                if self.progress >= 5:
                    self.status = Counter.IDLE
                    self.customer = None
                    print(self.id, "DONE!")
                else:
                    self.progress += random.randint(0, self.efficiency) - random.randint(0, self.customer.difficulty)
                    print(self.id, ">>", self.progress)
            else:
                if not customerQ.empty():
                    self.customer = customerQ.get()
                    self.status = Counter.BUSY
                    self.customer.status = Customer.CHECKING_IN
                    self.progress = 0


class Customer(threading.Thread):
    WAITING = 0
    CHECKING_IN = 1
    DONE = 2

    def __init__(self, difficulty):
        threading.Thread.__init__(self)
        self.difficulty = difficulty
        self.counter = None
        self.status = Customer.WAITING
    
    def run(self):
        while self.status != Customer.DONE:
            if self.status == Customer.WAITING:
                time.sleep(1)
                continue
            if self.status == Customer.CHECKING_IN:
                time.sleep(1)

# INITIALIZATION ====================================
simTime, simEnd = 0, 500
customerQ = Queue()

queueLength = []
counters = []

for i in range(5):
    counter = Counter(i, random.randint(5, 10))
    counters.append(counter)
    counter.start()

# Simulation ========================================
while simTime < simEnd:
    if simTime % 10 == 0:
        for i in range(random.randint(5, 20)):
            difficult = random.randint(0, 5)
            customer = Customer(difficult)
            customerQ.put(customer)
            customer.start()

    print("Queue length at time:", simTime, "is:", customerQ.qsize())
    queueLength.append(customerQ.qsize())
    
    time.sleep(1)
    simTime += 1


