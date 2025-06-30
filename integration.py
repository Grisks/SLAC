from scipy import integrate, interpolate
from averaging import make_averages, parse_csv, FILE_PATH, plot_count
import numpy as np
import matplotlib.pyplot as plt
import time



def get_values_mv_ns(num_csvs):
    arr = np.zeros((num_csvs,2,640))
    for i in range(num_csvs):
        arr[i] = parse_csv(f"{FILE_PATH}{i}.csv")
        arr[i][0]*=10**9
        arr[i][1]*=10**3
    return arr

values = get_values_mv_ns(10)

def integration(values, num_csvs):
    out = np.zeros(10)
    for i in range(num_csvs):
        out[i] = integrate.simpson(values[i][1],values[i][0])
        #plot_count(values[i],f"Plot: {i}")
    return out

print(integrate.simpson(make_averages()[1]*10**3,make_averages()[0]*10**9))

def findFwhm(values, numcsvs):
    fwhm = np.zeros(numcsvs)
    times = np.zeros([numcsvs,2])
    for i in range(numcsvs):

        frtol = 0.08
        fatol = 0.00
        srtol = 0.08
        satol = 0.00

        half_max = np.max(-values[i][1])/2

        split_values = np.array_split(values[i][1], [np.argmax(-values[i][1])])

        first_spots = np.isclose(half_max,-split_values[0],frtol,fatol)

        second_spots = np.isclose(half_max,-split_values[1],srtol,satol)

        while (np.sum(first_spots) != 1 or np.sum(second_spots) != 1):
            if(np.sum(first_spots) < 1):

                frtol +=0.001
                first_spots = np.isclose(half_max,-split_values[0],frtol,fatol)

            elif(np.sum(first_spots) > 1):

                frtol -=0.001
                first_spots = np.isclose(half_max,-split_values[0],frtol,fatol)
            
            if(np.sum(second_spots) < 1):

                srtol +=0.001
                second_spots = np.isclose(half_max,-split_values[1],srtol,satol)

            elif(np.sum(second_spots) > 1):

                srtol -=0.001
                second_spots = np.isclose(half_max,-split_values[1],srtol,satol)

        two_indexes = (np.nonzero(first_spots)[0], np.nonzero(second_spots)[0]+ len(split_values[0]))
        two_times = (values[i][0][two_indexes[0]],values[i][0][two_indexes[1]])
        fwhm[i] = abs(two_times[0][0] - two_times[1][0])
        times[i] = [two_times[0][0], two_times[1][0]]
    return (fwhm, times)

if __name__ == "__main__":
    fwhm, times = findFwhm(values, 10)
    plt.plot(values[2][0][200:400],-values[2][1][200:400])
    plt.hlines(np.max(-values[2][1])/2, times[2][0], times[2][1],colors='grey', linestyles='--', )
    #plt.text(two_times[1]+5,half_max, f"FWHM: {np.round(fwhm[i],2)}")

    plt.show()
    print(fwhm)

    average = make_averages()
    average[0]*= 10**9
    average[1]*= 10**3

    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
    axs[0].hist(fwhm, bins=5)
    axs[1].hist(integration(values,10), bins=5)
    plt.show()