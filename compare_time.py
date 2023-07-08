import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as mtick
import math
def cal_size_bucket(data):
    #f1 = np.array([1 if i < 1 else i for i in data.final_time])
   
    f1 = np.array([i for i in data.final_time])
    #print(len(f1))
    #s1 = np.array([1 if i < 1 else i for i in data.synthesis_time])
    s1 = np.array([i for i in data.synthesis_time])
    t = f1/s1 
    b1 = [i for i in t if i <= 1]
    b2 = [i for i in t if i <= 10]
    b3 = [i for i in t if i <= 100]
    p1 = len(b1)/len(t)
    p2 = len(b2)/len(t)
    p3 = len(b3)/len(t)
    return [p1, p2, p3, 1 -p3]
barWidth = 0.4
plt.rc('xtick', labelsize=15)    # fontsize of the tick labels
plt.rc('ytick', labelsize=15)    # fontsize of the tick labels
plt.rc('legend', fontsize=15)
fig = plt.subplots(figsize =(9, 6))
cvc5_data = pd.read_csv("cvc5.csv")
eusolver_data = pd.read_csv("eusolver.csv")

eusolver = [math.trunc(i*1000)/1000.0 for i in cal_size_bucket(eusolver_data)]
eusolver_label = ["{:.1f}%".format(i*100) for i in eusolver]
cvc5 = [math.trunc(i*1000)/1000.0 for i in cal_size_bucket(cvc5_data)]
cvc5_label = ["{:.1f}%".format(i*100) for i in cvc5]

br1 = np.arange(len(eusolver))
br2 = [x + barWidth for x in br1]
b1 = plt.bar(br1, eusolver, color='salmon', width= barWidth, edgecolor = 'grey', label = 'EUSolver', hatch = ['..'])
b2 = plt.bar(br2, cvc5, color='lightgreen', width= barWidth, edgecolor = 'grey', label = 'CVC5', hatch = ["//"])
plt.bar_label(b1, eusolver_label, fontsize=13)
plt.bar_label(b2, cvc5_label, fontsize=13)
plt.xlabel("Time needed compare with original synthesis tasks", fontsize=22)
plt.ylabel("Fraction of holes", fontsize=22)
plt.xticks([r + 0.5 * barWidth for r in range(len(eusolver))], ['≤ 1X', '≤ 10X', '≤ 100X', '> 100X'])
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
plt.legend(fontsize="15")
plt.tight_layout()
plt.savefig("compare_time.pdf")
