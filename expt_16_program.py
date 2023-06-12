"""Expt. 16 data collection program. jddmartin@uwaterloo.ca"""

import nidaqmx
from nidaqmx.constants import TerminalConfiguration 
import datetime
import numpy as np
import os.path

##############################################################################
# collect data using the NI USB-6008 DAQ
##############################################################################
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

##############################################################################
# plot and save time-domain waveform
##############################################################################
import matplotlib

matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
plt.ion()

fig,axs = plt.subplots(2)

times = np.linspace(0, (num_samples-1)/sample_rate, num_samples)

axs[0].plot(times, value[1])

data = value[1]

dt = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
s = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
np.savetxt(s+"_time_domain.txt", np.c_[times,data])

##############################################################################
# perform, plot, and save Fourier analysis
##############################################################################
amps = np.sqrt(np.abs(np.fft.fft(data))**2)  # amplitudes

time_step = 1.0 / sample_rate
freqs = np.fft.fftfreq(len(data), time_step)
idx = np.argsort(freqs)

axs[1].plot(freqs[idx], amps[idx])
np.savetxt(s+"_freq_domain.txt", np.c_[freqs[idx], amps[idx]])

print("data saved with precursor filename: ", s)
input("press any key to finish")