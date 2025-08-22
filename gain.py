import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# PMT1: LV2475
# PMT2: LV2476
# PMT3: LV2477
# PMT4: LV2454
# PMT5: LV2459 
# PMT6: LV2455 Improper gain on initial run
# PMT7: LV2461 Improper gain on initial run
# PMT8: LV2456
# PMT9: LV2460
# PMT10: LV2462
# PMT11: LV2457
# PMT12: LV2464

# When adding data, add Heights, Area and Area Error 
# Add line to plot new data and change plot file prefix
# Calculate number of photons using low LED and high LED pulse heights
PREFIX = "./Figures/LV2464/LV2464L"

VOLTAGES = [400, 500, 600, 700, 800, 850]
VOLTAGES2 = [400,500,600,800,850]

HEIGHTS_1 = [3.52, 22.06, 111.97, 425.62, 1267.1, 2054.2]
HEIGHTS_E_1 = [0.03, 0.19, 0.74, 3.08, 11.5, 3.21]

AREA_1 = [20.69, 227.51, 1212.5, 4896.4, 12191, 19660] 


HEIGHTS_2 = [2.88, 18.84, 95.67, 371, 1186, 1854] #Mean pulse height in mV
HEIGHTS_E_2 = [.1, .23, 1.1, 0.63, 11.1, 6.86] #Fitting Error in mVns

AREA_2 = [11.54, 205.82, 1012, 4047, 11498, 17990] # Mean pulse area in mVns
AREA_E_2 = [.17, .28, 1.17, 4.63, 17.31, 21.63] # Fitting Error in mv


HEIGHTS_3 = [1.45, 5.77, 28.11, 319.6, 498]

AREA_3 = [5, 39.4, 283.4, 3434, 5671]
AREA_E_3 = [.12, 0.19, .43, 5, 6.6]


HEIGHTS_4 = [3.09, 21.93, 106.7, 404.6, 1240, 1982]

AREA_4 = [5.29, 206.4, 1164, 4789, 11052, 18329]
AREA_E_4 = [0.15, .37, 1.42, 4.73, 13.4, 29.17]


HEIGHTS_5 = [3.11, 22.05, 108.5, 408.1, 1249, 1993.7]

AREA_5= [1.72, 208.4, 1235.45, 4416, 11490, 18751.2]
AREA_E_5 = [0.14, 0.34, 1.32, 4.6, 12, 19.09]


HEIGHTS_6 = [2.64, 18.6, 88.57, 333.04, 1057.9, 1706]

AREA_6 = [1.5, 170.86, 1041.8, 3653.1, 9631, 15992]
AREA_E_6 = [.5, .3, 1.5, 5.5, 14, 21.2]


HEIGHTS_7 = [2.17, 15.08, 74.7, 284.3, 888, 1430.1]

AREA_7 = [3, 121.2, 886.5, 3180.8, 7946, 13098]
AREA_E_7 = [0.2, .26, 1.4, 3.6, 13, 20]


HEIGHTS_8 = [3.11, 21.81, 105.8, 399.1, 1194, 1899.8]

AREA_8 = [1, 192.5, 1244, 4872, 10571, 17437]
AREA_E_8 = [0.2, .33, 1.4, 4.7, 15.7, 25.5]


HEIGHTS_9 = [2.74, 19.74, 96.43, 373.2, 1190, 1861]

AREA_9 = [4, 191.03, 1120, 4021.5, 10556, 17060]
AREA_E_9 = [.2, .3, 1.4, 4.5, 17, 23]


HEIGHTS_10 = [3.75, 27.03, 136.2, 510.9, 1538, 2404]

AREA_10 = [1.5, 246.6, 1495.8, 5956, 14177.8, 22726]
AREA_E_10 = [0.3, .4, 2.1, 7, 16.6, 21]


HEIGHTS_11 = [2.62, 18.2, 88.98, 336.2, 1032, 1693]

