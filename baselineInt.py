import matplotlib.pyplot as plt
import numpy as np
from integration import get_values_mv_ns
from averaging import NUM_CSVS
from scipy.integrate import simpson
from noise import fitNoise

BASELINE_MULT = 4

if __name__ == "__main__":
    values = get_values_mv_ns(1000)
    mean, stddev, __ = fitNoise(values)
    ints = np.zeros(NUM_CSVS)
    for i in range(NUM_CSVS):
        values[i][1] *= -1
        for j in range(640):
            if(values[i][1][j]< mean + BASELINE_MULT * stddev):
                values[i][1][j] = 0
            else:
                values[i][1][j] -=mean + BASELINE_MULT * stddev
    for i in range(NUM_CSVS):
        ints[i] = simpson(values[i][1],values[i][0])
    plt.hist(ints, 10)
    plt.show()
