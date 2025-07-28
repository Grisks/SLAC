import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

VOLTAGES = [400, 500, 600, 700, 800, 850]
VOLTAGES2 = [400,500,600,800,850]

HEIGHTS_1 = [3.52, 22.06, 111.97, 425.62, 1267.1, 2054.2]
HEIGHTS_E_1 = [0.03, 0.19, 0.74, 3.08, 11.5, 3.21]

AREA_1 = [20.69, 227.51, 1212.5, 4896.4, 12191, 19660]

HEIGHTS_2 = [2.88, 18.84, 95.67, 371, 1186, 1854]
HEIGHTS_E_2 = [.1, .23, 1.1, 0.63, 11.1, 6.86]

AREA_2 = [11.54, 205.82, 1012, 4047, 11498, 17990]
AREA_E_2 = [.17, .28, 1.17, 4.63, 17.31, 21.63]

HEIGHTS_3 = [1.45, 5.77, 28.11, 319.6, 498]

AREA_3 = [5, 39.4, 283.4, 3434, 5671]
AREA_E_3 = [.12, 0.19, .43, 5, 6.6]

NUM_PHO = 86 #Number of photons per pulse
REFF = 50 #Need to calculate more definitively
Q = 1.602 * 10 ** -19 #Charge of Electron
def gain(area):
    return area * (10**-12) / (REFF * Q)

Gain1 = gain(np.array(AREA_1))/(NUM_PHO*2) #set single photon gain by converting area to gain and divide by number of photons making up area
Gain2 = gain(np.array(AREA_2))/(NUM_PHO*2)
Gain3 = gain(np.array(AREA_3))/(NUM_PHO*2)

plt.errorbar(VOLTAGES, HEIGHTS_1, HEIGHTS_E_1, xerr=[2,2,2,2,3,3], label="LV2475")
plt.errorbar(VOLTAGES, HEIGHTS_2, HEIGHTS_E_2, xerr=[2,2,2,2,3,3], label="LV2476")
plt.errorbar(VOLTAGES2, HEIGHTS_3, xerr=[2,2,2,3,3], label="LV2477")

plt.legend()

plt.title("PMT Pulse Heights with 100 photon input on PMT")
plt.xlabel("Bias Voltage (V)")
plt.ylabel("Mean Pulse Height (mV)")
plt.savefig("./Figures/LV2477/LV2477L/HeightsComp")
plt.show()

plt.plot(VOLTAGES, HEIGHTS_1, label="LV2475")
plt.plot(VOLTAGES, HEIGHTS_2, label="LV2476")
plt.plot(VOLTAGES2, HEIGHTS_3, label="LV2477")

plt.legend()
plt.xscale("log")
plt.yscale("log")

plt.title("Log-Log plot of Height vs Bias for 100 photon")
plt.xlabel("Bias Voltage (V)")
plt.ylabel("Mean Pulse Height (mV)")
plt.savefig("./Figures/LV2477/LV2477L/HeightsCompL")
plt.show()

plt.plot(VOLTAGES, AREA_1, label="LV2475")
plt.plot(VOLTAGES, AREA_2, label="LV2476")
plt.plot(VOLTAGES2, AREA_3, label="LV2477")

plt.legend()
plt.xscale("log")
plt.yscale("log")

#res = linregress(np.log10(VOLTAGES),np.log10(AREA))
#x = np.linspace(300,1000,100)
#plt.plot(x, (res.intercept + res.slope*x), 'r', label='fitted line')
#print(f"High Slope: {res.slope}, High Inter: {res.intercept}")
plt.title("Log-Log plot of Area vs Bias for 100 photon")
plt.xlabel("Bias Voltage (V)")
plt.ylabel("Mean Pulse Area (mVns)")
plt.savefig("./Figures/LV2477/LV2477L/AreasCompL")
plt.show()


plt.plot(VOLTAGES, Gain1, label="LV2475")
plt.plot(VOLTAGES, Gain2, label="LV2476")
plt.plot(VOLTAGES2, Gain3, label="LV2477")

plt.legend()
plt.xscale("log")
plt.yscale("log")

plt.title("Log-Log plot of Gain vs Bias")
plt.xlabel("Bias Voltage (V)")
plt.ylabel("Gain")
plt.savefig("./Figures/LV2477/LV2477L/GainCompL")
plt.show()