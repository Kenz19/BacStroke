
"""
This script runs experiment 3.

Runs each combination of config and inital conditions file, 20 times
"""

# imports #####################################################################

import numpy as np
import os

import BacStroke as bac
import Functions as f

###############################################################################

# getting config file names
config_path = "Exp3_config_files"
config_list = os.listdir(config_path) # index removes unwanted files
config_list.pop(config_list.index('test_config.txt')) # remove default file
print(config_list)
# getting intitial condition file names
ic_path = "Exp3_initalconditions_files"
ic_list = os.listdir(ic_path)
ic_list.pop(ic_list.index('initialconditions.txt')) # remove default file 

# running experiment ##########################################################

# cycling through configuration file
for config in range(len(config_list)):
    print(config)
    # config file currently in loop
    current_config = 'Exp3_config_files/' + config_list[config]
    
    print(config_list[config])
    
    # changing initial conditions file within config
    for ic in range(len(ic_list)):
        
        # initial conditions file currently in loop
        current_ic = 'Exp3_initalconditions_files/' + ic_list[ic]
        
        # open config file
        with open(current_config, 'r') as file:
            data = file.readlines()       
        
        # replace name with new initial conditions file
        data[1] = current_ic + '\n' # \n to ensure new line added, ic file

        # and write everything back to config file
        with open(current_config, 'w') as file:
            file.writelines(data)
        
        # name of folder to store data for this config + ic set
        #direct = 'Exp3_data/' + config_list[config] + ',' + ic_list[ic]
        direct = 'D:\MPhys\ExpData/Exp3/' + config_list[config] + ',' + ic_list[ic]
        
        # create folder to read data into
        if not os.path.isdir(direct): # check if folder exists
            os.makedirs(direct)
        
        # run bacstroke with configuration 20 times
        for i in range(20): # change back to 20 !!!
        
            #print('hello')
            #print(config_list[config], i)
            
            # create folder for this runs output
            output_folder = direct + '/run_' + str(i+1)
            
            # creat output folder if it doesnt exist
            if not os.path.isdir(output_folder):
                os.makedirs(output_folder)
                
            
            positions_folder = output_folder + '/positions.csv'
            
            # run simulation if positions file doesnt exist
            if not os.path.isfile(positions_folder): # check if folder exists
                #os.makedirs(output_folder)
                
                f.change_starting_coords(current_ic, f.sample_from_hollow_cylinder(0.5E-2, 5E-2, 4E-2))
                    
                # run backstroke
                print(current_config)
                bac.main(current_config, output_folder + '/positions.csv', output_folder + '/tumbles.csv', output_folder + '/time.csv', output_folder + '/swimming_direction.csv', output_folder + '/trajectory.png')
    