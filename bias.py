import numpy as np
import matplotlib.pyplot as plt

VOLTAGES = [600, 650, 700, 750, 800, 850]

MEANS = [ 0.218, -0.042, 0.04, 0.048, 0.292, -0.089]

MEANE = [ 0.015, 0.006, 0.019, 0.020, 0.103, 0.088]

STDDEVS = [ 0.34, 0.36, 0.32, 0.37, 0.19, 0.25]

STDDEVE = [0.016, 0.006, 0.019, 0.019, 0.068, 0.050]

Areas = [8.54, 32.11, 19.27, 26.2, 54.39, 82.91]

AreaE = [.5, .51, .5, 0.76, 1.73, 3.1]

Pulses = [2.21, 4.01, 7.91, 15.0, 26.3, 15.4]

plt.errorbar(VOLTAGES, MEANS, MEANE, linestyle=':')
plt.xlabel("Bias Voltage (V)")
plt.ylabel("Mean Noise Levels (mv)")
plt.title("Mean Noise for PMT LV2464 vs Bias Voltage")
plt.savefig("./figures/NoiseLV2464")
plt.show()

plt.errorbar(VOLTAGES, STDDEVS, STDDEVE, linestyle=':')
plt.xlabel("Bias Voltage (V)")
plt.ylabel("StdDev of Noise (mv)")
plt.title("Spread of Noise for PMT LV2464 vs Bias Voltage")
plt.savefig("./figures/NoiseStdDevLV2464")
plt.show()

plt.errorbar(VOLTAGES, Areas, AreaE, linestyle=':')
plt.xlabel("Bias Voltage (V)")
plt.ylabel("Mean Noise Reduced Pulse Area (mVns)")
plt.title("Pulse Areas for PMT LV2464 vs Bias Voltage")
plt.savefig("./figures/AreasLV2464")
plt.show()

plt.plot(VOLTAGES, Pulses, linestyle=':')
plt.xlabel("Bias Voltage (V)")
plt.ylabel("Mean Pulse Height (mV)")
plt.title("Pulse Heights for PMT LV2464 vs Bias Voltage")
plt.savefig("./figures/HeightsLV2464")
plt.show()