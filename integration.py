from scipy import integrate, interpolate
from scipy.stats import norm
from scipy.optimize import curve_fit
from averaging import make_averages, parse_csv, FILE_PATH, FILE_LEN, NUM_CSVS, PMT_NAME, SELF_TRIG
import numpy as np
import matplotlib.pyplot as plt
import time
from trimValues import trimValues

NUM_AROUND = 15

def gaussian(x, amplitude, mean, sigma):
    return amplitude * np.exp(-(x - mean)**2 / (2 * sigma**2))

def area_around_pulse(values):
    areas = np.zeros(len(values))

    for i in range(len(values)):
        pulseIndex = np.argmax(-values[i][1])
        if(pulseIndex>100 and pulseIndex<900):
            areaRange = [pulseIndex-NUM_AROUND*5, pulseIndex+NUM_AROUND*5]
        elif (pulseIndex <=100):
            areaRange = [0, pulseIndex+NUM_AROUND*5]
        elif (pulseIndex >=900):
            areaRange = [pulseIndex-NUM_AROUND*5, 999]
        areas[i] = integrate.simpson(-values[i][1][areaRange[0]:areaRange[1]], x=values[i][0][areaRange[0]:areaRange[1]])
    return areas

def get_values_mv_ns(num_csvs, file=FILE_PATH):
    arr = np.zeros((num_csvs,2,FILE_LEN))
    for i in range(num_csvs):
        arr[i] = parse_csv(f"{file}{i}.csv")[:2]
        arr[i][0]*=10**9
        arr[i][1]*=10**3
    return arr

def integration(values, _num_csvs):
    out = np.zeros(len(values))
    for i in range(len(values)):
        out[i] = integrate.simpson(-values[i][1],x=values[i][0])
        #plot_count(values[i],f"Plot: {i}")
    return out

def findFwhm(values, numcsvs):
    fwhm = np.zeros(numcsvs)
    times = np.zeros([numcsvs,2])
    for i in range(numcsvs):
        num_it = 0
        frtol = 0.08
        fatol = 0.00
        srtol = 0.08
        satol = 0.00

        half_max = np.max(-values[i][1])/2

        split_values = np.array_split(values[i][1], [np.argmax(-values[i][1])])

        first_spots = np.isclose(half_max,-split_values[0],frtol,fatol)

        second_spots = np.isclose(half_max,-split_values[1],srtol,satol)

        while (np.sum(first_spots) != 1 or np.sum(second_spots) != 1):
            num_it += 1
            if(np.sum(first_spots) < 1):

                frtol +=0.005
                first_spots = np.isclose(half_max,-split_values[0],frtol,fatol)

            elif(np.sum(first_spots) > 1):

                frtol -=0.005
                first_spots = np.isclose(half_max,-split_values[0],frtol,fatol)
            
            if(np.sum(second_spots) < 1):

                srtol +=0.005
                second_spots = np.isclose(half_max,-split_values[1],srtol,satol)

            elif(np.sum(second_spots) > 1):

                srtol -=0.005
                second_spots = np.isclose(half_max,-split_values[1],srtol,satol)
            if(num_it > 1000):
                print("Could not find just two values")
                break

        two_indexes = (np.nonzero(first_spots)[0], np.nonzero(second_spots)[0]+ len(split_values[0]))
        two_times = (values[i][0][two_indexes[0]],values[i][0][two_indexes[1]])
        fwhm[i] = abs(two_times[0][0] - two_times[1][0])
        times[i] = [two_times[0][0], two_times[1][0]]
        print(fwhm[i])
    return (fwhm, times)

def save_integration( file_prefix, file_suffix, FileName=FILE_PATH):
    values = get_values_mv_ns(NUM_CSVS, file=FileName)

    average = make_averages()
    average[0][0]*= 10**9
    average[0][1]*= 10**3

    #for i in range(2500):
        #if(fwhm[i] > 5):
        #    num_out += 1
        #    fwhm[i] = 5
    #axs[0].hist(fwhm, bins=20)
    ints = integration(values,2500)
    
    areas = area_around_pulse(values)

    mean, stddev = norm.fit(ints)
    hist_data = plt.hist(ints, bins=100)
    popt, pcov = curve_fit(gaussian,[hist_data[1][i] for i in range(100)], hist_data[0], p0=(200,mean,stddev))

    perr = np.round(np.sqrt(np.diag(pcov)),2)
    mean = popt[1]
    stddev = popt[2]

    plt.text(mean+1.5*stddev, 55, f"Mean: {np.round(mean,2)}+-{np.round(perr[1],2)}")
    plt.text(mean+1.5*stddev, 45, f"Stddev: {np.round(stddev,2)}+-{np.round(perr[2],2)}")

    plt.title(f"Pulse area with {NUM_CSVS} counts for PMT {PMT_NAME}")
    plt.xlabel("Pulse Area (mVns)")
    plt.ylabel("Counts")
    if file_suffix != "" and file_prefix != "":
        plt.savefig(f"{file_prefix}/Integration_{file_suffix}")
    plt.show()

    plt.hist(areas, 40, range=(-5,75))
    plt.xlabel("Pulse Area (mVns)")
    plt.ylabel("Counts")
    plt.title("Pulse area localized to +-15ns around pulse at 800V")
    plt.savefig("./PulseArea800")
    plt.show()

if __name__ == "__main__":
    save_integration("","")