AREA_11 = [9.26, 169.0, 1036.05, 3664.82, 9477.5, 16125]
AREA_E_11 = [0.09, .26, 1.2, 5.16, 15, 21.6]

HEIGHTS_12 = [2.37, 16.96, 81.82, 307.5, 937.9, 1517.6]

AREA_12 = [1, 154.19, 982.9, 3416.4, 8253.4, 13761]
AREA_E_12 = [0.1, 0.24, 1.2, 3.6, 12.8, 18.7]

NUM_PHO1 = 86 #Number of photons per pulse
NUM_PHO2 = 86 
NUM_PHO3 = 65 
NUM_PHO4 = 90
NUM_PHO5 = 110
NUM_PHO6 = 83
NUM_PHO7 = 87
NUM_PHO8 = 90
NUM_PHO9 = 90
NUM_PHO10 = 110
NUM_PHO11 = 90
NUM_PHO12 = 92

REFF = 50 #Need to calculate more definitively
Q = 1.602 * 10 ** -19 #Charge of Electron
def gain(area):
    return area * (10**-12) / (REFF * Q)

def gainToArea(gain):
    return gain * (REFF * Q)/(10**-12)

def power(a, D, b, c):
    return (D/(10**6)) * a**b + c

Gain1 = gain(np.array(AREA_1))/(NUM_PHO1*2) #set single photon gain by converting area to gain and divide by number of photons making up area
Gain2 = gain(np.array(AREA_2))/(NUM_PHO2*2)
Gain3 = gain(np.array(AREA_3))/(NUM_PHO3*2)
Gain4 = gain(np.array(AREA_4))/(NUM_PHO4*2)
Gain5 = gain(np.array(AREA_5))/(NUM_PHO5*2)
Gain6 = gain(np.array(AREA_6))/(NUM_PHO6*2)
Gain7 = gain(np.array(AREA_7))/(NUM_PHO7*2)
Gain8 = gain(np.array(AREA_8))/(NUM_PHO8*2)
Gain9 = gain(np.array(AREA_9))/(NUM_PHO9*2)
Gain10 = gain(np.array(AREA_10))/(NUM_PHO10*2)
Gain11 = gain(np.array(AREA_11))/(NUM_PHO11*2)
Gain12 = gain(np.array(AREA_12))/(NUM_PHO12*2)

totalVoltage = np.zeros(40)

for i in range(5):
    for j in range(8):
        totalVoltage[j+i*8] = VOLTAGES[i]

totalGain = np.zeros(40)

for i in range(5):
    totalGain[8*i] = Gain1[i]
    totalGain[8*i+1] = Gain2[i]
    totalGain[8*i+2] = Gain4[i]
    totalGain[8*i+3] = Gain5[i]
    totalGain[8*i+4] = Gain6[i]
    totalGain[8*i+5] = Gain7[i]
    totalGain[8*i+6] = Gain8[i]
    totalGain[8*i+7] = Gain9[i]

popt, pcov = curve_fit(power, totalVoltage/10, totalGain, (.1,7.2,0), bounds=((-np.inf,-np.inf, -40000), (np.inf, np.inf, np.inf)))
x = np.linspace(400,850,90)/10

print(popt)

y = power(x,popt[0],popt[1],popt[2])

plt.loglog(x*10,y, label = "approx")
plt.plot(VOLTAGES, Gain1, label="LV2475")
plt.plot(VOLTAGES, Gain2, label="LV2476")
plt.plot(VOLTAGES, Gain4, label="LV2454")
plt.plot(VOLTAGES, Gain5, label="LV2459")
plt.plot(VOLTAGES, Gain6, label="LV2455")
plt.plot(VOLTAGES, Gain7, label="LV2461")
plt.plot(VOLTAGES, Gain8, label="LV2456")
plt.plot(VOLTAGES, Gain9, label="LV2460")


