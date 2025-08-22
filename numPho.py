import numpy as np
import matplotlib.pyplot as plt

LED_VOLT = [1.5, 1.75, 2.0, 2.25, 2.5]

Heights_7 = [4.1, 9.06, 37.5, 129.3, 333]

Area_7 = [3, 39.6, 297.3, 1433, 3653]

AreaE_7 = [.25, .77, 1.5, 3, 5.5]

Heights_8 = [13.2, 27.85, 115, 395, 1057.9]

Area_8 = [25, 131.5, 1230, 4207.2, 9631]

AreaE_8 = [.33, 2.6, 4.8, 9, 13.7]

plt.plot(LED_VOLT, Heights_7, label="700V")
plt.plot(LED_VOLT, Heights_8, label="800V")

plt.xscale('log')
plt.yscale("log")

plt.legend()

plt.xlabel("LED Voltage (V)")
plt.ylabel("Mean Pulse Height (mV)")
plt.title("Pulse Height scaling with LED voltage for PMT LV2455")
plt.savefig("./figures/LV2455/LV2455_LED/HeightLED")

plt.show()

plt.errorbar(LED_VOLT, Area_7, AreaE_7, [0.02,0.02,0.02,0.02,0.02], label="700V")
plt.errorbar(LED_VOLT, Area_8, AreaE_8, [0.02,0.02,0.02,0.02,0.02], label="800V")

plt.legend()

plt.xlabel("LED Voltage (V)")
plt.ylabel("Mean Pulse Area (mVns)")
plt.title("Pulse Area scaling with LED voltage for PMT LV2455")

plt.savefig("./figures/LV2455/LV2455_LED/AreaLED")

plt.show()