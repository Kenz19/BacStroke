'''
This code is intended to be the main line for simulating bacteria swimming 
within a rotating clinostat.
'''

# Imports #####################################################################

# modules
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyfit

# external files
import Functions as f 

# class
from Bacteria3D import Bacteria3D as bac

# setting seed for random generators
np.random.seed(1912)
  
###############################################################################

def main():
    
    # 1. FILE INITIALISING ####################################################
    
    # opening config file containing all file paths needed to execute code
    config_file = 'test_config.txt' # path to config file
    file = open(config_file, "r")
    
    # reading every entry from configuration file (containing constants etc)
    config = file.readlines()[1::3]
    
    # removing trailing new line (\n)
    for i in range(len(config)):
        config[i] = config[i].rstrip()
    
    # obtaining file names from config file
    inputfile_name = config[0]# input data file (containing becterium initial conditions)
    # !!! this can probably be generated for when N (no. bacteria) gets high
    
    # Determining length of inputfile = no. bacteria in system   
    with open(inputfile_name, 'r') as fp:
        lines = len(fp.readlines()) # no. bacteria present 
        
    fp.close() # close input file to ensure no mess or overwriting
    
    infile = open(inputfile_name, "r")# opening input file to use

    bacteria = [] # will contain instances of Bacteria3D, i.e initial conditions of each bacterium
    
    # initialising bacteria instances
    for i in range(lines):
        bacteria.append(bac.new_b3d(infile))
        
    # DEFINING INITIAL CONDITIONS AND CONSTANTS OF CLINOSTAT SYSTEM ###########
        
    # Time parmeters of simulation
    time = 0.0 # [s]
    dt = float(config[1]) # length of each timestep [s]
    total_time = float(config[2]) # total length of similation [s]
    numstep = round(total_time/dt) # number of steps that simulation will take, rounded to int as used as np sizing
    
    # clinostat parameters 
    clino_rotation_rate = float(config[3]) # rotation rate of clinostat [RPM]
    omega = clino_rotation_rate*2*np.pi/60 # converting rotation rate to angular velocity [rad/s]
    
    R = float(config[4]) # radius of circular face of clinostat [m]
    H = float(config[5]) # length of clinostat down the z axis [m]
    r = 0.5E-2
    # system constants
    density = float(config[6]) # density of medium in clinostat [kg/m^3]
    g = float(config[7]) # acceleration due to gravity [m/s^2]
    print(g)
    rotational_diffusion_coefficient = float(config[8]) # inversely proportional to time it takes bacterium to forget direction its travelling in [1/s]
    viscosity_coefficient = float(config[9]) # viscosity coefficient of clinostat medium at room temp [Pa/s] (water during testing)
    diffusion_coefficient = float(config[10]) # diffusion coefficient for medium within clinostat at room temp [m^2/s]

    # We now have a list of bacteria created as point particle instances from
    # the bacteria3D class 
    
    # 2. GENERATING INITIAL CONDITIONS ########################################
    
    initial_positions = np.zeros([lines, 3])
    
    # reading inital position of bacteria
    for i in range(len(bacteria)):        
            # Saving initial positions
            initial_positions[i] = bacteria[i].pos

    # Storage for data
    pos_array = np.zeros([lines, numstep, 3]) # xyz position of every bacteria every timestep
    time_array = np.zeros(numstep)
    #MSD = np.zeros(numstep)
    
    # establishing terminal and rotational velocity of bacteria
    for i in range(lines):
        bacteria[i].terminal_vel(viscosity_coefficient, density, g)
        bacteria[i].rotational_vel(omega)
    
    # 3. BEGINNING OF TIME INTEGRATION  #######################################
    
    for i in range(numstep):  # Anything that happens per each timestep 
        
        # progress tracking for loop
        #print('Progress: ' + str(i+1) + ' out of ' + str(numstep))
        
        time += dt # establishing current time in simulation
        time_array[i] = time # storing current time in simulation
        
        for j in range(lines): # Anything for each particle
            #MSD[i] = f.calc_msd_simple(pos_array)   
            # updating velocity of each bacterium [m/s]
            bacteria[j].update_vel(dt, diffusion_coefficient)
            
            # boundary conditions (x & y)
            
            #position on a 2D circle (set z = 0)
            planar_position = bacteria[j].pos - [0, 0, bacteria[j].pos[2]]
            planar_magnitude = np.linalg.norm(planar_position)
            
            # zone where boundry conditions are applied
            bc_zone = R - bacteria[j].rad
                
            # if bacterium position, r, within 1 bacterial radii from the edge, apply boundry conditions
            if planar_magnitude >= (bc_zone):
                current_vel = bacteria[j].vel
                
                # getting the radial magnitude and direction of the velocity
                planar_rad_mag, planar_rad_dir = f.radial_velocity(planar_position, bacteria[j].vel)
                
                # removing the radial component of the velocity
                bacteria[j].vel = current_vel - (planar_rad_mag*planar_rad_dir)
                
                # setting orientation to negative radial direction
                rad_mag, rad_dir = f.radial_velocity(bacteria[j].pos, bacteria[j].vel)
                bacteria[j].swim_direction = -rad_dir
                # print(rad_dir)
                
                # distance of bacterium from wall
                wall_distance = R - planar_magnitude
                d = wall_distance - bacteria[j].rad 
                print(bacteria[j].pos)
                bacteria[j].pos = bacteria[j].pos + d*rad_dir
                print(d*rad_dir)
                print(bacteria[j].pos)


            # Update position of each bacterium, using updated velocity
            bacteria[j].update_pos(dt) 
            pos_array[j, i] = bacteria[j].pos # store each position
            
            # updating rotational velocity as it depends on position
            bacteria[j].rotational_vel(omega)
            
            # updating the swimming velocity
            bacteria[j].update_swimming_vel(omega, rotational_diffusion_coefficient, dt)
     
            
    # saving 1st bacterium positions to output csv file
    np.savetxt('bacpos.csv', pos_array[0], delimiter=",")
    #np.savetxt('tumbles.txt', tumbles, delimiter=",")
    
    # 4. PLOTTING ################################################################
            
    # plotting path of bacteria
    
    x_coords = pos_array[0,:,0]
    y_coords = pos_array[0,:,1]
    z_coords = pos_array[0,:,2]
    
    fig,ax = plt.subplots(1,3, figsize = (24,8))
    ax[0].scatter(x_coords[::10], z_coords[::10], s=5, label = 'Bacteria 1')
    ax[0].set_xlabel('x', fontsize = 15)
    ax[0].set_ylabel('z', fontsize = 15)
    ax[0].legend()
    
    # view of circular face of clinostat
    cir = plt.Circle((0, 0), R, facecolor='#c7c7c7', alpha=1, linewidth=3, linestyle='--', edgecolor='black')#color='darkorange',fill=False)
    ax[1].add_patch(cir)
    cir2 = plt.Circle((0, 0), r, facecolor='white', alpha=1, linewidth=3, linestyle='--', edgecolor='black')#color='darkorange',fill=False)
    ax[1].add_patch(cir2)
    ax[1].scatter(x_coords[::10], y_coords[::10], s=5, zorder = 1, label = 'Bacteria 1')
    ax[1].set_xlabel('x', fontsize = 15)
    ax[1].set_ylabel('y', fontsize = 15)

    # plotting y position against time
    ax[2].scatter(time_array[::10]/1e2, y_coords[::10], s = 5, label = 'Bacteria 1')
    ax[2].set_xlabel('t ($10^2$s)', fontsize = 15)
    ax[2].set_ylabel('y', fontsize = 15)
    fig.suptitle('Sim length = ' + str(total_time) + 's' + ', $\Delta$t = ' + str(dt) + 's' + ', RPM = ' + str(clino_rotation_rate), fontsize=20)
    plt.show()
    
# Execute main method, but only when directly invoked
if __name__ == "__main__":
    main()