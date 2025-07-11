import matplotlib.pyplot as plt
import numpy as np
from integration import get_values_mv_ns
from averaging import NUM_CSVS, plot_count, FILE_LEN, PMT_NAME, SELF_TRIG
from scipy.integrate import simpson
from noise import findNoise
from trimValues import trimValues

BASELINE_MULT = 3

def baseLineInt(val):
    values = trimValues(val,6)[0]
    ints = np.zeros(len(values))

    for i in range(len(values)):
        mean, stddev = findNoise(values[i])
        values[i][1] *= -1
        for j in range(FILE_LEN):
            if(values[i][1][j]< mean + BASELINE_MULT * stddev):
                values[i][1][j] = 0
            else:
                values[i][1][j] -=mean + BASELINE_MULT * stddev
        
    for i in range(len(values)):
        ints[i] = simpson(values[i][1],values[i][0])
    
    return ints

def save_baseline(file_suffix):
    values = get_values_mv_ns(NUM_CSVS)
    ints = baseLineInt(values)

    plt.hist(ints, 50, range=(0,200))

    plt.title(f"Noise reduced pulse area with {NUM_CSVS} counts for PMT {PMT_NAME}")

    plt.xlabel("Pulse Area (mVns)")
    plt.ylabel("Counts")
    if file_suffix != "":
        plt.savefig(f"./figures/BaseLineIntegration_{file_suffix}")
    plt.show()


if __name__ == "__main__":
    save_baseline("")