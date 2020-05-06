# compare software and hardware difference
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=[10, 10])

data = np.loadtxt("./Software/SoftwareAvgDataF400.txt", skiprows=1)
# print(data)
pwm = data[:, 0]
avg = data[:, 1]
var = data[:, 2]

plt.errorbar(pwm, avg, yerr=var, marker='*',label="Software 400Hz",alpha=0.5)

data = np.loadtxt("./Hardware/HardwareAvgDataF10000.txt", skiprows=1)
# print(data)
pwm = data[:, 0]
avg = data[:, 1]
var = data[:, 2]

plt.errorbar(pwm, avg, yerr=var, marker='*',label="Hardware 10000Hz",alpha=0.5)
plt.plot(np.linspace(0,3.3,100),np.linspace(0,3.3,100),lw=10,alpha=0.5)

plt.xlabel("PWM", fontsize=18)
plt.ylabel("ADC", fontsize=18)
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.savefig("compare.png", dpi=200)
plt.show()
