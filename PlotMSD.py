# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 19:16:56 2023

@author: kenzi
"""

# modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def alpha2(MSD, MQD, d):
    '''
    This function calculates the non gaussian parameter.

    :param MSD: array of Mean square displacement values
    :param MQD: array of Mean quadratic displacement values
    :param d: integer, dimensionality of system
    
    both input arrays must be the same length and order
    
    :returns NGP: array of non gaussian parameters
    '''
    # divison factor
    factor = (d+2)/d
    
    NGP = (MQD/(factor*MSD**2)) - 1
    
    return NGP


MSDdata = pd.read_csv("MSD-1000s-9.8ms-2.csv", sep = ';')
#MSDdata = pd.read_csv("MSD.csv", sep = ';')
MSDs = np.array(MSDdata)

# separating MSD, MQD and lagtimes from datafile
MSD = MSDs[:,0]
MQD = MSDs[:,1]
lagtimes = MSDs[:,2]

# finding portion of data with good statistics
N = len(lagtimes) # number of data points
d = 3 # number of dimensions in positional data

# number of points with good statistics
Ng = int((N/100)*90)

# calculate non gaussian parameter
NGP = alpha2(MSD, MQD, d)

# plotting
fig = plt.figure()
gs = fig.add_gridspec(2, hspace=0)
axs = gs.subplots(sharex=True)
axs[0].scatter(lagtimes[0:Ng], MSD[0:Ng], s = 20)
axs[0].set_ylabel(r'$\langle \Delta r^2 (\delta t) \rangle \: (m^2)$')
axs[0].set_yscale('log')
axs[0].set_xscale('log')
fig.text(0.14, 0.82, '(a)', fontsize = 30, color ="black")
fig.text(0.14, 0.15, '(b)', fontsize = 30, color ="black")
axs[1].axhline(y=0, color='black', linestyle='dotted', alpha = 0.2, zorder = 0)
axs[1].scatter(lagtimes[0:Ng], NGP[0:Ng], s = 20, c = 'darkorange', zorder = 10)
axs[1].set_ylabel(r'$\alpha_2 (\delta t)$')
axs[1].set_xlabel('$\delta t \: (s)$')


# Hide x labels and tick labels for all but bottom plot.
for ax in axs:
    ax.label_outer()

