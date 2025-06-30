import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, chisquare
from scipy.optimize import curve_fit
from integration import get_values_mv_ns
from averaging import NUM_CSVS
from math import pi, sqrt, exp

NOISE_DEPTH = 100

def gaussian(x, amplitude, mean, sigma):
    return amplitude * np.exp(-(x - mean)**2 / (2 * sigma**2))

def fitNoise(values):
    modVals = np.zeros((NUM_CSVS, NOISE_DEPTH))
    for i in range(NUM_CSVS):
        modVals[i] = values[i][1][:NOISE_DEPTH]
    comb_data = modVals.flatten()
    mean, stddev = norm.fit(comb_data)
    
    x = np.linspace(-5* stddev + mean, 5 * stddev + mean, 1000)
    #pdf = 1 / (stddev * sqrt(2*pi)) * np.exp((-1/2)*(((x-mean)/stddev)**2))
    pdf = [gaussian(x[i],1  / (stddev * sqrt(2*pi)),mean,stddev) for i in range(len(x))]

    print(f"Mean: {mean}, Standard Deviation: {stddev}")

    hist_data = plt.hist(comb_data, 15, density=True)

    expected = [gaussian(hist_data[1][i], 1  / (stddev * sqrt(2*pi)), mean, stddev) for i in range(15)]
    goodness, p_value = chisquare(hist_data[0], expected, sum_check=False)

    print(f"ChiSquare stat: {goodness}, p_value: {p_value}")

    popt, pcov = curve_fit(gaussian, [(hist_data[1][i]+hist_data[1][i+1])/2 for i in range(15)], hist_data[0], bounds=([1  / (stddev * sqrt(2*pi))-0.001,-10,0],[1  / (stddev * sqrt(2*pi)),10,2]))

    print(popt)
    perr = np.sqrt(np.diag(pcov))
    print(perr)

    print(f"Mean diff: {popt[1]-mean}, Standard Deviation diff: {popt[2]-stddev}")

    plt.plot(x, pdf)
    plt.show()

    

if __name__ == "__main__":
    values = get_values_mv_ns(NUM_CSVS)
    fitNoise(values)