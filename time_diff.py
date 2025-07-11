from averaging import get_pulses, NUM_CSVS
from integration import get_values_mv_ns
import numpy as np
import matplotlib.pyplot as plt

def get_diff(time, pulses, values):
    diff = np.abs(time[np.argmax(-values)] - time[np.argmax(pulses)])
    return diff

def get_diffs(values, pulses):
    diffs = np.zeros(len(pulses))
    for i in range(len(pulses)):
        diffs[i] = get_diff(values[i][0], pulses[i], values[i][1])
    return diffs

if __name__ == "__main__":
    values = get_values_mv_ns(NUM_CSVS)
    pulses = get_pulses()

    diffs = get_diffs(values, pulses)

    under20 = []
    above20 = []

    plt.hist(diffs,100, range=(0,120))
    for i, diff in enumerate(diffs):
        if(diff<=20):
            under20.append(np.abs(np.min(values[i][1])))
        elif(diff<=60):
            above20.append(np.abs(np.min(values[i][1])))
    plt.show()

    fig, axs = plt.subplots(1, 2, sharey=False, tight_layout=True)
    fig.set_figheight(8)
    fig.set_figwidth(10)

    axs[0].hist(under20,20)
    axs[1].hist(above20,20)
    plt.show()