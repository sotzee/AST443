import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def func(x,a):
    xmax = np.sin(np.pi*1.e-10*a)/(np.pi*1.e-10)
    x = np.sin(np.pi*x*a)/(np.pi*x)
    return abs(x)/xmax

data = np.loadtxt('vis.csv',delimiter=',')
xdata = data[:,0]
ydata = data[:,1]
popt, pcov = curve_fit(func,xdata,ydata,0.0087)
print xdata,ydata
print popt,pcov

plt.plot(xdata,ydata,'*',label='Data')
x = np.arange(0,200,1)
y = func(x,popt)
#y = func(x,0.0087)
plt.plot(x,y,label='Best fit')
plt.plot(x,func(x,0.5/180.*np.pi),label='Literature')
plt.xlabel('Baseline (in)')
plt.ylabel('Normalized Visibility')
plt.legend()
plt.show()
