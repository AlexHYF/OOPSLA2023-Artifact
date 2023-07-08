import pandas as pd
import numpy as np
from scipy.stats import gmean
import math
def geo_mean(iterable):
    a = np.array(iterable)
    return a.prod()**(1.0/len(a))
#cvc5:(0.4514149610431553, 0.825158451414961, 0.9647571757296839, 0.03524282427031611)
#eusolver:(0.743756345177665, 0.911756345177665, 0.9842030456852792, 0.015796954314720835)

#(0.8192644624762827, 0.9261636591175164, 0.9865568608453433, 0.01344313915465667)
#(0.8231472081218274, 0.9244263959390863, 0.9842030456852792, 0.015796954314720835)
cvc5_data = pd.read_csv("cvc5.csv")
eusolver_data = pd.read_csv("eusolver.csv")
dc_data = pd.read_csv("DreamCoder/DC.csv")
def cal_size_bucket(data):
    #f1 = np.array([1 if i < 1 else i for i in data.final_time])
   
    f1 = np.array([i for i in data.final_time])
    print(len(f1))
    #s1 = np.array([1 if i < 1 else i for i in data.synthesis_time])
    s1 = np.array([i for i in data.synthesis_time])
    t = f1/s1 
    b1 = [i for i in t if i <= 1]
    b2 = [i for i in t if i <= 10]
    b3 = [i for i in t if i <= 100]
    p1 = len(b1)/len(t)
    p2 = len(b2)/len(t)
    p3 = len(b3)/len(t)
    return p1, p2, p3, 1 -p3

#x = [i for i in cvc5_data.final_time if i <= 1]
#y = [i for i in eusolver_data.final_time if i <= 1] 
#compressed = dc_data.subspec_size/dc_data.triv_size
#z = [i for i in compressed if i < 0.41]
#print(len(z)/len(compressed))
#print(len(x)/len(cvc5_data.final_time))
#print((len(x) + len(y))/(len(cvc5_data.final_time) +len(eusolver_data.final_time)))
#print(cal_size_bucket(cvc5_data))
#print(cal_size_bucket(eusolver_data))
#exit(0) 

print(math.trunc(100*gmean(eusolver_data.preprocessed_size/eusolver_data.triv_size)), math.trunc(100*gmean(eusolver_data.final_size/eusolver_data.preprocessed_size)), math.trunc(100*gmean(eusolver_data.final_size/eusolver_data.triv_size)))
print(math.trunc(100*gmean(cvc5_data.preprocessed_size/cvc5_data.triv_size)), math.trunc(100*gmean(cvc5_data.final_size/cvc5_data.preprocessed_size)), math.trunc(100*gmean(cvc5_data.final_size/cvc5_data.triv_size)))
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
#plt.rcParams["figure.figsize"] = [15.00, 10.00]
#plt.rcParams['font.size'] = '29'
plt.rc('xtick', labelsize=15)    # fontsize of the tick labels
plt.rc('ytick', labelsize=15)    # fontsize of the tick labels
plt.rc('legend', fontsize=15)
fig, ax = plt.subplots(figsize=(9,6))
y_axis = np.array(list(range(1, len(cvc5_data.final_size)+1)))
y_axis1 = np.array(list(range(1, len(eusolver_data.final_size)+1)))
x_axis = np.array(np.sort(cvc5_data.final_size/cvc5_data.triv_size))
x_axis1 = np.array(np.sort(eusolver_data.final_size/eusolver_data.triv_size))

l1, =ax.plot(x_axis, y_axis, label = "CVC5",  linewidth=3)
l2, =ax.plot(x_axis1, y_axis1, label = "EUSolver",linestyle="dashed", linewidth=3)
ax.set_xlabel("$\\frac{|subspec|}{|seed\ subspec|}$",fontsize=21)
ax.set_ylabel("# of holes in SyGuS (cumulative)",fontsize=17)
ax2= ax.twinx()

x_axis = np.sort([i for i in (dc_data.subspec_size/dc_data.triv_size) if i <= 1])
filterout = [i for i in x_axis if i < 0.38]
y_axis = np.array(list(range(1, len(x_axis) + 1)))
ax2.set_ylabel("# of holes in DreamCoder (cumulative)", fontsize=17)
l3, = ax2.plot(x_axis, y_axis ,color = "green", label="DC",linestyle="dotted", linewidth=3)
plt.legend([l1,l2, l3],["CVC5", "EUSolver", "DreamCoder"],loc = "lower right")
plt.tight_layout()

plt.savefig("reduction.pdf")
