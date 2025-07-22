from integration import get_values_mv_ns
from averaging import NUM_CSVS, PMT_NAME, SELF_TRIG, FILE_PATH
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from noise import gaussian
from math import pi, sqrt

MINVALUE = 0
MAXVALUE = 1000

def show_all_pulse_heights():
    filePaths = ["./OscopeOut/PMT_1_OnLED850/Test_","./OscopeOut/PMT_1_OnLED800/Test_", "./OscopeOut/PMT_1_OnLED760/Test_","./OscopeOut/PMT_1_OnLED730/Test_","./OscopeOut/PMT_1_OnLED700/Test_"]
    for file in filePaths:
        save_pulse_heights("","", FileName=file)
    plt.savefig("./figures/LV2472/Heights")
    plt.show()

def save_pulse_heights(file_prefix, file_suffix, FileName=FILE_PATH):
    values = get_values_mv_ns(NUM_CSVS, file=FileName)
    
    numMatches = 0
    for i in range(NUM_CSVS):
        if(np.max(-values[i][1]) >= MINVALUE and np.max(-values[i][1]) <= MAXVALUE):
            numMatches += 1

    maxes = np.zeros(numMatches)
    print(len(maxes))
    allMaxes = np.zeros(NUM_CSVS)

    valuesInd = 0
    for i in range(NUM_CSVS):
        if(np.max(-values[i][1]) >= MINVALUE and np.max(-values[i][1]) <= MAXVALUE):
            maxes[valuesInd] = np.max(-values[i][1])
            valuesInd += 1
        allMaxes[i] = np.max(-values[i][1])
    
    mean, stddev = norm.fit(maxes)
    print(mean)
    print(stddev)

    x = np.linspace(0,30,1000)
    y = np.zeros(1000)
    
    for i in range(1000):
        y[i] = gaussian(x[i],1  / (stddev * sqrt(2*pi)),mean, stddev) /(len(allMaxes)/len(maxes))
    
    #plt.plot(x,y)

    plt.hist(maxes, 50, density=False, label=FileName,range=(0,30))
    plt.title(f"Pulse height count with {NUM_CSVS} counts on PMT {PMT_NAME}")
    plt.legend()
    plt.xlabel("Max height of pulse (mV)")
    plt.ylabel("Number of Pulses")
    if file_suffix != "" and file_prefix != "":
        plt.savefig(f"{file_prefix}/PulseHeight_{file_suffix}")


if __name__ == "__main__":
    save_pulse_heights("", "", FILE_PATH)
    #show_all_pulse_heights()
    plt.show()
