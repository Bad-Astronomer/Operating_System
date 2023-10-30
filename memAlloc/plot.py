import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random


class Block:
    def __init__(self, size, offset):
        self.size = size
        self.offset = offset
        self.void = 0
    
    def load(self, processSize):
        memory[self.offset: processSize + 1] = ["process" for i in range(processSize)]



def plot(memory, blocks):
    colorPicker = lambda : [random.randint(120, 200)/255 for i in range(3)] + [1]
    plt.style.use('dark_background')
    colors = {
        "unallocated" : "#121212",
        "void" : "#242424",
        "process" : colorPicker(),
    }
    
    memSize = len(memory)
    height = min(1.5 * memSize//8, 8)
    fig, ax = plt.subplots(figsize=(4, height))
    plt.grid(True)
    
    ax.set_ylim(0, memSize)
    
    patch = lambda offset, size, color = "aqua": patches.Rectangle((0, offset), 4, size, linewidth=1, facecolor=color)
    
    [ax.add_patch(patch(block.offset, block.size, color = colors["unallocated"])) for block in blocks]
    
    for i, unit in enumerate(memory):
        ax.add_patch(patch(i, 1, color = colors[unit]))
    
    
    plt.gca().invert_yaxis()
    plt.yticks([block.offset for block in blocks])
    plt.xticks([])
    plt.show()


global memory
blocks = [5, 10, 15, 10]

blocks = [
    Block(5, 0),
    Block(10, 5),
    Block(15, 15),
    Block(10, 30),
]
memSize = sum([block.size for block in blocks])
memory = ["unallocated" for i in range(memSize)]

for block in blocks:
    process = random.randint(1, block.size)
    block.load(process)

print(memory)


plot(memory, blocks)