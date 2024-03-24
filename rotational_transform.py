# -*- coding: utf-8 -*-
"""
Transform coordinates to rotational frame
"""

### imports as style

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

plt.rcParams.update({
    'text.usetex': False,
    'font.family': 'roman',
})

# #handle graph formatting and style
plt.style.use('shendrukGroupStyle')
#mpl.rcParams['image.cmap'] = 'viridis'
import shendrukGroupFormat as ed
MYLW=1.0 #line width

###

def rotation_matrices(angle_array):
    """
    Generate an array of rotation matrices corresponding to an array of angles.
    """
    cos_theta = np.cos(angle_array)
    sin_theta = np.sin(angle_array)
    rotation_matrix = np.stack((np.stack((cos_theta, -sin_theta), axis=-1),
                                np.stack((sin_theta, cos_theta), axis=-1)), axis=-2)

    return rotation_matrix


def transform_to_rotational_coords(positions, times, omega):
    '''
    positions n x 3 array in xyz format
    
    times n array 
    
    omega, angular speed in radians per second
    '''
    #print(positions)
    
    # angle to transform with
    theta = omega*times # -1 for negative rotation
    #print(theta)
    # calculate sin and cos theta
    costheta = np.cos(theta)
    sintheta = np.sin(theta)
    
    #print(costheta, sintheta)
    
    # isolate axis coords
    x = positions[:, 0]
    y = positions[:, 1]
    z = positions[:, 2]
    
    rotx = (x*costheta[:, 0]) - (y*sintheta[:, 0])
    roty = (x*sintheta[:, 0]) + (y*costheta[:, 0])  
    
    #print(rotx[0], x[0])
    #print(roty[0], y[0])
    
    rotpositions = np.zeros_like(positions)
    
    rotpositions[:, 0] = rotx
    rotpositions[:, 1] = roty
    rotpositions[:, 2] = z
    
    #rotpositions = np.array([rotx, roty, z])
    #print(rotpositions)
    
    return rotpositions

#transform_to_rotational_coords(np.array([1, 0, 0]), times, omega)
       
        
# path = '../../bacpos.csv'    
# timepath = '../../time.csv' 

# #xyz = pd.read_csv('D:\MPhys\ExpData/Exp2/omega=1.407052941362897,vs=7.5e-06/run_1/positions.csv')
# xyz = pd.read_csv('D:\MPhys\ExpData/Exp3/omega=1.407,g=29.4,vs=2.5e-05/run_1/positions.csv')
# xyz = pd.read_csv(path)
# positions = np.array(xyz) # in xyz format

# x = positions[:, 0]
# y = positions[:, 1]
# r = np.sqrt((x**2) + (y**2))

# #time = pd.read_csv('time.csv')
# time = pd.read_csv(timepath)
# t = np.array(time)
    
# rotcoords = transform_to_rotational_coords(positions, t, 1.407052941362897)

# fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (15, 8))

# ax[0].scatter(x[::50], y[::50], s = 1)
# ax[1].scatter(rotcoords[:, 0][::50], rotcoords[:, 1][::50], s = 1)


# get all folder names in Data directory
config_path = 'D:/Kenzie_Mphys/Data/Exp2/Raw2/'
config_list = os.listdir(config_path)
config_list = config_list
#print(config_list)

time = pd.read_csv('C:/Users/kenzi/Documents/Masters/BacStroke2.0/BacStroke2.0/Studies/Exp2/timenew230324.csv')
times = np.array(time)
#print(times)

