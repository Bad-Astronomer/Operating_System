import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

class Process:
    def __init__(self, index, priority, arrivalTime, serviceTime):
        self.index = index
        self.priority = priority
        self.serviceTime = serviceTime
        self.arrivalTime = arrivalTime
        
        self.remainingTime = serviceTime
        self.finishTime = arrivalTime + serviceTime
    
    def info(self):
        print(f"\nProcess P{self.index}:\n")
        print(f"Priority:\t {self.priority}")
        print(f"Arrival Time:\t {self.arrivalTime}")
        print(f"Service Time:\t {self.serviceTime}")
    
    def colorize(self):
        r = random.randint(100, 255)/255
        g = random.randint(100, 255)/255
        b = random.randint(100, 255)/255
        self.color = (r, g, b, 1)
    
    def update(self):
        self.remainingTime -= 1
        self.remainingTime = max(self.remainingTime, 0)
        gantt.append(self)
    
    def calc(self):
        waitingTime = self.finishTime - self.arrivalTime - self.serviceTime
        turnaroundTime = self.finishTime - self.arrivalTime
        # print(f"\nProcess P{self.index}:\n")
        # print(f"Waiting Time:\t {waitingTime}")
        # print(f"Turnaround:\t {turnaroundTime}")
        return waitingTime, turnaroundTime
    
    def reset(self):
        self.remainingTime = self.serviceTime
        self.finishTime = self.arrivalTime + self.serviceTime


def plot(label):
    plt.style.use('dark_background')
    width = totalTime * 1.5
    height = processCount * 1.5
    fig, ax = plt.subplots(figsize=(width, height))

    ax.set_xlim(0, totalTime)
    ax.set_ylim(1, processCount + 1)

    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))

    ax.set_xlabel('Clock Tick')
    ax.set_ylabel('Process')

    plt.grid(True)

    for i in range(totalTime):
        x = i
        y = gantt[i].index
        square = patches.Rectangle((x, y), 1, 1, linewidth=1, facecolor=gantt[i].color)
        ax.add_patch(square)
        
        if(gantt[i].index != gantt[i-1].index) or not i:
            ax.text(x + 0.5, y + 0.5, f"P{gantt[i].index}", ha='center', va='center', color='black')

    ax.set_position([0.125, 0.2, 0.7, 0.7])
    fig.suptitle(label)
    
def calc(label):
    timings = [process.calc() for process in processes]
    
    avgWaitingTime = sum([time[0] for time in timings])/processCount
    avgTurnaroundTime = sum([time[1] for time in timings])/processCount
    
    print(f"\n{label}\n")
    print(f"AVG Waiting Time:\t {avgWaitingTime}")
    print(f"AVG Turnaround:\t\t {avgTurnaroundTime}")
    
    plot(label)


def roundRobin():
    global processes, gantt
    remaining, waiting = [process for process in processes], []
        
    clock = 0
    for process in remaining:
            if process.arrivalTime <= clock:
                waiting.append(process)
    for process in waiting:
        if process in remaining: remaining.remove(process)
    current = waiting[0]

    running = timeQuantum
    for clock in range(totalTime):
        for process in remaining:
            if process.arrivalTime <= clock:
                waiting.append(process)
        for process in waiting:
            if process in remaining: remaining.remove(process)
        
        if not running or not current.remainingTime:
            running = timeQuantum
            
            #* Prev current
            if current.remainingTime:
                waiting.append(current)
            else:
                current.finishTime = clock
            waiting.pop(0)
            
            #* New current
            current = waiting[0]
        current.update()
        running -= 1
    
    waiting[0].finishTime = clock + 1
    waiting.pop(0)

    calc("Round Robin")
    
    gantt = []
    [process.reset() for process in processes]
    
    
def shortestRemainingTime():
    global processes, gantt
    waiting, remaining = [], [process for process in processes]
    for clock in range(totalTime):
        for i, process in enumerate(remaining):
            if process.arrivalTime <= clock:
                waiting.append(process)
        for process in waiting:
            if process in remaining: remaining.remove(process)
        
        if not waiting[0].remainingTime:
            waiting[0].finishTime = clock
            waiting.pop(0)
        
        waiting = sorted(waiting, key=lambda process: process.remainingTime)
        waiting[0].update()
    waiting[0].finishTime = clock + 1
    waiting.pop(0)
    
    calc("Shortest Remaining Time First")
    
    gantt = []
    [process.reset() for process in processes]


def priority():
    global processes, gantt
    waiting, remaining = [], [process for process in processes]
    
    for clock in range(totalTime):
        for i, process in enumerate(remaining):
            if process.arrivalTime <= clock:
                waiting.append(process)
        for process in waiting:
            if process in remaining: remaining.remove(process)
            
        waiting = sorted(waiting, key=lambda process: process.priority)

        waiting[0].update()
        if not waiting[0].remainingTime:
            waiting[0].finishTime = clock + 1
            waiting.pop(0)
    
    calc("Preemtive Priority Based")
    
    gantt = []
    [process.reset() for process in processes]


global gantt, porcesses
gantt, processes = [], []

processCount = int(input("Enter number of processes:\t"))
timeQuantum = int(input("Enter Time Quantum:\t\t"))

for i in range(processCount):
    process = Process(  
                        i+1,
                        int(input(f"\nEnter Priority of P{i+1}:\t\t")),
                        int(input(f"Enter Arrival Time of P{i+1}:\t")),
                        int(input(f"Enter Service Time of P{i+1}:\t"))
                    )
    process.colorize()
    processes.append(process)

[process.info() for process in processes]

processes = sorted(processes, key=lambda process: process.arrivalTime)
totalTime = sum([process.serviceTime for process in processes])

roundRobin()
shortestRemainingTime()
priority()

plt.show()