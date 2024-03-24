"""
This file intakes an output positions file (csv) from BacStroke.py and plots
the mean square displacement of the bacterium position.

Requirements:
    The output file of Bacstoke.py that is being input into this script must
    correspond to the current configuration file otherwise results will be 
    incorrect.
    If you dont want to use the current cofiguration file, create a copy of the 
    one used to generate the positional data that will be input into the script
    and alter the name of the config file at the top of this script.
"""

# IMPORTS ###

# external libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import time

def main(positions_file, time_file, output_file, N, max_lagtime, dt):
    '''
    

    Parameters
    ----------
    positions_file : string
        File path to positions file from current directory.
    time_file : string
        File path to time file from current directory.
    output_file : string
        file path to outputfile (doesnt need to exist already), csv.
    N : integer
        number of data points to skip periodically to speed up calculation.
    max_lagtime : float
        max lagtime desired.
    dt : float
        timestep of data from positions file.

    Returns
    -------
    Generates output_file in specified directory with 3 columns.
    
    MSD, MQD, lagtime

    '''
    
    #N = every nth data point to use (for optimisation purposes)
    
    # CONFIGURATION FILE READING #####
    
    # # reading in current configuration file for constants and timing etc
    # config_file = config_file # path to config file
    # file = open(config_file, "r")
        
    # # reading every entry from configuration file (containing constants etc)
    # config = file.readlines()[1::3]
        
    # # removing trailing new line (\n)
    # for i in range(len(config)):
    #     config[i] = config[i].rstrip()
    
    # # pulling needed constants from config file
    # t0 = 0.0 # [s]
    # dt = float(config[1]) # length of each timestep [s]
    # total_time = float(config[2]) # total length of similation [s]
    # numstep = round(total_time/dt) # number of simulation steps
    
    no_steps = int(max_lagtime/dt)
    
    
    # POSITION FILE READING ####
    
    data = pd.read_csv(positions_file)
    positions = np.array(data)[0:no_steps:N] # in xyz format
    no_pos = len(positions[0::])

    # storage array for times    
    #t = np.zeros(no_pos)
    
    # # creating time array for specific positions file
    # for i in range(no_pos):
    #     #print(str(i) + 'out of ' + str(no_pos))
    #     t[i] = ((i)*dt) # last element agrees with the total time
   
    #print(t) 
    
    time = pd.read_csv(time_file, header = None)[0:-1]
    #print(time)
    time_arr = time.to_numpy()[0:no_steps:N]
    #print(time_arr)
    
    # print(len(t), len(time))
   
    # MSD AND MQD 
    MSD = np.zeros(no_pos)
    MQD =  np.zeros(no_pos)
    count = np.zeros(no_pos)
    
    for i in range(no_pos):
        print('Progress ' + str(i) + ' out of ' + str(no_pos))
        # new time portion, set current time to starting time
        #t1 = t[i]
        
        # setting positions for this
        pos1 = positions[i]
        
        # calculating MSD for each step inbetween current time i and end time
        for j in range(i,no_pos):
            pos2 = positions[j]
            vec = pos2 - pos1
            dr2 = np.sum(vec*vec)
            dr4 = dr2*dr2
            MSD[j-i] += dr2
            MQD[j-i] += dr4
            count[j-i] += 1.0
    
    # dividing MSD & MQD by count
    for i in range(no_pos):
        if(count[i]>0):
            MSD[i] /= count[i]
            MQD[i] /= count[i]
    
    # write MSD, MQD & lagtime to file
    with open(output_file, 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(zip(MSD, MQD, time_arr))
    
    # # # plot
    # # plt.scatter(t, MSD, s = 5)
    # # plt.xlabel('Lagtime (s)')
    # # plt.ylabel('Mean Square displacement')
    # # plt.xscale('log')
    # # plt.yscale('log')

# Execute main method, but only when directly invoked
if __name__ == "__main__":
    start = time.time()
    main('bacpos.csv', 'time.csv', 'MSD.csv', 10)
    end = time.time()
    print('Time to complete: ' + str(end - start) + 's')

