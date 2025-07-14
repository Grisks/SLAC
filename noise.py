import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, chisquare
from scipy.optimize import curve_fit
from integration import get_values_mv_ns
from averaging import NUM_CSVS, PMT_NAME, SELF_TRIG
from math import pi, sqrt

NOISE_DEPTH = 100

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



def save_noise(file_prefix, file_suffix):
    values = get_values_mv_ns(NUM_CSVS)
    mean, stddev, __, comb_data = fitNoise(values)

    x = np.linspace(-4*stddev+mean,4*stddev+mean)
    y = gaussian(x, 1  / (stddev * sqrt(2*pi)), mean, stddev)

    plt.figure(figsize=(10,8))

    plt.hist(comb_data, 10, density=True)
    plt.title(f"Noise levels across {NUM_CSVS} counts from PMT {PMT_NAME}")

    plt.xlabel("Noise level (mv)")
    plt.ylabel("Noise readings at level")

    plt.plot(x,y)
    if file_suffix != "" and file_prefix != "":
        plt.savefig(f"{file_prefix}/Noise_{file_suffix}")

    plt.show()

if __name__ == "__main__":
    save_noise("", "")