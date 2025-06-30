import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FILE_PATH = "./OscopeOut/TestTrace"
NUM_CSVS = 10


def parse_csv(file):
    v = pd.read_csv(file, sep=',', header=3)
    return np.array([v["# time"].tolist(), v['1'].tolist()])

def make_averages():
    arr = np.zeros((NUM_CSVS,2,640))
    for i in range(NUM_CSVS):
        arr[i] = parse_csv(f"{FILE_PATH}{i}.csv")
    avv_arr = np.average(arr, 0)
    return avv_arr

def plot_count(arr, title):
    plt.plot(arr[0],arr[1])
    plt.xticks(np.linspace(-50,50,11))

    plt.ylabel("Voltage (mV)")
    plt.xlabel("Time (ns)")

    plt.title(title)

    plt.axvline(arr[0][np.argmax(-arr[1])], color = "grey", linestyle = '--')
    plt.text(arr[0][np.argmax(-arr[1])]-34,-np.max(-arr[1]),f"Max Point: {np.round(-np.max(-arr[1]),2)}mV")

    plt.axvline(arr[0][np.argmax(arr[1])], color = "grey", linestyle = '--')
    plt.text(arr[0][np.argmax(arr[1])]+2, -4, f"First reflection delay: {np.round(arr[0][np.argmax(arr[1])]-arr[0][np.argmax(-arr[1])],2)}ns")

    plt.show()


if __name__ == "__main__":
    #one = parse_csv(f"{FILE_PATH}1.csv")
    #plot_count([one[0]*10**9,one[1]], )
    avv = make_averages()
    avv[0] = avv[0] * 10**9
    plot_count(avv, "Averaged voltage over 10 different Dark counts in PMT")