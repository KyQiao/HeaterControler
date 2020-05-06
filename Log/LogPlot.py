# plot voltage data
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=[14, 7])

filename = "04-30-at-15_42-year2020Cyclelog"

data = np.loadtxt(filename+".txt", skiprows=2)
# print(data)
timestep = 10
Setpoint = data[:, 0]
Output = data[:, 1]
Objective = data[:, 2]


plt.plot(Setpoint, '--d', label="Setpoint")
plt.plot(Output, '-*', label="Output")
plt.plot(Objective, '-s', label="Objective")
rows = len(Setpoint)
mins = range(0, rows, int(60/timestep))

ax = plt.gca()
# 10mins as a tick
ax.set_xticks(range(0, len(Setpoint), 60))
ax.set_xticks(range(0, len(Setpoint)), minor=True)
ax.set_xticklabels([10*x for x in range(len(range(0, len(Setpoint), 6)))])

plt.xlabel("Time(Min)", fontsize=18)
plt.ylabel("Temperature", fontsize=18)
# plt.yscale('symlog')
# plt.xscale('log')
plt.legend()
plt.savefig(filename+".png", dpi=200)
plt.show()
