import matplotlib.pyplot as plt
import numpy as np
from integration import get_values_mv_ns
from averaging import NUM_CSVS, plot_count, FILE_LEN, PMT_NAME, SELF_TRIG
from scipy.integrate import simpson
from scipy.optimize import curve_fit
from noise import findNoise, gaussian
from trimValues import trimValues

BASELINE_MULT = 3
MIN_VAL = 5

def baseLineInt(val):
    values = trimValues(val,MIN_VAL)[0]
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

def save_baseline(file_prefix, file_suffix):
    values = get_values_mv_ns(NUM_CSVS)
    ints = baseLineInt(values)

    

    hist_data = plt.hist(ints, 50)

    popt, pcov = curve_fit(gaussian,[(hist_data[1][i]+hist_data[1][i+1])/2 for i in range(50)], hist_data[0])

    error = np.round(np.sqrt(np.diag(pcov)),2)

    print(error)

    print(f"Mean Area: {popt[1]}+-{error[1]}")
    print(f"Stddev: {popt[2]}+-{error[2]}")

    plt.text(60,60,f"Mean Area: {np.round(popt[1],2)}+-{error[1]}")
    plt.text(60,50,f"Stddev: {np.round(popt[2],2)}+-{error[2]}")

    x = np.linspace(0,5*np.round(popt[1],0),1000)
    plt.plot(x,gaussian(x,popt[0],popt[1],popt[2]))

    plt.title(f"Noise reduced pulse area with {NUM_CSVS} counts for PMT {PMT_NAME}")

    plt.xlabel("Pulse Area (mVns)")
    plt.ylabel("Counts")

    if file_suffix != "" and file_prefix != "":
        plt.savefig(f"{file_prefix}/BaseLineIntegration_{file_suffix}")
    plt.show()


if __name__ == "__main__":
    save_baseline("", "")