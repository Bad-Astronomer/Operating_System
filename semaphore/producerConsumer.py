import multiprocessing
import time
# import os


def wait(semaphore, lock, comment):
    with lock: # Mutex (lock) on semaphore
        # print(multiprocessing.current_process().pid, f"{semaphore.value} -> {semaphore.value - 1}")
        
        semaphore.value -= 1
        if semaphore.value == -1:
            semaphore.value = 0
        else:
            print(f"{comment} SUCCESSFUL")
            return
        
        # if semaphore.value != 0:
        #     semaphore.value -= 1
        #     return
    
    print(f"{comment} FAILED")
    time.sleep(1)
    wait(semaphore, lock, comment)

def signal(semaphore, lock, comment):
    with lock:
        semaphore.value += 1
    print(f"{comment} SUCCESSFUL")


def producer(m, e, f, buffer, lock, pid):
    # wait(m)
    # wait(e)
    # produce()
    # signal(m)
    # signal(f)
    
    wait(m, lock, f"producer {pid}: wait(m)")
    wait(e, lock, f"producer {pid}: wait(e)")
    
    time.sleep(1) # produce
    buffer[BUFFER_SIZE - (e.value + 1)] = int(pid[1:])
    print(f"PRODUCER PROCESS {pid} DONE")
    print(f"Buffer:\t{buffer[:]}")
    print(f"{pid.upper()}\tm: {m.value}\te: {e.value}\tf: {f.value}", end="\n\n")
    time.sleep(1) # produce
    
    signal(m, lock, f"producer {pid}: signal(m)")
    signal(f, lock, f"producer {pid}: signal(f)")


def consumer(m, e, f, buffer, lock, pid):
    # wait(f)
    # wait(m)
    # consume()
    # signal(m)
    # signal(e)
    
    wait(f, lock, f"consumer {pid}: wait(f)")
    wait(m, lock, f"consumer {pid}: wait(m)")
    
    time.sleep(1) #consume
    buffer[BUFFER_SIZE - (e.value + 1)] = -1
    print(f"CONSUMER PROCESS {pid} DONE")
    print(f"Buffer:\t{buffer[:]}")
    print(f"{pid.upper()}\tm: {m.value}\te: {e.value}\tf: {f.value}", end="\n\n")
    time.sleep(1) #consume
    
    signal(m, lock, f"consumer {pid}: signal(m)")
    signal(e, lock, f"consumer {pid}: signal(e)")


global BUFFER_SIZE
BUFFER_SIZE = 3

if __name__ == '__main__': 

    # Shared memory
    m = multiprocessing.Value('i', 1)

    f = multiprocessing.Value('i', 0)
    e = multiprocessing.Value('i', BUFFER_SIZE)
    buffer = multiprocessing.Array('i', [0 for i in range(BUFFER_SIZE)])

    lock = multiprocessing.Lock()
    
    # print(m.value, e.value, f.value, multiprocessing.current_process().pid)
    
    #! NOT SHARED
    # m = 1
    # e = BUFFER_SIZE
    # f = 0
    # buffer =  []
    
    # print(m, e, f, buffer, multiprocessing.current_process().pid)
    
    producer1 = multiprocessing.Process(target = producer, args=(m, e, f, buffer, lock, "p1"))
    consumer1 = multiprocessing.Process(target = consumer, args=(m, e, f, buffer, lock, "c1"))
    
    producer2 = multiprocessing.Process(target = producer, args=(m, e, f, buffer, lock, "p2"))
    consumer2 = multiprocessing.Process(target = consumer, args=(m, e, f, buffer, lock, "c2"))
    

    #! TEST CASE 1
    processes = [producer1, producer2, consumer1, consumer2]
    [process.start() for process in processes]
    [process.join() for process in processes]
    
    
    #! TEST CASE 2
    # processes = [producer1, consumer1, consumer2]
    # [process.start() for process in processes]
    
    # time.sleep(5)
    # producer2.start()
    
    # [process.join() for process in processes]
    # producer2.join()
    
    
    print(f"m:{m.value}\te: {e.value}\tf: {f.value}")
    print(f"Buffer:\t{buffer[:]}")