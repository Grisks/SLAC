from integration import save_integration
from averaging import NUM_CSVS, get_pulses, SELF_TRIG, PMT_NAME, VOLTAGE
from baselineInt import save_baseline
from noise import save_noise
from pulseHeight import save_pulse_heights
import numpy as np
import matplotlib.pyplot as plt



if __name__ == "__main__":
    suffix = f"{PMT_NAME}_{"Self" if SELF_TRIG else "OnLED"}_{VOLTAGE}"
    save_noise(suffix)
    save_pulse_heights(suffix)
    save_integration(suffix)
    save_baseline(suffix)