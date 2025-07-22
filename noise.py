import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, chisquare
from scipy.optimize import curve_fit
from integration import get_values_mv_ns
from averaging import NUM_CSVS, PMT_NAME, SELF_TRIG, FILE_PATH
from math import pi, sqrt

NOISE_DEPTH = 100

def show_all_noise():
    filePaths = ["./OscopeOut/PMT_3_850/Test_","./OscopeOut/PMT_3_800/Test_", "./OscopeOut/PMT_3_750/Test_","./OscopeOut/PMT_3_700/Test_","./OscopeOut/PMT_3_650/Test_","./OscopeOut/PMT_3_600/Test_"]

    for file in filePaths:
        save_noise("","", FileName=file)
    plt.savefig("./figures/LV2464/Noise")
    plt.show()

def gaussian(x, amplitude, mean, sigma):
    return amplitude * np.exp(-(x - mean)**2 / (2 * sigma**2))

def findNoise(value):
    mean, stddev = norm.fit(value[1][:NOISE_DEPTH])
    return (mean, stddev)

def fitNoise(values):
    modVals = np.zeros((NUM_CSVS, NOISE_DEPTH))
    for i in range(NUM_CSVS):
        modVals[i] = values[i][1][:NOISE_DEPTH]
    comb_data = modVals.flatten()
    mean, stddev = norm.fit(comb_data)

    hist_data = plt.hist(comb_data, 15, density=True)
    plt.close()
    return (mean, stddev, hist_data, comb_data)

def evaluateFit(hist_data, mean, stddev):
    expected = [gaussian(hist_data[1][i], 1  / (stddev * sqrt(2*pi)), mean, stddev) for i in range(15)]
    goodness, p_value = chisquare(hist_data[0], expected, sum_check=False)

    print(f"ChiSquare stat: {goodness}, p_value: {p_value}")

    popt, pcov = curve_fit(gaussian, [(hist_data[1][i]+hist_data[1][i+1])/2 for i in range(15)], hist_data[0], bounds=([1  / (stddev * sqrt(2*pi))-0.001,-10,0],[1  / (stddev * sqrt(2*pi)),10,2]))
    perr = np.sqrt(np.diag(pcov))
    return popt, perr



def save_noise(file_prefix, file_suffix, FileName=FILE_PATH):
    values = get_values_mv_ns(NUM_CSVS, file=FileName)
    mean, stddev, hist_data, comb_data = fitNoise(values)

    popt, perr = evaluateFit(hist_data, mean, stddev)

    x = np.linspace(-4*stddev+mean,4*stddev+mean)
    y = gaussian(x, 1  / (stddev * sqrt(2*pi)), mean, stddev)

    plt.figure(figsize=(10,8))

    print(f"Mean {popt[1]}+-{perr[1]}, Stddev: {popt[2]}+-{perr[2]}")

    plt.hist(comb_data, 10, density=True)
    plt.title(f"Noise levels across {NUM_CSVS} counts from PMT {PMT_NAME}")

    plt.xlabel("Noise level (mv)")
    plt.ylabel("Noise readings at level")

    plt.plot(x,y)
    if file_suffix != "" and file_prefix != "":
        plt.savefig(f"{file_prefix}/Noise_{file_suffix}")
    plt.show()


if __name__ == "__main__":
    show_all_noise()