import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random


colorPicker = lambda : [random.randint(128, 224)/255 for i in range(3)] + [1] # pick random color rgba

class Block:
    def __init__(self, size, offset):
        self.size = size
        self.offset = offset
        self.next = offset
        self.free = size
    
    def load(self, process, memory):
        memory[self.next : process.size + self.next] = [process.pid] * process.size #+ ["void"] * (self.free - process.size)
        self.next += process.size
        self.free -= process.size
    
    def reset(self):
        self.next = self.offset
        self.free = self.size


class Process:
    def __init__(self, pid, size):
        self.pid = pid
        self.size = size
        colors[pid] = colorPicker()
    
    def info(self):
        print(f"PID: {self.pid}\nSize: {self.size}\nColor: {colors[self.pid]}")


def plot(memory, blocks, label="Memory Allocation"):
    plt.style.use('dark_background')
    
    memSize = len(memory)
    height = max(1.5 * memSize//8, 8)
    fig, ax = plt.subplots(figsize=(6, height))
    ax.set_ylim(0, memSize)
    plt.grid(True)
    
    patch = lambda offset, size, color = "aqua": patches.Rectangle((0, offset), 4, size, linewidth=1, facecolor=color)
    [ax.add_patch(patch(block.offset, block.size, color = colors["unallocated"])) for block in blocks]
    
    for i, unit in enumerate(memory):
        ax.add_patch(patch(i, 1, color = colors[unit]))

    plt.gca().invert_yaxis()
    plt.yticks([block.offset for block in blocks] + [sum(block.size for block in blocks)])
    plt.xticks([])
    plt.title(label)
    
    legend_handles = [patches.Patch(color=color, label=label) for label, color in colors.items()]
    plt.legend(handles=legend_handles, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.subplots_adjust(right=0.7)
    
    [block.reset() for block in blocks]


def first_fit(processes, blocks):
    memSize = sum([block.size for block in blocks])
    memory = ["unallocated" for i in range(memSize)]
    
    for process in processes:
        for block in blocks:
            if block.free > process.size and block.free == block.size:
                block.load(process, memory)
                break
    plot(memory, blocks, "First Fit")

def best_fit(processes, blocks):
    memSize = sum([block.size for block in blocks])
    memory = ["unallocated" for i in range(memSize)]

    for process in processes:
        blocks.sort(key = lambda block: block.size - process.size)
        for block in blocks:
            if block.free > process.size and block.free == block.size:
                block.load(process, memory)
                break
    plot(memory, blocks, "Best Fit")

def worst_fit(processes, blocks):
    memSize = sum([block.size for block in blocks])
    memory = ["unallocated" for i in range(memSize)]

    for process in processes:
        blocks.sort(key = lambda block: -(block.size - process.size))
        for block in blocks:
            if block.free > process.size and block.free == block.size:
                block.load(process, memory)
                break
    plot(memory, blocks, "Worst Fit")



global colors
colors = {
        "unallocated" : "#121212",
        # "void" : "#242424",
    }


blocks = [5, 10, 15, 10]

processes = [
    Process("P1", 6),
    Process("P2", 4),
    Process("P3", 7),
    Process("P4", 2),
]

# blocks[0] = Block(blocks[0], 0)
# for i in range(1, len(blocks)):
#     blocks[i] = Block(blocks[i], blocks[i-1].offset + blocks[i])

for i, size in enumerate(blocks[:]):
    offset = sum(blocks[:i])
    blocks.append(Block(size, offset))
blocks = blocks[len(blocks)//2:]


# [process.info() for process in processes]

first_fit(processes, blocks)
best_fit(processes, blocks)
worst_fit(processes, blocks)

plt.show()
