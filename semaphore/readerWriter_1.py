import threading
import time
import random


def writer(writer_id):
    # wait(rw_mutex)
    # write()
    # signal(rw_mutex)
    
    # print(f"WRTIER {writer_id}: START  ")
    
    rw_mutex.acquire()
    print(f"WRTIER {writer_id}: WRITING  ", flush=True)
    # logs += f"WRTIER {writer_id}: WRITING  "
    time.sleep(1)
    print(f"WRTIER {writer_id}: DONE  ", flush=True)
    # logs += f"WRTIER {writer_id}: DONE  "
    rw_mutex.release()

def reader(reader_id):
    # wait(mutex)
    # read_count++
    # if read_count == 1:
    #       wait(rw_mutex)
    # signal(mutex)
    
    # read()
    
    # wait(mutex)
    # read_count--
    # if read_count == 0:
    #       signal(rw_mutex);
    # signal(mutex)
    
    global read_count
    
    mutex.acquire()
    read_count += 1
    if read_count == 1:
        rw_mutex.acquire()
    mutex.release()
    
    time.sleep(1)
    
    mutex.acquire()
    read_count -= 1
    if read_count == 0:
        rw_mutex.release()
    mutex.release()
    
    print(f"READER {reader_id}: DONE  ", flush=True)
    # logs += f"READER {reader_id}: DONE  "


mutex = threading.Semaphore(1)
rw_mutex = threading.Semaphore(1)
read_count = 0
# logs = ""

threads = []

for i in range(3):
    writer_thread = threading.Thread(target=writer, args=(i + 1,))
    reader_thread = threading.Thread(target=reader, args=(i + 1,))
    threads.append(writer_thread)
    threads.append(reader_thread)

random.shuffle(threads)

[thread.start() for thread in threads]    
[thread.join() for thread in threads]    

# print(f"\n\nLogs:\n")
# for log in logs.split("  "):
#     print(log)