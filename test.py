import numpy as np
import matplotlib.pyplot as plt
import keyoscacquire as koa

scope = koa.oscilloscope.Oscilloscope(address="")

scope.set_options_get_trace_save("TestTrace.png", num_points=1000)
scope.plot_trace()