# for each folder
for i in range(len(config_list)): #len(config_list)
    print(i)
    
    # path to save output plot too 
    plot_path = 'D:/Kenzie_Mphys/Data/Exp2/Rotated_coordinates/' + config_list[i] + '.png'
    
    # if png doesnt exist already then generate it
    if not os.path.exists(plot_path):
        
        char1 = '='
        char2 = ','
        
        omega = float(config_list[i][config_list[i].find(char1)+1:config_list[i].find(char2)])
    
        # current folder path
        folder_path = config_path + '/' + config_list[i]
        
        # getting each run folder
        run_paths = os.listdir(folder_path)
        #print(run_paths)
        
        # # create figure to plot too for each iteration
        
        # fig = plt.figure(constrained_layout = True, figsize = (15,8))
        # gs = fig.add_gridspec(nrows = 1, ncols = 2, wspace = 0, figure = fig)
        # ax = gs.subplots()#sharey = True)

        # # fig, ax = plt.subplots(ncols = 2, nrows = 1, figsize = (25, 12))
        # # fontsize = 27
        # ax[0].set_xlabel(r'$x (m)$')#,fontsize = fontsize)
        # ax[0].set_ylabel(r'$y (m)$')#,fontsize = fontsize)
        # ax[0].set_title('Lab frame')
        # ax[1].set_xlabel(r'$x (m)$')#,fontsize = fontsize)
        # ax[1].set_ylabel(r'$y (m)$')#,fontsize = fontsize)
        # ax[1].set_title('Rotated frame')
        # # ax[2].set_xlabel(r'$z/m$')#,fontsize = fontsize)
        # # ax[2].set_ylabel(r'$y/m$')#,fontsize = fontsize)
       

        # ticklabelsize = 23
        # ax[0].tick_params(axis='x')#, labelsize=ticklabelsize)
        # ax[0].tick_params(axis='y')#, labelsize=ticklabelsize)
        
        # ax[1].tick_params(axis='x')#, labelsize=ticklabelsize)
        # ax[1].tick_params(axis='y')#, labelsize=ticklabelsize)
        
        # # ax[2].tick_params(axis='x')#, labelsize=ticklabelsize)
        # # ax[2].tick_params(axis='y')#, labelsize=ticklabelsize)
        
        # ax[0].set_ylim(-0.055, 0.055)
        # ax[1].set_ylim(-0.055, 0.055)
        
        # # adding circular patches for scale
        # R = 5E-2
        # r = 0.5E-2
        # cir = plt.Circle((0, 0), R, facecolor='#c7c7c7', alpha=0.5, linewidth=3, linestyle='--', edgecolor='black')#color='darkorange',fill=False)
        # ax[0].add_patch(cir)
        # cir2 = plt.Circle((0, 0), r, facecolor='white', alpha=0.5, linewidth=3, linestyle='--', edgecolor='black')#color='darkorange',fill=False)
        # ax[0].add_patch(cir2)
        
        # cir = plt.Circle((0, 0), R, facecolor='#c7c7c7', alpha=0.5, linewidth=3, linestyle='--', edgecolor='black')#color='darkorange',fill=False)
        # ax[1].add_patch(cir)
        # cir2 = plt.Circle((0, 0), r, facecolor='white', alpha=0.5, linewidth=3, linestyle='--', edgecolor='black')#color='darkorange',fill=False)
        # ax[1].add_patch(cir2)
        
        # fig.suptitle(config_list[i], fontsize = 30)
        
        # # for axs in ax:
        # #     axs.label_outer()
        
        
        # for each iteration of a config
        for j in range(len(run_paths)):
            
            # check if folder exists
            
            # grab the sub folders containing the data and find the positions.csv file
            pos_path = folder_path + '/' + run_paths[j] + '/positions.csv'
            
            # fetch positions and convert to numpy array
            xyz = pd.read_csv(pos_path)
            positions = np.array(xyz) # in xyz format
            
            npoints = 50
            #ax[0].scatter(positions[:, 0][::npoints], positions[:, 1][::npoints], s = 3, alpha = 0.3)
            
            # transformed coordinates
            rotcoords = transform_to_rotational_coords(positions, times, omega)
            
            # write to file
            output_path = 'D:/Kenzie_Mphys/Data/Exp2/Rotated_coordinates/' + config_list[i] + '/' + run_paths[j]
            if not os.path.exists(output_path):
                os.makedirs(output_path)
                print(output_path)
                
                np.savetxt(output_path + '/rotated_positions.csv', rotcoords, delimiter=",")
                
            #ax[1].scatter(rotcoords[:, 0][::npoints], rotcoords[:, 1][::npoints], s = 3, alpha = 0.3)
            
            
        #plt.show()
        #fig.savefig(plot_path, dpi = 500)
        
        
        
        
        
        
    

    
    
    



    
    
    





