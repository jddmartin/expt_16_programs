import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
plt.ion()

fig,axs = plt.subplots(2)

raw_data = np.loadtxt("./triangle.txt")
axs[0].plot(raw_data[:,0], raw_data[:,1])
data = raw_data[:,1]


ps = np.abs(np.fft.fft(data))**2

time_step = raw_data[1][0] - raw_data[0][0]
freqs = np.fft.fftfreq(1000, time_step)
idx = np.argsort(freqs)

axs[1].plot(freqs[idx], ps[idx])
input()