import numpy as np
import matplotlib.pyplot as plt

VOLTAGES = [700, 730, 760, 800, 850]

MEANS = [0.24117, 0.1194, 0.19009, 0.13161, -0.1951]

MEANE = [0.0214, 0.0118, 0.0133, 0.0041, 0.0978]

STDDEVS = [0.3188, 0.3496, 0.3365, 0.3546, 0.19654]

STDDEVE = [0.0206, 0.0120, 0.0132, 0.0044, 0.0682]

#plt.plot(VOLTAGES, MEANS, linestyle=':')
plt.errorbar(VOLTAGES, MEANS, MEANE)
plt.show()

plt.plot(VOLTAGES, STDDEVS, linestyle=':')
plt.errorbar(VOLTAGES, STDDEVS, STDDEVE)
plt.show()