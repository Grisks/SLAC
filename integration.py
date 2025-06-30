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

def integration(values, num_csvs):
    out = np.zeros(num_csvs)
    for i in range(num_csvs):
        out[i] = integrate.simpson(values[i][1],values[i][0])
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

                frtol +=0.0005
                first_spots = np.isclose(half_max,-split_values[0],frtol,fatol)

            elif(np.sum(first_spots) > 1):

                frtol -=0.0005
                first_spots = np.isclose(half_max,-split_values[0],frtol,fatol)
            
            if(np.sum(second_spots) < 1):

                srtol +=0.0005
                second_spots = np.isclose(half_max,-split_values[1],srtol,satol)

            elif(np.sum(second_spots) > 1):

                srtol -=0.0005
                second_spots = np.isclose(half_max,-split_values[1],srtol,satol)
            if(num_it > 200):
                print("Could not find just two values")
                break

        two_indexes = (np.nonzero(first_spots)[0], np.nonzero(second_spots)[0]+ len(split_values[0]))
        two_times = (values[i][0][two_indexes[0]],values[i][0][two_indexes[1]])
        fwhm[i] = abs(two_times[0][0] - two_times[1][0])
        times[i] = [two_times[0][0], two_times[1][0]]
        print(fwhm[i])
    return (fwhm, times)

if __name__ == "__main__":
    values = get_values_mv_ns(1000)
    fwhm, times = findFwhm(values, 1000)

    average = make_averages()
    average[0]*= 10**9
    average[1]*= 10**3
    fig, axs = plt.subplots(1, 2, sharey=False, tight_layout=True)
    fig.set_figheight(8)
    fig.set_figwidth(10)

    num_out = 0
    for i in range(1000):
        if(fwhm[i] > 5):
            num_out += 1
            fwhm[i] = 5
    print(num_out)
    axs[0].hist(fwhm, bins=20)
    axs[1].hist(integration(values,1000), bins=50)
    plt.show()