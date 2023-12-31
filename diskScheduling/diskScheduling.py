"""
    FIFO
    SSTF
    SCAN
    C-SCAN
    LOOK
"""
# ! IN CODE LOOK is SCAN and CLOOK is CSCAN


import matplotlib.pyplot as plt
import numpy


plt.style.use('dark_background')
def calc(label, graph):
    
    """
        graph = [
            [request_served, time_stamp], ...
        ]
    """
    
    print(f"{label}:")
    print(f"Avg track traversals: {graph[-1][1] / len(requests)}\n")
    
    [print(i) for i in graph]
    
    x, y = [i[0] for i in graph], [i[1] for i in graph]
    
    plt.scatter(x, y)
    plt.plot(x, y, label=label)


def fifo(requests, head):
    graph = [[start, 0]]
    for request in requests:
        time_stamp = abs(head - request)
        graph.append([request, time_stamp + graph[-1][1]])
        head = request
    
    calc("fifo", graph)


def sstf(requests, head):
    graph = [[start, 0]]
    
    for i in range(len(requests)):
        requests.sort(key = lambda request: abs(head - request))
        time_stamp = abs(head - requests[0])
        graph.append([requests[0], time_stamp + graph[-1][1]])
        head = requests[0]
        requests.pop(0)

    calc("sstf", graph)


def scan(requests, head, last = 0):
    
    '''
        direction:
        <-- == +1   [high to low]
        --> == -1   [low to high]
    '''
    if last: requests.append(0)
    if last: requests.append(last)
    
    requests.sort()
    graph = [[start, 0]]
    direction = numpy.sign(requests [-1] - 2*head)  # sign( l/2 - h ) => sign = -1 if h > l/2
    
    for _ in ["forward", "backward"]:
        for request in requests:
            if numpy.sign(head - request) == direction:
                graph.append([request, direction * (head - request) + graph[-1][1]])
                head = request
        direction = -direction
    
    graph.sort(key = lambda cord: cord[1])
    if last: calc("scan", graph)
    else: calc("look", graph)


def cscan(requests, head, last = 0):
    graph = [[start, 0]]
    direction = 1
    
    while True:
        requests.sort()
        for request in requests:
            if numpy.sign(head - request) != direction:
                graph.append([request, abs(head - request) + graph[-1][1]])
                head = request
        
        direction = 0
        travel = max(requests) - min(requests)
        
        for request, _ in graph:
            if request in requests:
                requests.remove(request)
        if not requests: break
        
        if last:
            graph.append([last, last - head + graph[-1][1]])
            graph.append([0, last + graph[-1][1]])
            head = 0
        else:
            graph.append([requests[0], travel + graph[-1][1]])
            head = requests[0]
    
    if last: calc("cscan", graph)
    else: calc("clook", graph)

def look(requests, head):
    scan(requests, head, 0)

def clook(requests, head):
    cscan(requests, head, 0)


# requests = [55, 58, 39, 18, 90, 160, 150, 38, 184]
requests = [98, 183, 37, 122, 14, 124, 65, 67]
# requests = [82, 170, 43, 140, 24, 16, 190]
start = 100

fifo(requests[:], start)
sstf(requests[:], start)
look(requests[:], start)
clook(requests[:], start)
# scan(requests[:], start, 199)
# cscan(requests[:], start, 199)



plt.axvline(start, color="#a1a1a1", linestyle="--")
[plt.axvline(request, color="#a1a1a1", linestyle="--") for request in requests]

plt.gca().invert_yaxis()
plt.title("Disk Scheduling")
plt.xlabel("Tracks")
plt.ylabel("Time")

plt.legend()
plt.show()
