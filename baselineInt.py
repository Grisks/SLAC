import matplotlib.pyplot as plt
import numpy as np
from integration import get_values_mv_ns
from averaging import NUM_CSVS
from scipy.integrate import simpson
from noise import fitNoise

if __name__ == "__main__":
    values = get_values_mv_ns(1000)
    mean, stddev, __ = fitNoise(values)
    for i in range(NUM_CSVS):
        for i in range(640):
            