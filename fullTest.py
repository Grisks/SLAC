from integration import save_integration
from averaging import NUM_CSVS, get_pulses, SELF_TRIG, PMT_NAME, VOLTAGE, FILE_PATH
from baselineInt import save_baseline
from noise import save_noise
from pulseHeight import save_pulse_heights
import numpy as np
import matplotlib.pyplot as plt
import os



if __name__ == "__main__":
    
    prefix = f"./figures/{PMT_NAME}_{"Self" if SELF_TRIG else "OnLED"}_{VOLTAGE}"
    try:
        os.makedirs(prefix)
    except FileExistsError:
        print("Directory already exists")
    suffix = f"{PMT_NAME}_{"Self" if SELF_TRIG else "OnLED"}_{VOLTAGE}"
    save_noise(prefix, suffix)
    save_pulse_heights(prefix, suffix)
    plt.show()
    save_integration(prefix, suffix)
    save_baseline(prefix, suffix)