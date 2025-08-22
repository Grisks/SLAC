from integration import save_integration
from averaging import NUM_CSVS, get_pulses, SELF_TRIG, PMT_NAME, VOLTAGE, FILE_PATH
from baselineInt import save_baseline
from noise import save_noise
from pulseHeight import save_pulse_heights
import numpy as np
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    Voltages = [400, 500, 600, 700, 800, 850]
    #Voltages = [700, 800, 850]
    #Voltages = ["8_1_50", "8_1_75", "8_2_00", "8_2_25", "8_2_50"]

    Files =  ["./OscopeOut/PMT_18_400_L/Test_", "./OscopeOut/PMT_18_500_L/Test_", "./OscopeOut/PMT_18_600_L/Test_", "./OscopeOut/PMT_18_700_L/Test_", "./OscopeOut/PMT_18_800_L/Test_", "./OscopeOut/PMT_18_850_L/Test_"]
    #Files = ["./OscopeOut/PMT_18_700/Test_", "./OscopeOut/PMT_18_800/Test_", "./OscopeOut/PMT_18_850/Test_"]
    #Files = ["./OscopeOut/PMT_12_800/Test_", "./OscopeOut/PMT_12_800_1_75V/Test_", "./OscopeOut/PMT_12_800_2V/Test_", "./OscopeOut/PMT_12_800_2_25V/Test_", "./OscopeOut/PMT_12_800_L/Test_",]

    for i in range(len(Voltages)):
        prefix = f"./figures/{PMT_NAME}_{"Self" if SELF_TRIG else "OnLED"}_{Voltages[i]}"
        try:
            os.makedirs(prefix)
        except FileExistsError:
            print("Directory already exists")
        suffix = f"{PMT_NAME}_{"Self" if SELF_TRIG else "OnLED"}_{Voltages[i]}"
        save_noise(prefix, suffix, FileName=Files[i])
        plt.close()
        #save_pulse_heights(prefix, suffix, FileName=Files[i])
        #plt.close()
        #save_integration(prefix, suffix, FileName=Files[i])
        #plt.close()
        #save_baseline(prefix, suffix,FileName=Files[i])
        #plt.close()