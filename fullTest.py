from integration import save_integration
from averaging import NUM_CSVS, get_pulses, SELF_TRIG, PMT_NAME, VOLTAGE, FILE_PATH
from baselineInt import save_baseline
from noise import save_noise
from pulseHeight import save_pulse_heights
import numpy as np
import matplotlib.pyplot as plt
import os



if __name__ == "__main__":
    Voltages = [700,800,850]
    Files = ["./OscopeOut/PMT_9_700/Test_", "./OscopeOut/PMT_9_800/Test_", "./OscopeOut/PMT_9_850/Test_"]
    for i in range(len(Voltages)):
        prefix = f"./figures/{PMT_NAME}_{"Self" if SELF_TRIG else "OnLED"}_{Voltages[i]}"
        try:
            os.makedirs(prefix)
        except FileExistsError:
            print("Directory already exists")
        suffix = f"{PMT_NAME}_{"Self" if SELF_TRIG else "OnLED"}_{Voltages[i]}"
        #save_noise(prefix, suffix, FileName=Files[i])
        #plt.close()
        save_pulse_heights(prefix, suffix, FileName=Files[i])
        plt.close()
        save_integration(prefix, suffix, FileName=Files[i])
        plt.close()
        save_baseline(prefix, suffix,FileName=Files[i])
        plt.close()