"""
Generate MSD file for each run of each config
"""

### imports

import numpy as np
import os
import OptimisedMSD as MSD

###

def main():
    
    N = 1
    
    #output_files = []
    #positions_files = []
    #time_files = []
    #N_list = []

    time_path = 'C:/Users/kenzi/Documents/Masters/BacStroke2.0/BacStroke2.0/Studies/Exp2/timenew230324.csv' # path to time file
    
    # get names of each configuration folder
    config_folders = 'D:/Kenzie_Mphys/Data/Exp2/Raw2/'
    config_list = os.listdir(config_folders)
    
    # for each congfiguration folder
    for i in range(len(config_list)):
        
        # define path to current config from this directory
        path_to_config = config_folders + '/' + str(config_list[i]) 
        print(path_to_config)
        
        # get all folders inside current configuration directory
        runs = os.listdir(path_to_config)
        
        # for each iteration of a config
        for j in range(len(runs)):
            
            # path to run file
            run_path = path_to_config + '/' + str(runs[j])
            
            # get path to the positions file
            positions_file_path = run_path + '/positions.csv'  
            
            # define output file name
            output_file = run_path + '/MSD.csv'
            print(output_file)
            
            # if MSD file has not been generated, generate it
            if not os.path.isfile(output_file): # check if folder exists
                #print(config_list[i])
                # if MSD file has not been generated, generate it
                MSD.main(positions_file_path, time_path, output_file, N, 300, 0.1)
            

if __name__ == "__main__":    
    main()
