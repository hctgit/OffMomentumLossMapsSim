#!/usr/bin/env python

import numpy as np
#import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os.path
#from matplotlib.colors import LogNorm
from math import factorial
from random import gauss
from random import uniform

from generate_distribution import *

import os,sys

#rc('text', usetex=True)
#rc('xtick', labelsize=18) 
#rc('ytick', labelsize=18)

def myPDF():
        rand_num_1 = gauss(0,1)
	rand_num_2 = gauss(0,1)
        pdf = -np.sqrt(rand_num_1**2.0 + rand_num_2**2.0)
        return pdf

def myPDFxbeta():
        beyondCut = False
        xb_prim_0 = -0.77
        sigma_xb_prim = 0.5
        cut = 0.
        while beyondCut == False:
                rand_num = gauss(xb_prim_0, sigma_xb_prim)
                if (rand_num < cut):
                        xb_prim = rand_num
                        beyondCut = True
        return xb_prim

def myPDFdelta():
        delta_lambda = -30.0 # this parameter controls the width of the distribution
        delta_prim_off = -1.82 # this parameter controls the cut of deltaprime with the axis
        rand_num = uniform(0,1)
        exp_num = np.log(1-rand_num**2)/(-delta_lambda)+delta_prim_off
        delta_prim = exp_num
        return delta_prim

def rotateSystem(x,delta):
        sigma = 257.77e-3
        disp_IR3 = -2.066731669
        angle = np.pi/2. - np.arctan(disp_IR3/sigma)
        xb = x*np.cos(-angle)+delta*np.sin(-angle)
        delta = -delta*np.cos(-angle)+x*np.sin(-angle)
        x = xb*sigma+delta*disp_IR3
        return x, xb, delta

def myPDF2(sigma):
        rand_num_1 = gauss(0,sigma)
        pdf = rand_num_1
        return pdf

def intensity(x,x0=0.0,sigma1=1.0,sigma2=1.0,I1=1.0,I2=1.0):
        intensity = I1*np.exp(-(x-x0)**2/(2*sigma1**2)) + I2*np.exp(-(x-x0)**2/(2*sigma2**2))
        return intensity

def derInt(x,x0=0.0,sigma1=1.0,sigma2=1.0,I1=1.0,I2=1.0):
        derInt = -I1*(x-x0)/(sigma1**2)*np.exp(-(x-x0)**2/(2*sigma1**2)) - I2*(x-x0)/(sigma2**2)*np.exp(-(x-x0)**2/(2*sigma2**2))
        return derInt
        
e0 = 450000.0

sigma = 0.98
emitn = 3.5e-6

mp = 938.27
gamma = e0/mp
emit = emitn/gamma
dpp0 = 1.129e-4

col_cut_tcp3_sigma = 8.
col_cut_tcp3_mm = col_cut_tcp3_sigma*sigma

print "Collimator cut [mm] =", col_cut_tcp3_mm
cut = col_cut_tcp3_mm

Npart = 5000

xbV = []	
deltaV = []
xV = []
dpp = []
px = []
y = []
py = []
E = []

x,px,y,py,zz,ddp,EE,xCut,pxCut,yCut,pyCut,Ecut,zCut,ddpCut = dist_generator(Npart, 0.450e12, 0.4518e12,'LHC_coll', 'False', 1, 1, 3.5e-6, 3.5e-6, 1.725949, -2.058981, 131.519214, 144.642962, 0, 0, 0, 0, 2.147613, -0.030521, 0.049058, 0.000231, 42, 0e-4, 0,cut)

print "b =", abs(x[0]*1e3-cut)

# Plot
#plt.figure(1)
#plt.subplot(311)
#plt.hist(xCut, bins=50, alpha=0.5, label='With cut')
#plt.xlabel(r"$x_b$ [mm]",fontsize=18)
#plt.ylabel(r"Counts",fontsize=18)
#plt.legend()
#plt.subplot(312)
#plt.hist(ddpCut, bins=50,alpha=0.5, label='With cut')
#plt.xlabel(r"$\delta D_x$ [mm]",fontsize=18)
#plt.ylabel(r"Counts",fontsize=18)
#plt.legend()
#plt.subplot(313)
#plt.hist(xCut,bins=50, alpha=0.5, label='With cut')
##plt.axvline(col_cut_tcp3_mm, linewidth=3, color='red')
#plt.xlabel(r"$x$ [mm]",fontsize=18)
#plt.ylabel(r"Counts",fontsize=18)
#plt.legend()
##plt.show()

#plt.figure(2)
#plt.subplot(221)
##plt.plot(xV,px*1e3,'.')
#plt.plot(x,px,'.')
#plt.plot(xCut,pxCut,'.')
##plt.hist2d(xV,px*1e3,bins=(100,100),range=((3.78,3.9),(-0.015,0.015)))
#plt.xlabel("$x$ [mm]",fontsize=18)
#plt.ylabel("$p_x$ [mrad]",fontsize=18)
#plt.subplot(222)
#plt.plot(y,py,'.')
#plt.plot(yCut,pyCut,'.')
##plt.hist2d(y,py*1e3,bins=(100,100))
#plt.xlabel("$y$ [mm]",fontsize=18)
#plt.ylabel("$p_y$ [mrad]",fontsize=18)
#plt.subplot(223)
##plt.plot(deltaV,xbV,'.')
#plt.plot(ddp,x,'.')
#plt.plot(ddpCut,xCut,'.')
##plt.hist2d(deltaV,xbV,bins=(100,100))
#plt.xlabel("$\delta [10^{-3}]$",fontsize=18)
#plt.ylabel(r"$x$ [mm]",fontsize=18)
##plt.ylabel(r"$x_\beta$ [mm]",fontsize=18)
#plt.subplot(224)
#plt.plot(zz*1e3,EE*1e-6,'.')
#plt.plot(zCut,Ecut,'.')
##plt.hist2d(z,E,bins=(100,100))
#plt.xlabel("$z$ [mm]",fontsize=18)
#plt.ylabel("$E$ [GeV]",fontsize=18)
#plt.show()

myOutput = open("myDist.dat","w")

for i in range(len(xCut)):
        #print>>myOutput, xV[i]*1e-3, px[i], y[i], py[i], zz[i]*1e3, E[i]
        print>>myOutput, xCut[i], pxCut[i], yCut[i], pyCut[i], zCut[i], Ecut[i]

