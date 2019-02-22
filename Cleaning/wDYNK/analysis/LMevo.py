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
import pytimber
import time

rc('text', usetex=True)
rc('xtick', labelsize=22) 
rc('ytick', labelsize=22)

db=pytimber.LoggingDB()

def convertTime(t0):
    pattern = '%d.%m.%Y %H:%M:%S'
    t = int(time.mktime(time.strptime(t0, pattern)))
    return t

def getTimberData(t01,t02,BLM):
    t1 = convertTime(t01)
    t2 = convertTime(t02)
    data=db.get([BLM],t1,t2)
    tt_BLM,vv_BLM = data[BLM]
    return tt_BLM, vv_BLM

def plotBLMtime(t01,t02,BLM,label):
     tt_BLM, vv_BLM = getTimberData(t01,t02,BLM)
     plotBLMtime = plt.plot_date(epoch2num(tt_BLM+2*3600), vv_BLM,'o', label=label)
     return plotBLMtime

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
nIP3,binsIP3,_ = ax1.hist(ir3,bins=50,range=(1,300),alpha=0.5,label='Losses TCP(IR3)')
nIP7,binsIP7,_ = ax1.hist(ir7,bins=50,range=(1,300),alpha=0.5,label='Losses TCP(IR7)')
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
ax1.legend(loc=2,fontsize=24)
#plt.show()
print "Max in TCP(IR3) =", max(nIP3)
print "Max in TCP(IR7) =", max(nIP7)
print "Hits in TCP(IR3) =", sum(nIP3)
print "Hits in TCP(IR7) =", sum(nIP7)
print "Ratio: log(IR3/IR7) =", np.log10(sum(nIP3)/sum(nIP7))

plt.savefig('LMevo.png',bbox_inches='tight')

fig = plt.figure(2)
ax1 = fig.add_subplot(111)
ax2 = ax1.twiny()

ax1.plot(binsIP3[1:],nIP3/max(nIP3),label='Simulated TCP(IR3)')
ax1.plot(binsIP7[1:],nIP7/max(nIP3),label='Simulated TCP(IR7)')

ax1.set_yscale("log")
ax1.set_ylim(5e-6,2)
ax1.set_xlabel('$f_{RF}$ [Hz]',fontsize=20)
ax1.set_ylabel('Counts/max(IR3)',fontsize=20)
ax1.set_xlim(0, 300)
ax2.set_xlim(0, 300)
ax2.set_xlabel('Turns',fontsize=20)
ax2.set_xticks([0, 100, 200, 300])
ax2.set_xticklabels(['0','2000','4000', '6000'])
#ax1.legend(loc=2,fontsize=20)

# plot data on top
maxFreq = 300.0
minFreq = 0.0
df = 5.
dt = maxFreq/df

#t01 = '13.04.2018 00:56:46'
#t02 = '13.04.2018 00:57:02'
t01 = '23.09.2018 01:22:10'
t02 = '23.09.2018 01:22:40'
BLM1 = "BLMTI.06L7.B1E10_TCP.C6L7.B1:LOSS_RS09"
BLM2 = 'BLMTI.06L3.B1I10_TCP.6L3.B1:LOSS_RS09'
BLM1tt, BLM1data = getTimberData(t01,t02,BLM1)
BLM2tt, BLM2data = getTimberData(t01,t02,BLM2)
t1 = BLM1tt - BLM1tt[0]
t2 = BLM2tt - BLM2tt[0]
f1 = maxFreq*t1/max(t1)
f2 = maxFreq*t2/max(t2)

ax1.plot(f2,BLM2data/max(BLM2data),'o',label='Measured TCP(IR3)')
ax1.plot(f1,BLM1data/max(BLM2data),'o',label='Measured TCP(IR7)')
ax1.legend(loc=2,fontsize=20)

plt.savefig('LMevoCompNorm.png',bbox_inches='tight')
plt.show()


