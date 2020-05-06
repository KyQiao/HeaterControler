import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure(figsize=[20,10])

ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

data = np.loadtxt("increase.txt",skiprows=1)
setpoint1 = data[:,0]
output = data[:,1]
obj = data[:,2]

ax1.plot(output,'--d')
ax1.plot(obj,'-*')
ax1.set_xticks(range(0,len(setpoint1),6))
ax1.set_xticks(range(0,len(setpoint1)),minor=True)
ax1.set_xticklabels(range(len(range(0,len(setpoint1),6))))
ax1.set_xlabel('Min',fontsize=18)
ax1.set_ylabel("temperature",fontsize=18)


data = np.loadtxt("decrease.txt",skiprows=1)
setpoint2 = data[:,0]
output = data[:,1]
obj = data[:,2]

ax2.plot(output,'--d')
ax2.plot(obj,'-*')
ax2.set_xticks(range(0,len(setpoint2),6))
ax2.set_xticks(range(0,len(setpoint2)),minor=True)
ax2.set_xticklabels(range(len(range(0,len(setpoint2),6))))
ax2.set_xlabel('Min',fontsize=18)
ax2.set_ylabel("temperature",fontsize=18)
plt.savefig("cycleBench.png",bbox_inches='tight')
plt.show()