import numpy as np
import matplotlib.pyplot as plt
import keyoscacquire as koa
import time

scope = koa.oscilloscope.Oscilloscope(address='USB0::10893::6006::MY58262555::INSTR', )
scope.savepng = False
for i in range(10):
    scope.set_options_get_trace(num_points=1000)
    scope.save_trace(f"./OscopeOut/TestTrace3_{i}", ext=".csv")
    time.sleep(0.0001)