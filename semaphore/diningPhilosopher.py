import threading
import time
import random


nPhilosophers = 5
nForks = nPhilosophers
forks = [threading.Semaphore(1) for i in range(nForks)] # forks mutex
mutex = threading.Semaphore(1) # philosopher mutex


def philosopher(index):
    while True:
        print(f"Philosopher {index}: THINKING   ")
        time.sleep(random.randint(1, 5))
        
        mutex.acquire()
        forks[index - 1].acquire()  # left fork => index - 1
        forks[index].acquire()      # right fork => index
        print(f"Philosopher {index}: EATING   ")
        time.sleep(random.randint(1, 5))
        mutex.release()
        
        forks[index].release()
        forks[index - 1].release()


threads = []
for i in range(nPhilosophers):
    threads.append(threading.Thread(target = philosopher, args = (i,)))

[thread.start() for thread in threads]
[thread.join() for thread in threads]