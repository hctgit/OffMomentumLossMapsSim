#!/usr/bin/env python

import numpy as np
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D	
import os.path
from matplotlib.colors import LogNorm
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

# x = np.linspace(0,4.5,100)

# figure(1)
# ##plt.plot(x,intensity(x))
# #plt.plot(x,-derInt(x,0.,1.0,1.0,1660,0))
# #plt.xlabel(r"$x_b$ [mm]",fontsize=18)
# #plt.ylabel(r"Counts",fontsize=18)
# #plt.show()
        
e0 = 6500000.0

sigma = 0.25777
emitn = 3.5e-6

mp = 938.27
gamma = e0/mp
emit = emitn/gamma
dpp0 = 1.129e-4

col_cut_tcp3_sigma = 15.
col_cut_tcp3_mm = col_cut_tcp3_sigma*sigma
col_cut_tcp3_mm = 3.78
#disp_IR3 = 2066.731669
#disp_IR3 = 2100.
disp_IR3 = 1.876058*1e3
deltaCut = 2.06e-3

print "Collimator cut [mm] =", col_cut_tcp3_mm

Npart = 5000
#Npart = 100

xbV = []	
deltaV = []
xV = []
dpp = []
px = []
y = []
py = []
E = []

part = 0

# while (part < Npart):
#         beyondCut = False
#         xb_temp = myPDF()
#         #y.append(myPDF2(1))
#         #py.append(myPDF2(1))
#         #px.append(myPDF2(1))
#         while (beyondCut == False):
#                 delta0 = myPDF()
# 	        delta_temp = (-delta0*dpp0-deltaCut)*disp_IR3
# 	        x = xb_temp*sigma + delta_temp
# 	        if (x <= -col_cut_tcp3_mm):
# 		        xb.append(xb_temp*sigma)
# 		        delta.append((delta_temp))
#                         dpp.append(delta_temp/disp_IR3)
#                         E.append(e0*(1+delta_temp/disp_IR3))
# 		        xV.append(x)
#                         beyondCut = True
# 		        part += 1

#while (part < Npart):
#        xb_temp = myPDFxbeta()
#        delta_temp = myPDFdelta()
#        x, xb, delta = rotateSystem(xb_temp,delta_temp)
#        xbV.append(xb*sigma)
#        deltaV.append(-delta)
#        dpp.append(-delta/disp_IR3)
#        E.append(e0*(1-delta/disp_IR3))
#        #E.append(e0*(1-dpp/disp_IR3))
#        xV.append(x)
#        part += 1

#print "Particles generated =", part
# Regular distribution
#x,px,y,py,zz,ddp,EE,xCut,pxCut,yCut,pyCut,Ecut,zCut,ddpCut = dist_generator(Npart, 6.5e12, 6.486e12,'LHC_coll', 'False', 1, 1, 3.5e-6, 3.5e-6, 1.72435, -2.059930, 131.520626, 144.694088, 0, 0, 0, 0, 2.103, -0.031, 0.221, 0.0042, 42, 1e-4, 0)
# Pencil beam distribution
x,px,y,py,zz,ddp,EE,xCut,pxCut,yCut,pyCut,Ecut,zCut,ddpCut = dist_generator(Npart, 6.5e12, 6.513e12,'LHC_coll', 'False', 1, 1, 3.5e-6, 3.5e-6, 1.72435, -2.059930, 1.520626, 1.694088, 0, 0, 0, 0, 2.103, -0.031, 0.221, 0.0042, 42, 0e-4, 0)

# Plot
##plt.figure(1)
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
##plt.show()

myOutput = open("myDist.dat","w")

for i in range(len(xCut)):
        #print>>myOutput, xV[i]*1e-3, px[i], y[i], py[i], zz[i]*1e3, E[i]
        print>>myOutput, xCut[i], pxCut[i], yCut[i], pyCut[i], zCut[i], Ecut[i]



#figure(2)
##plt.hist2d(delta,xb, bins=300, norm=LogNorm())
##plt.ylabel(r"$x_b/\sigma_\beta$",fontsize=22)
##plt.xlabel(r"\delta [10^{-3}]",fontsize=22)
##plt.ylim(-3,3)
##plt.show()

#figure(1)
#pdf = #plt.hist(xb, bins=50)
##plt.xlabel(r"$x_b/\sigma_\beta$",fontsize=22)
##plt.ylabel(r"Counts",fontsize=22)
##plt.show()


################################################################################################

# Tracking data

#fname_out_pos = "TCP_distribution_pos.dat"
#fname_out_neg = "TCP_distribution_neg.dat"

#fileDType1 = np.dtype([('name', np.int), ('x', np.float), ('y', np.float),
#                       ('xp', np.float), ('yp', np.float),
#                       ('E', np.float), ('s', np.float),
#                       ('turn', np.int), ('halo', np.int),
#                       ('nabs', np.int), ('dpp', np.float), ('xb', np.float)])


#fdata_out_pos = np.loadtxt(fname_out_pos, dtype=fileDType1)
#fdata_out_neg = np.loadtxt(fname_out_neg, dtype=fileDType1)

#print len(-fdata_out_neg[:]["xb"])

#figure(2)
##plt.hist(-fdata_out_neg[:]["xb"]/sigma, bins=50)
##plt.xlim(-2,2)
##plt.ylim(-3,3)
##plt.xlabel(r"Counts",fontsize=22)
##plt.xlabel(r"$x_\beta [\sigma_\beta]$",fontsize=22)
##plt.colorbar()
##plt.show()
