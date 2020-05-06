# plot voltage data
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=[10, 10])
for i in range(1, 11):
    data = np.loadtxt("SoftwareAvgDataF"+str(i)+"00.txt", skiprows=1)
    # print(data)
    pwm = data[:, 0]
    avg = data[:, 1]
    var = data[:, 2]

    # plt.errorbar(pwm[90:], avg[90:], yerr=var[90:], marker='*',label=str(i)+"00Hz")
    plt.errorbar(pwm, avg, yerr=var, marker='*',label=str(i)+"00Hz",alpha=0.5)


plt.plot(np.linspace(0,3.3,100),np.linspace(0,3.3,100),lw=10,alpha=0.5)
plt.xlabel("PWM", fontsize=18)
plt.ylabel("ADC", fontsize=18)
plt.yscale('log')
plt.xscale('log')
plt.legend()
plt.savefig("overallPerformance.png", dpi=200)
plt.show()
