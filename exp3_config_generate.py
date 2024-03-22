'''
This script generates all of the configuration & initalcondition files
needed for experiment 1 and stores them within this directory

!!!  need to add code to copy defualt files into directory instead of just
# manual copy paste
'''

# imports #####################################################################

# modules
import numpy as np
import os
import shutil

# external files
import Functions as f

# Generate folders ############################################################

# create storage directories for configuration and initialconditions files
directory_path_config = 'Exp3_config_files'
directory_path_conditions = 'Exp3_initalconditions_files'

if not os.path.exists(directory_path_config): 
      
    # if the directory is not present  
    # then create it. 
    os.makedirs(directory_path_config)
    
if not os.path.exists(directory_path_conditions): 
      
    # if the directory is not present  
    # then create it. 
    os.makedirs(directory_path_conditions)
    
    # # copy default config file to this directory
    # default_path = os.path.dirname(os.path.dirname(os.path.abspath('initialconditions.txt'))) # fetch path to inital conditions file
    # print(default_path)
    # shutil.copy(default_path, directory_path_config)

# define omega (w) & vs values ########################################################

# get omega values that produce equivalent g from exp 1. 

# omega depends on distance from axis of rotation therefore choose r that
# is consistent - centripetal acceleration doesnt drastically change over the
# range of the clinostat therefore just choose largest radius

r = 4.95E-2 # m, just inside the clinostat radius
g = np.array([0, 0.01, 0.03, 0.1, 0.3, 1, 3])*9.8 # [m/s^2] gravities from exp1

# omega [rad/s]
omega = np.sqrt(g/r)

# converting to clinostat rotation rate [RPM], for config file format
w = omega*60/(2*np.pi)

# same swimming speeds as exp1
vs = np.array([0, 0.1, 0.3, 1, 3, 10, 30])*25E-6 # [m/s] swimming speeds

# create configuration files ##################################################

# !!! need to add code to copy defualt files into directory instead of just
# manual copy paste

for i in range(len(w)):
    for j in range(len(g)):
        
        roundedg = round(g[j], 5)
        roundedw = round(omega[i], 3)
        
        new_config_path = 'Exp3_config_files/omega=' + str(roundedw) + ',g=' + str(roundedg)
        
        # create new config file by copying default config file 
        shutil.copyfile('C:/Users/kenzi/Documents/Masters/BacStroke2.0/BacStroke2.0/Studies/Exp1/Exp1_config_files/g=0.0', new_config_path)
        
        # open new file and change g
        with open(new_config_path, 'r') as file:
            data = file.readlines()       
        
        # setting diffusion coefficient and rotation to 0 in config file
        data[10] = str(w[i]) + '\n' # \n to ensure new line added, rpm
        data[22] = str(g[j]) + '\n' # gravity m/s^2
    
        # and write everything back to config file
        with open(new_config_path, 'w') as file:
            file.writelines(data)
        
# create initial conditions files #############################################

for j in range(len(vs)):
    
    # name if new initial conditions file
    new_ic_path = 'Exp3_initalconditions_files/vs=' + str(vs[j])
    
    # create copy of default ic file under new name
    shutil.copyfile('Exp3_initalconditions_files/initialconditions.txt', new_ic_path)
    
    # change swimming speed in new ic file
    f.change_swimming_speed(new_ic_path, [vs[j]])