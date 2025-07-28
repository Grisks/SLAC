import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

FILE_PATH = "./OscopeOut/PMT_9_800_L/Test_"
PMT_NAME = "LV2477"
NUM_CSVS = 2500
FILE_LEN = 1000
SELF_TRIG = False
MIN_VALUE = 0
VOLTAGE = 800

def parse_csv(file):
    v = pd.read_csv(file, sep=',', header=3)
    if(not SELF_TRIG):
        return np.array([v["# time"].tolist(), v['3'].tolist(), v['1'].tolist()])
    return np.array([v["# time"].tolist(), v['3'].tolist()])

def make_averages():
    arr = []
    for i in range(NUM_CSVS):
        if(not SELF_TRIG):
            if(-(min(parse_csv(f"{FILE_PATH}{i}.csv")[1]))>=MIN_VALUE*(10**-3)):
                arr.append(parse_csv(f"{FILE_PATH}{i}.csv"))
        else:
            arr.append(parse_csv(f"{FILE_PATH}{i}.csv"))
    print(len(arr))
    avv_arr = sum(arr)/len(arr)
    return avv_arr, arr

def plot_count(arr, title):
    plt.plot(arr[0],arr[1])
    if(SELF_TRIG):
        plt.axvline(arr[0][np.argmax(arr[1])], color = "grey", linestyle = '--')
        plt.text(arr[0][np.argmax(arr[1])]+2, -4, f"First reflection delay: {np.round(arr[0][np.argmax(arr[1])]-arr[0][np.argmax(-arr[1])],2)}ns")
    plt.xlim(-100,100)
    plt.xticks(np.linspace(-100,100,11))

    plt.ylabel("Voltage (mV)")
    plt.xlabel("Time (ns)")

    plt.title(title)

    plt.axvline(arr[0][np.argmax(-arr[1])], color = "grey", linestyle = '--')
    plt.text(arr[0][np.argmax(-arr[1])]-34,-np.max(-arr[1]),f"Max Point: {np.round(-np.max(-arr[1]),2)}mV")

    plt.show()

def get_pulses():
    pulses = np.zeros((NUM_CSVS,FILE_LEN))
    for i in range(NUM_CSVS):
        pulses[i] = parse_csv(f"{FILE_PATH}{i}.csv")[2]
    return pulses

if __name__ == "__main__":
    avv, arr = make_averages()
    avv[0] *= 10**9
    avv[1] *= 10**3
    if(not SELF_TRIG):
        pulses = get_pulses()
    
    for j in range(10):
        
        i = random.randint(0,len(arr))

        plt.figure(figsize=(10, 8))
        signal = arr[i][1]
        # Compute the FFT
        plt.subplot(2, 1, 1)

        N = len(signal)

        sampling_rate = 1/(arr[i][0][1]-arr[i][0][0])
        fourier_transform = np.fft.fft(signal)
        frequencies = np.fft.fftfreq(N, d=1/sampling_rate)
        amplitude_spectrum = fourier_transform

        plt.plot(frequencies, np.abs(amplitude_spectrum))
        plt.xlim(0,sampling_rate/10)

        plt.subplot(2,1,2)
        
        plt.plot(frequencies, np.angle(amplitude_spectrum))
        plt.xlim(0,sampling_rate/10)
        plt.show()

        plt.plot(arr[i][0]*10**9,arr[i][1]*10**3)
        if(not SELF_TRIG):
            plt.plot(arr[i][0]*10**9, (pulses[i]*10)-30)
        plt.show()
        
    plot_count(avv, "Averaged voltage over 2500 different Dark counts in PMT")