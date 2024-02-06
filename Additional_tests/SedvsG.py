'''
This script plots sedimentation speed against gravitational strength
for each of the objects in the Objects_initial_conditions folder.

The Object_initial_conditions folder contains inital conditions file for numerous
objects. Naming on the plot is based off of the file name minus the .txt.

This script turns off the following components of velocity:
    
    Diffusion: by setting diffusion coefficient to 0 in config file
    Swimming: by setting swimming velocity in each initial conditions file to 0
    Rotation: by setting the clinostat rotation rate to 0 in the configuration file

Check the configuration text file to ensure all other parameters are correct.
'''

# imports #####################################################################

# modules
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
plt.style.use('seaborn-v0_8-poster')
from labellines import labelLine, labelLines
from scipy.stats import linregress

# external files
import BacStroke as bs
import Functions as f

###############################################################################

#able to call the main function from BacStroke here using this command
#bs.main()

def main():
    
    # configuration file path
    config_file_path = 'test_config.txt'
    
    # reading in each initial condition file name from Object_initial_conditions
    arr = os.listdir('Object_initial_conditions')

    # creating values of gravitational strength that we want to test
    g = 9.8 # gravitational acceleration strength [m/s]

    # numerous values of gravitational strength [m/s]
    gs = np.arange(0, 11, 1)*g

    # opening configuration file and setting diffusion and rotation to 0 ######

    # opening config file
    with open(config_file_path, 'r') as file:
        # read a list of lines into data
        data = file.readlines()       
    
    # setting diffusion coefficient and rotation to 0 in config file
    data[10] = '0\n' # \n to ensure new line added, rotation
    data[31] = '0\n' # diffusion
    
    # grabbing total time as variable
    sim_time = float(data[7])

    # and write everything back to config file
    with open(config_file_path, 'w') as file:
        file.writelines(data)
     
    # calculating sedimentation speed for each object at each gs    
    sedimentation_speeds = np.zeros([len(arr), len(gs)]) # sed speed storage array, [number of objects, number of gravs]
    
    # for each object in Object_initial_conditions folder #####################
    for i in range(len(arr)):
        
        # set the initial conditions file #####
        
        # opening config file to edit value of g
        with open(config_file_path, 'r') as file:
            # read a list of lines into data
            data = file.readlines()       
        
        # resetting gravitational acceleration [m/s]
        data[1] = 'Object_initial_conditions/' + arr[i] + '\n'
    
        # and write everything back to config file
        with open(config_file_path, 'w') as file:
            file.writelines(data)
            
        # speed to set swimming too
        swimming_speed = [0.0]    
           
        # setting swimming speed to 0
        f.change_swimming_speed('Object_initial_conditions/' + arr[i], swimming_speed)
         
        # for each gravitational strength measured ############################
        for j in range(len(gs)):
            
            # opening config file to edit value of g #####
            with open(config_file_path, 'r') as file:
                # read a list of lines into data
                data = file.readlines()       
            
            # resetting gravitational acceleration [m/s]
            data[22] = str(gs[j]) + '\n' # \n for keeping config file format
            
            # and write everything back to config file
            with open(config_file_path, 'w') as file:
                file.writelines(data)

            # run BacStroke to get position array saved into bacpos.csv
            bs.main()
            
            # access bacpos file
            data = pd.read_csv("bacpos.csv")
            positions = np.array(data) # in xyz format
            
            # difference between first and last position of object
            displacement_vec = positions[-1] - positions[0]
            displacement_mag = np.linalg.norm(displacement_vec)
            
            # total simulation time
            sedimentation_speeds[i, j] = displacement_mag/sim_time

    # plotting ################################################################
    
    # getting labels for plot legend (removing .txt from file names)
    
    for k in range(len(arr)):
        arr[k] = arr[k].removesuffix('.txt')
     
    # plotting using label lines
    fig, ax = plt.subplots(ncols = 1, nrows = 1, figsize = (12, 8))
    font_prop = fm.FontProperties(size=20)
    
    slopes = np.zeros(len(arr))
    
    for i in range(len(arr)):
        ax.plot(gs, sedimentation_speeds[i], label = arr[i])
        slopes[i] = linregress(gs, sedimentation_speeds[i])[0]
        print(slopes[i])
        
    ax.set_xlabel('g $(m/s^{2})$')
    ax.set_ylabel('Sedimentation speed $(m/s) $')
    ax.set_xscale('log')
    ax.set_yscale('log')
    labelLines(ax.get_lines(), fontproperties = font_prop)
    
# Execute main method, but only when directly invoked
if __name__ == "__main__":
    main()