plt.legend()
plt.show()

plt.plot(VOLTAGES, AREA_1, label="LV2475")
plt.plot(VOLTAGES, AREA_2, label="LV2476")
plt.plot(VOLTAGES2, AREA_3, label="LV2477")
plt.plot(VOLTAGES, AREA_4, label="LV2454")
plt.plot(VOLTAGES, AREA_5, label="LV2459")
plt.plot(VOLTAGES, AREA_6, label="LV2455")
plt.plot(VOLTAGES, AREA_7, label="LV2461")
plt.plot(VOLTAGES, AREA_8, label="LV2456")
plt.plot(VOLTAGES, AREA_9, label="LV2460")
plt.plot(x*10, gainToArea(y*87*2), label="Approx")
plt.plot(VOLTAGES, gainToArea(Gain1*86*2), label="ApproxGain1")

plt.legend()
plt.show()

smallVolt = [700, 800, 850]
smallArea = [11, 44, 87]
plt.plot(smallVolt, smallArea)
plt.plot(x*10, gainToArea(y), label="Approx")
plt.show()

plt.errorbar(VOLTAGES, HEIGHTS_1, HEIGHTS_E_1, xerr=[2,2,2,2,3,3], label="LV2475")
plt.errorbar(VOLTAGES, HEIGHTS_2, HEIGHTS_E_2, xerr=[2,2,2,2,3,3], label="LV2476")
plt.errorbar(VOLTAGES2, HEIGHTS_3, xerr=[2,2,2,3,3], label="LV2477")
plt.errorbar(VOLTAGES, HEIGHTS_4, xerr=[2,2,2,2,3,3], label="LV2454")
plt.errorbar(VOLTAGES, HEIGHTS_5, xerr=[2,2,2,2,3,3], label="LV2459")
plt.errorbar(VOLTAGES, HEIGHTS_6, xerr=[2,2,2,2,3,3], label="LV2455")
plt.errorbar(VOLTAGES, HEIGHTS_7, xerr=[2,2,2,2,3,3], label="LV2461")
plt.errorbar(VOLTAGES, HEIGHTS_8, xerr=[2,2,2,2,3,3], label="LV2456")
plt.errorbar(VOLTAGES, HEIGHTS_9, xerr=[2,2,2,2,3,3], label="LV2460")
plt.errorbar(VOLTAGES, HEIGHTS_10, xerr=[2,2,2,2,3,3], label="LV2462")
plt.errorbar(VOLTAGES, HEIGHTS_11, xerr=[2,2,2,2,3,3], label="LV2457")
plt.errorbar(VOLTAGES, HEIGHTS_12, xerr=[2,2,2,2,3,3], label="LV2464")

plt.legend()

plt.title("PMT Pulse Heights with 100 photon input on PMT")
plt.xlabel("Bias Voltage (V)")
plt.ylabel("Mean Pulse Height (mV)")
plt.savefig(f"{PREFIX}/HeightsComp")
plt.show()

plt.plot(VOLTAGES, HEIGHTS_1, label="LV2475")
plt.plot(VOLTAGES, HEIGHTS_2, label="LV2476")
plt.plot(VOLTAGES2, HEIGHTS_3, label="LV2477")
plt.plot(VOLTAGES, HEIGHTS_4, label="LV2454")
plt.plot(VOLTAGES, HEIGHTS_5, label="LV2459")
plt.plot(VOLTAGES, HEIGHTS_6, label="LV2455")
plt.plot(VOLTAGES, HEIGHTS_7, label="LV2461")
plt.plot(VOLTAGES, HEIGHTS_8, label="LV2456")
plt.plot(VOLTAGES, HEIGHTS_9, label="LV2460")
plt.plot(VOLTAGES, HEIGHTS_10, label="LV2462")
plt.plot(VOLTAGES, HEIGHTS_11, label="LV2457")
plt.plot(VOLTAGES, HEIGHTS_12, label="LV2464")

