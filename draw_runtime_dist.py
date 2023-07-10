import pandas as pd
import numpy as np
from scipy.stats import gmean
cvc5_data = pd.read_csv("cvc5.csv")
eusolver_data = pd.read_csv("eusolver.csv")
#dc_data = pd.read_csv("DC.csv")
import matplotlib.pyplot as plt
#plt.rcParams["figure.figsize"] = [15.00, 10.00]
#plt.rcParams['font.size'] = '29'
plt.rc('xtick', labelsize=15)    # fontsize of the tick labels
plt.rc('ytick', labelsize=15)    # fontsize of the tick labels
plt.rc('legend', fontsize=15)
fig, ax = plt.subplots(figsize=(9,6))
x_axis = np.array(list(range(1, len(cvc5_data.final_size)+1)))
x_axis1 = np.array(list(range(1, len(eusolver_data.final_size)+1)))
y_axis = np.array(np.sort(cvc5_data.final_time))
y_axis1 = np.array(np.sort(eusolver_data.final_time))

l1, =ax.plot(x_axis, y_axis, label = "CVC5",linewidth=3)
l2, =ax.plot(x_axis1, y_axis1, label = "EUSolver",linestyle="dashed", linewidth=3)
ax.set_xlabel("# of holes in SyGuS (cumulative)",fontsize=22)
ax.set_ylabel("Runtime of $S^3$ (seconds)",fontsize=22)
plt.legend([l1,l2],["CVC5", "EUSolver"],loc = "upper left")
plt.tight_layout()

plt.savefig("runtime-dist.pdf")
