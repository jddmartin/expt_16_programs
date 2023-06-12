"""Expt. 16 data collection program. jddmartin@uwaterloo.ca"""

import nidaqmx
from nidaqmx.constants import TerminalConfiguration 
import datetime
import numpy as np

num_samples = 1000
sample_rate = 5e3

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0",max_val=10, min_val=-10,
                                         terminal_config = TerminalConfiguration.DIFF)
    task.ai_channels.add_ai_voltage_chan("Dev1/ai3",max_val=10, min_val=-10,
                                         terminal_config = TerminalConfiguration.DIFF)
    task.triggers.start_trigger.cfg_dig_edge_start_trig("/Dev1/PFI0")
    task.timing.cfg_samp_clk_timing(sample_rate, sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=num_samples)
    task.start()
    value = task.read(number_of_samples_per_channel=num_samples)

import matplotlib

matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
plt.ion()

fig,axs = plt.subplots(2)

axs[0].plot(value[1])

data = value[1]

s = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

times = np.linspace(0, num_samples/sample_rate, num_samples)

np.savetxt(s+"_time_domain.txt", np.c_[times,data])

amps = np.sqrt(np.abs(np.fft.fft(data))**2)

time_step = 1.0 / sample_rate
freqs = np.fft.fftfreq(len(data), time_step)
idx = np.argsort(freqs)

axs[1].plot(freqs[idx], amps[idx])
np.savetxt(s+"_freq_domain.txt", np.c_[freqs[idx], amps[idx]])


print("data saved with precursor filename: ", s)
input("press any key to finish")
