"""Expt. 16 data collection program. jddmartin@uwaterloo.ca"""

import nidaqmx
from nidaqmx.constants import TerminalConfiguration 
import datetime
import numpy as np
import os.path
from pathlib import Path

##############################################################################
# define helper functions
##############################################################################
def data_directory():
    """Creates directory for data if it doesn't exist
    and returns path to this directory"""
    dt = os.path.join(os.environ['USERPROFILE'], 
                      "OneDrive - University of Waterloo",
                      'Desktop')
    date = datetime.datetime.now().strftime("%Y%m%d")

    data_directory = os.path.join(dt, date + "_expt_16_data")
    Path(data_directory).mkdir(exist_ok=True, parents=True)
    return data_directory

##############################################################################
# collect data using the NI USB-6008 DAQ
##############################################################################
num_samples = 10000
sample_rate = 5e3  # (Hz) do not change, maximum available
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

max_to_plot = 250
axs[0].plot(times[:max_to_plot], value[1][:max_to_plot])
axs[0].set_title("First few cycles")
axs[0].set_xlabel("time (s)")

data = value[1]

dt = data_directory()

s = os.path.join(dt, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
np.savetxt(s+"_time_domain.txt", np.c_[times,data])

##############################################################################
# perform, plot, and save Fourier analysis
##############################################################################
amps = np.sqrt(np.abs(np.fft.fft(data))**2)  # amplitudes

time_step = 1.0 / sample_rate
freqs = np.fft.fftfreq(len(data), time_step)
idx = np.argsort(freqs)

axs[1].plot(freqs[idx], amps[idx])
axs[1].set_title("Power spectrum")
axs[1].set_xlabel("frequency (Hz)")
plt.tight_layout()
np.savetxt(s+"_freq_domain.txt", np.c_[freqs[idx], amps[idx]])

print("data saved with precursor filename: ", s)
input("press any key to finish")