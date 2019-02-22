import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import linecache
import scipy.io
import glob
import operator
import sys
import os.path
from matplotlib import rc

rc('text', usetex=True)
rc('xtick', labelsize=22) 
rc('ytick', labelsize=22)

def readImpactsReal(fileData):
    fileDType = np.dtype([('icoll', np.int), ('rotation', np.float),
                          ('s', np.float), ('x', np.float), ('xp', np.float),
                          ('y', np.float), ('yp', np.float), ('nabs', np.int),
                          ('np', np.int), ('ntu', np.int)])
    data = np.loadtxt(fileData,fileDType)
    return data

ir3 = []
ir7 = []

freqTrim = 500.
turns = 1e4
deltap = 3.87e-3
tlapse = 15.
frev = 11.e3

for j in range(1000):
    m = j + 1
    file = '../run%04d/impacts_real.dat' % m
    if os.path.isfile(file):
        turn = readImpactsReal(file)['ntu']*freqTrim/turns
        #turn = readImpactsReal(file)['ntu']*deltap/turns*1e3
        icoll = readImpactsReal(file)['icoll']

        for i in range(len(turn)):
            if (icoll[i] == 1):
                ir3.append(turn[i])
            if (icoll[i] == 11):
                ir7.append(turn[i])

fig = plt.figure(1)
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()
nIP3,binsIP3,_ = ax1.hist(ir3,bins=50,range=(1,300),alpha=0.5,label='IR3')
nIP7,binsIP7,_ = ax1.hist(ir7,bins=50,range=(1,300),alpha=0.5,label='IR7')
#plt.hist(ir3,bins=50,range=(0,2.5),alpha=0.5,label='IR3')
#plt.hist(ir7,bins=50,range=(0,2.5),alpha=0.5,label='IR7')
#plt.yscale('log',fontsize=22)
ax1.set_yscale("log")
ax1.set_xlabel('$f_{RF}$ [Hz]',fontsize=20)
#ax1.yscale('log',fontsize=22)
#ax1.set_xlabel('$f_{RF}$ [Hz]',fontsize=22)
#ax2.set_xlabel('Turns',fontsize=22)
#plt.xlabel('Turn',fontsize=18)
#plt.xlabel('deltap',fontsize=18)
ax1.set_ylabel('Counts',fontsize=20)
ax1.set_xlim(0, 300)
ax2.set_xlim(0, 300)
ax2.set_xlabel('Turns',fontsize=20)
ax2.set_xticks([0, 100, 200, 300])
ax2.set_xticklabels(['0','2000','4000', '6000'])
#ax1.legend(loc=2,fontsize=22)
plt.show()
print "Hits in TCP(IR3) =", sum(nIP3)
print "Hits in TCP(IR7) =", sum(nIP7)
print "Ratio: log(IR3/IR7) =", np.log10(sum(nIP3)/sum(nIP7))

