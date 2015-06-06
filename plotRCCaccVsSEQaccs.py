import sys
import matplotlib.pyplot as plt
import numpy as np
import math

from numpy import arange,array,ones,linalg
from scipy import stats


fn = sys.argv[1]
fin = open(fn)

fin.readline()

famnames = []
difficulties = []
RCCaccs = []
SEQaccs = []

for l in fin:
    l = l.strip().split()
    famnames.append(l[0])
    difficulties.append(float(l[1]))
    RCCaccs.append(float(l[2]))
    SEQaccs.append(float(l[3]))

#difficulties = np.asarray(difficulties)
#difficulties = 1- difficulties

plt.xlim(0,1.2)
plt.ylim(0,1.2)
plt.grid()
plt.scatter(difficulties,RCCaccs,color='#2E9AFE',label='RCC',s=100,edgecolor='#084B8A')
#plt.scatter(difficulties,SEQaccs,color='#FE642E',label='SEQ',s=100,edgecolor='#B40404')
plt.xlabel('difficulty')
plt.ylabel('accuracy')
plt.legend()

#Linear regression

xi = np.asarray(difficulties) #range(0,1.0)
A = array([ xi, ones(len(xi))])
y = np.asarray(RCCaccs)
slope, intercept, r_value, p_value, std_err = stats.linregress(xi,y)
_range = np.arange(0,1.5,0.01)
line = slope*_range+intercept
plt.plot(_range,line,c='#084B8A',linestyle='--')

z = difficulties
y = RCCaccs

#for i, txt in enumerate([a.replace('_','.') for a in famnames]):
#    plt.annotate(txt, (z[i]+0.005,y[i]+0.005),size=9,
#                        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.3))

#fit = np.polyfit(difficulties,RCCaccs,1)
#fit_fn = np.poly1d(fit) # fit_fn is now a function which takes in x and returns an estimate for y
#plt.plot(difficulties,fit_fn(difficulties),color='blue')

#fit = np.polyfit(difficulties,SEQaccs,1)
#fit_fn = np.poly1d(fit) # fit_fn is now a function which takes in x and returns an estimate for y
#plt.plot(difficulties,SEQaccs, 'yo', SEQaccs, fit_fn(SEQaccs), '--k',color='red')


plt.show()


binsRCC = np.linspace(math.ceil(min(RCCaccs)),
                   math.floor(max(RCCaccs)),
                   17)

binsSEQ = np.linspace(math.ceil(min(SEQaccs)),
                   math.floor(max(SEQaccs)),
                   17)
ax = plt.subplot(111)
ax.grid(axis='y')
ax.set_axisbelow(True)
ax.set_zorder(-1)
ax.hist([RCCaccs,SEQaccs],alpha=1,color=['#2E9AFE','#FE642E'],label=['RCC','SEQ'],bins=10,stacked=True)
#plt.hist(SEQaccs,alpha=0.5,label='SEQ',color='#FE642E',bins=10,stacked=True)
ax.legend(loc=2)

print np.median(RCCaccs), np.median(SEQaccs)



plt.show()
