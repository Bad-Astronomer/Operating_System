import numpy as np

resources = [9, 3, 6]

currAlloc = np.array([
    [1, 0, 0],
    [6, 1, 2],
    [2, 1, 1],
    [0, 0, 2],
    # [0, 0, 2]
])

maxAlloc = np.array([
    [3, 2, 2],
    [6, 1, 3],
    [3, 1, 4],
    [4, 2, 2],
    # [5, 3, 3]
])

remResources = np.array(resources) - np.sum(currAlloc, axis=0)
run = True

print("Process\tNeed\tRemaining")
while run:
    run = False
    for i, (processAlloc, processMaxAlloc) in enumerate(zip(currAlloc, maxAlloc)):
        remAlloc = processMaxAlloc - processAlloc
        if not max(remAlloc > remResources) and sum(processAlloc):
            run = True
            print(f"P{i + 1}     {remAlloc}  {remResources}")
            remResources += processAlloc
            currAlloc[i] -= currAlloc[i]

if sum(np.sum(currAlloc, axis=1)):
    print("DEADLOCK")