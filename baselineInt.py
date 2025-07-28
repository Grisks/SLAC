import matplotlib.pyplot as plt
import numpy as np
from integration import get_values_mv_ns
from averaging import NUM_CSVS, plot_count, FILE_LEN, PMT_NAME, SELF_TRIG, FILE_PATH
from scipy.integrate import simpson
from scipy.stats import norm
from scipy.optimize import curve_fit
from noise import findNoise, gaussian
from trimValues import trimValues

BASELINE_MULT = 3
MIN_VAL = 2

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

def show_all():
    filePaths = ["./OscopeOut/PMT_1_OnLED850/Test_","./OscopeOut/PMT_1_OnLED800/Test_", "./OscopeOut/PMT_1_OnLED760/Test_","./OscopeOut/PMT_1_OnLED730/Test_","./OscopeOut/PMT_1_OnLED700/Test_"]

    for file in filePaths:
        values = get_values_mv_ns(NUM_CSVS, file=file)
        plt.hist(baseLineInt(values),100, label=file)
        plt.legend()
    plt.savefig("PMT_1_Integration")
    plt.show()    

def save_baseline(file_prefix, file_suffix, FileName = FILE_PATH):
    values = get_values_mv_ns(NUM_CSVS, file=FileName)
    ints = baseLineInt(values)


    hist_data = plt.hist(ints, 50)

    mean_g, stddev_g = norm.fit(ints)

    popt, pcov = curve_fit(gaussian,[(hist_data[1][i]+hist_data[1][i+1])/2 for i in range(1,50)], hist_data[0][1:50], p0=(100, mean_g, stddev_g) )

    error = np.round(np.sqrt(np.diag(pcov)),2)

    print(error)

    print(f"Mean Area: {popt[1]}+-{error[1]}")
    print(f"Stddev: {popt[2]}+-{error[2]}")

    plt.text(popt[1]+1.2*popt[2],60,f"Mean Area: {np.round(popt[1],2)}+-{error[1]}")
    plt.text(popt[1]*1.2*popt[2],50,f"Stddev: {np.round(popt[2],2)}+-{error[2]}")

    #x = np.linspace(0,5*np.round(popt[1],0),1000)
    #plt.plot(x,gaussian(x,popt[0],popt[1],popt[2]))

    plt.title(f"Noise reduced pulse area with {NUM_CSVS} counts for PMT {PMT_NAME}")

    plt.xlabel("Pulse Area (mVns)")
    plt.ylabel("Counts")

    if file_suffix != "" and file_prefix != "":
        plt.savefig(f"{file_prefix}/BaseLineIntegration_{file_suffix}")


if __name__ == "__main__":
    #save_baseline("", "")
    show_all()