plt.legend()
plt.xscale("log")
plt.yscale("log")

plt.title("Log-Log plot of Height vs Bias for 100 photon")
plt.xlabel("Bias Voltage (V)")
plt.ylabel("Mean Pulse Height (mV)")
plt.savefig(f"{PREFIX}/HeightsCompL")
plt.show()

plt.plot(VOLTAGES, AREA_1, label="LV2475")
plt.plot(VOLTAGES, AREA_2, label="LV2476")
plt.plot(VOLTAGES2, AREA_3, label="LV2477")
plt.plot(VOLTAGES, AREA_4, label="LV2454")
plt.plot(VOLTAGES, AREA_5, label="LV2459")
plt.plot(VOLTAGES, AREA_6, label="LV2455")
plt.plot(VOLTAGES, AREA_7, label="LV2461")
plt.plot(VOLTAGES, AREA_8, label="LV2456")
plt.plot(VOLTAGES, AREA_9, label="LV2460")
plt.plot(VOLTAGES, AREA_10, label="LV2462")
plt.plot(VOLTAGES, AREA_11, label="LV2457")
plt.plot(VOLTAGES, AREA_12, label="LV2464")

plt.legend()
plt.xscale("log")
plt.yscale("log")

plt.title("Log-Log plot of Area vs Bias for 100 photon")
plt.xlabel("Bias Voltage (V)")
plt.ylabel("Mean Pulse Area (mVns)")
plt.savefig(f"{PREFIX}/AreasCompL")
plt.show()

plt.plot(HEIGHTS_1, AREA_1, label="LV2475")
plt.plot(HEIGHTS_2, AREA_2, label="LV2476")
plt.plot(HEIGHTS_3, AREA_3, label="LV2477")
plt.plot(HEIGHTS_4, AREA_4, label="LV2454")
plt.plot(HEIGHTS_5, AREA_5, label="LV2459")
plt.plot(HEIGHTS_6, AREA_6, label="LV2455")
plt.plot(HEIGHTS_7, AREA_7, label="LV2461")
plt.plot(HEIGHTS_8, AREA_8, label="LV2456")
plt.plot(HEIGHTS_9, AREA_9, label="LV2460")
plt.plot(HEIGHTS_10, AREA_10, label="LV2462")
plt.plot(HEIGHTS_11, AREA_11, label="LV2457")
plt.plot(HEIGHTS_12, AREA_12, label="LV2464")

plt.legend()

plt.title("Area vs Height scaling for 100 photon")
plt.xlabel("Mean Pulse Height (mV)")
plt.ylabel("Mean Pulse Area (mVns)")
plt.savefig(f"{PREFIX}/HeightAreaL")
plt.show()

plt.figure(figsize=(10,8))
plt.plot(VOLTAGES, Gain1, label="LV2475")
plt.plot(VOLTAGES, Gain2, label="LV2476")
plt.plot(VOLTAGES2, Gain3, label="LV2477")
plt.plot(VOLTAGES, Gain4, label="LV2454")
plt.plot(VOLTAGES, Gain5, label="LV2459")
plt.plot(VOLTAGES, Gain6, label="LV2455")
plt.plot(VOLTAGES, Gain7, label="LV2461")
plt.plot(VOLTAGES, Gain8, label="LV2456")
plt.plot(VOLTAGES, Gain9, label="LV2460")
plt.plot(VOLTAGES, Gain10, label="LV2462")
#plt.plot(VOLTAGES, Gain11, label="LV2457")
plt.plot(VOLTAGES, Gain12, label="LV2464")

plt.legend()
plt.xscale("log")
plt.yscale("log")

plt.title("Log-Log plot of Gain vs Bias")
plt.xlabel("Bias Voltage (V)")
plt.ylabel("Gain")
plt.savefig(f"{PREFIX}/GainCompL")
plt.show()