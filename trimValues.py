import numpy as np

def trimValues(values, threshold):
    count = 0
    for i in range(len(values)):
        if(max(-values[i][1])>=threshold):
            count += 1
    trimmed = np.zeros((count+1, 2, len(values[0][1])))
    indices = np.zeros(count+1)

    num = 0
    for i in range(len(values)):
        if(max(-values[i][1])>=threshold):
            trimmed[num] = values[i]
            num += 1
            indices[num] = i
    return trimmed, indices