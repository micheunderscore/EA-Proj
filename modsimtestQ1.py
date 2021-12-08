import random
import threading

simTime, simEnd = 0, 100
# Copy from here
# Class Objects =====================================
# Person Class
class Person(threading.Thread):
    WALKING = 0
    INTERACTED = 1
    QUEUEING = 2

    def __init__(self, interest):
        threading.Thread.__init__(self)
        # Person interest to the store (Int)
        self.interest = interest
        # Distance (Int) is -2 due to 
        # person has to walk closer before interaction with stall
        self.distance = -2
        # Person status
        self.status = Person.WALKING

    # Interact with salesperson
    def interact(self, person):
        self.interest = random.randint(0, person.expertise)
        self.status = Person.INTERACTED 

    def run(self):
        while simTime < simEnd:
            # Walking by/towards
            self.distance += 1

            # If person is already interested, go queue
            if self.interest > 4 and self.distance == 0:
                self.status = Person.QUEUEING

            # If person is close to store, inspect the queue
            elif self.distance == 0:
                # Count people queueing and compound with current interest
                for person in peoples:
                    if person.status == Person.QUEUEING:
                        self.interest += 1

                # If queue is significant + interest enough, join the queue
                if self.interest > 5:
                    self.status = Person.QUEUEING

            # If distance is too far, break out the loop and kill thread
            elif self.distance > 2:
                break

# Sales Person Class
class SalesPerson(threading.Thread):
    IDLE = 0
    INTERACTING = 1
    
    def __init__(self, id, expertise):
        threading.Thread.__init__(self)
        # Their ID
        self.id = id
        # Their convincing skills (1 - 10)
        self.expertise = expertise
        # Current attendedPerson
        self.attendedPerson = None
        # Current activity status
        self.status = SalesPerson.IDLE

    def run(self):
        while simTime < simEnd:
            # If staff isn't doing anything
            while self.status == SalesPerson.IDLE:
                # Look for potential victims
                if len(peoples) > 0:
                    focus = random.randint(0, len(peoples) - 1)
                    person = peoples[focus]
                    # Check if focus person is possible victim
                    if person.distance == 0 and person.status == Person.WALKING:
                        self.attendedPerson = person
                        self.status = SalesPerson.INTERACTING
            # If sales staff is not doing anything,
            # find someone to interact with
            if self.status != SalesPerson.IDLE and self.attendedPerson != None:
                self.attendedPerson.interact(self)
                self.attendedPerson = None
                self.status = SalesPerson.IDLE
                    
# INITIALIZATION ====================================
# Make two staffs
for i in range(2):
    staff = SalesPerson(i, random.randint(1, 10))
    staff.start()

peoples = []

# Simulation ========================================
while simTime < simEnd:
    queueLengf = 0 # Queue length resets for accuracy

    # Creates new person with preset random interest
    # Determines if the person is intending to go 
    # to the stall itself in the first place
    interest = random.randint(0, 10)
    person = Person(interest)
    person.start()

    # Calculate queue length
    if len(peoples) > 0:
        for person in peoples:
            if person.status == Person.QUEUEING:
                queueLengf += 1

    # BROADCAST: Queue length
    print("Queue lengf: %r" % (queueLengf))

    # Advance time
    simTime += 1
