'''
This function calculates the rotation period of a bacterium as a function
of rotation.

It also tests numerous starting positions.

The bacteriums velocity is made of 4 components: Gravity, diffusion, swimming 
and clinostat rotation.

In this script everything except the rotation is turned off.

'''
# imports #####################################################################

# modules
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-poster')
import pandas as pd

# external files
import BacStroke as bs
import Functions as f

###############################################################################

def flow_period(positions, centre_coord, sim_length, dt, RPM):
    '''
    This function calculates the period of rotation of an object travelling
    uniformly in a circle around a central location. It calculates this by
    determining the angle swept by the object within the simulation time. It
    does not assume that an object has completed a full orbit.
    
    :param positions: n x D numpy array, n  = no. positions, D = coordinate dimensionality,
    array containing positional coordinates of object rotating in a circle
    :param centre_coord: 1 x D numpy array, coordinate at centre of circle
    :param sim_length: float/integer, length of simulation [s]
    :param dt: float/ integer, timestep of simulation [s]
    
    :returns period: float, time for object to complete 1 rotation around circle [s]
    '''
    
    # determining vector between each position and centre of circle
    sep = positions - centre_coord
    
    # calculating number of steps in simulation
    steps = round(sim_length/dt)
    
    # sweeping angle
    theta = 0.0
    
    # calculating angle swept between each separation vector
    for i in range(1, steps-2):
        
        # magntiude of current separation vector and the next one
        mag1 = np.linalg.norm(sep[i])
        mag2 = np.linalg.norm(sep[i+1])
        
        # calculating angle swept between two separation vectors
        theta += np.arccos(np.dot(sep[i], sep[i+1])/(mag1*mag2))
        
    # if object has completed at least 1 rotation 
    if theta >= 2*np.pi:
        n_rotations = theta/(2*np.pi) # number of rotations completed
        period = sim_length/n_rotations 
    
    # account for partial rotations
    else:
        #period = (2*np.pi*sim_length*dt)/theta
        omega = RPM*2*np.pi/60
        period = 2*np.pi/omega
        
    return period
             
def main():
    
    # file paths
    positions_file_path = 'bacpos.csv' # file containing coordinate positions
    config_file_path = 'test_config.txt' # sim config file corresponding to above positions file
    
    # set diffusion, gravity and swimming to 0 (!!! work on swimming another time)
    # opening config file
    with open(config_file_path, 'r') as file:
        # read a list of lines into data
        data = file.readlines()       
    
    # setting diffusion coefficient and rotation to 0 in config file
    data[22] = '0\n' # \n to ensure new line added, gravity
    data[31] = '0\n' # diffusion
    
    # grabbing needed variables from config, needs to be tidied (config function)
    initial_conditions_path = data[1].strip()
    sim_time = float(data[7])
    dt = float(data[4])
    R = float(data[13]) # clinostat radius, m
    dR = (R/100)*5 # 5% of clinostat radius
    r = 0.5E-2
    
    print(sim_time, dt, R, dR)

    # and write everything back to config file
    with open(config_file_path, 'w') as file:
        file.writelines(data)
   
    # speed to set swimming too
    swimming_speed = [0.0]    
       
    # setting swimming speed to 0
    f.change_swimming_speed(initial_conditions_path, swimming_speed)
       
    # varying values for clinostat rotation [RPM]
    RPM = np.arange(1, 11, 1)
    
    # setting various starting positions
    # just above inner radius, Half way from centre, just below outer radius
    starting_positions = np.array([[r + dR, 0, 0], [R/2, 0, 0], [R - dR, 0, 0]])
    
    # rotation periods for each starting position at each clino rotation rate
    period = np.zeros([len(starting_positions), len(RPM)])

    for j in range(len(starting_positions)):
        
        # changing starting position in initial conditions file
        f.change_starting_coords(initial_conditions_path, starting_positions[j])
        print(starting_positions[j])
        
        # running simulation for each rotation value
        for i in range(len(RPM)):
        
            # SETTING CLINOSTAT ROTATION ####
        
            # open config file
            with open(config_file_path, 'r') as file:
                # read a list of lines into data
                data = file.readlines()       
                
                # resetting rotation rate of clinostat
                data[10] = str(RPM[i]) + '\n'
                
                # and write everything back to config file
            with open(config_file_path, 'w') as file:
                file.writelines(data)
                
            #print(RPM[i])
            # running bacstroke simulation to get new positions
            bs.main()
        
            # getting position file from bacstoke output
            data = pd.read_csv(positions_file_path)
            positions = np.array(data)
        
            # calculating bacterium rotation period for current value of clinostat rotation rate
            centre_coord = [0, 0, 0]
        
            period[j, i] = flow_period(positions, centre_coord, sim_time, dt, RPM[i])
    
    # plotting using label lines
    fig, ax = plt.subplots(ncols = 1, nrows = 1, figsize = (12, 8))
    #ax.scatter(RPM, period)
    plt.yscale('log')
    plt.xscale('log')
        
    labels = ['$r + dR$', '$R/2$', 'R - dR']
    
    for j in range(len(period)):
        print(period[j, :])
        ax.scatter(RPM, period[j, :], label = labels[j])
        
    ax.set_xlabel('Rotation rate $(RPM)$')
    ax.set_ylabel('Rotation Period $(s) $')
    ax.legend()
    plt.show()
    
if __name__ == "__main__":
    main()

