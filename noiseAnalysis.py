from integration import get_values_mv_ns, save_integration
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

values = get_values_mv_ns(2500)

#save_integration("","")

sums = [np.sum(values[i][1])*.2 for i in range(2500)]
sums1 = [np.sum(values[i][1][:333])*.2 for i in range(2500)]
sums2 = [np.sum(values[i][1][333:667])*.2 for i in range(2500)]
sums3 = [np.sum(values[i][1][667:1000])*.2 for i in range(2500)]

total = 0
for i in range(2500):
    for j in range(1000):
        total += values[i][1][j]



print(total/(2500*1000))

mean, stddev = norm.fit(sums)

plt.hist(sums, 40, histtype="step", label="Total")

plt.text(mean+10, 100, f"Mean Area: {np.round(mean, 2)}")
plt.text(mean+10, 90, f"StdDev: {np.round(stddev, 2)}")
plt.show()

plt.hist(sums1, 40, histtype="step", label="First Third")
plt.hist(sums2, 40, histtype="step", label="Middle Third")
plt.hist(sums3, 40, histtype="step", label="Last Thrid")

plt.legend()
plt.show()
