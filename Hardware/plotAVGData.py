# plot voltage data
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=[10, 10])
for i in range(1, 2):
    data = np.loadtxt("HardwareAvgDataF"+str(i)+"0000.txt", skiprows=1)
    # print(data)
    pwm = data[:, 0]
    avg = data[:, 1]
    var = data[:, 2]

    # plt.errorbar(pwm[90:], avg[90:], yerr=var[90:], marker='*',label=str(i)+"00Hz")
    plt.errorbar(pwm, np.abs(avg-pwm), yerr=var, marker='*',label=str(i)+"0000Hz",alpha=0.5)
    print(str(i)+"0000Hz: "+str(np.sum(np.abs(avg-pwm))))

for i in range(9, 10):
    data = np.loadtxt("HardwareAvgDataF"+str(i)+"000.txt", skiprows=1)
    # print(data)
    pwm = data[:, 0]
    avg = data[:, 1]
    var = data[:, 2]

    # plt.errorbar(pwm[90:], avg[90:], yerr=var[90:], marker='*',label=str(i)+"00Hz")
    plt.errorbar(pwm, np.abs(avg-pwm), yerr=var, marker='*',label=str(i)+"000Hz",alpha=0.5)
    print(str(i)+"000Hz: "+str(np.sum(np.abs(avg-pwm))))

plt.plot(np.linspace(0,3.3,100),np.linspace(0,0,100),lw=10,alpha=0.5)
plt.xlabel("PWM", fontsize=18)
plt.ylabel("ADC", fontsize=18)
# plt.yscale('symlog')
# plt.xscale('log')
plt.legend()
# plt.savefig("HardwarePWMOverall.png", dpi=200)
plt.show()