'''
This code is intended to be the main line for simulating bacteria swimming 
within a rotating clinostat.
'''

# Imports #####################################################################

# modules
import numpy as np
import matplotlib.pyplot as plt

# external files
import Functions as f 

# class
from Bacteria3D import Bacteria3D as bac
  
###############################################################################

# defining constants
viscosity_coefficient = 1E-3 #PaS, water at room temp
diffusion_coefficient = 0.02E-6 #m^2/S !!! CHECK THESE UNITS
density = 1000 #kg/m3, water
g = 9.8 #gravity, m/s2
a = 1E-6 # size of bacteria, m

def main():
    
    #t1 = time.time()
    # FILE INITIALISING #######################################################
    
    # opening config file containing all file paths needed to execute code
    config_file = 'test_config.txt' # path to config file
    configuration = open(config_file, "r")
    
    # obtaining file names from config file
    inputfile_name = configuration.readline().rstrip() # input data file (containing becteria initial conditions)
    # !!! this can probably be generated for when N gets high
       
    # Determining length of inputfile = no. bacteria in system   
    with open(inputfile_name, 'r') as fp:
        lines = len(fp.readlines()) # no. bacteria present
     
    #print(lines)
    fp.close() # close input file to ensure no mess
    
    infile = open(inputfile_name, "r")# opening input file to use
    #lines = len(fp.readlines()) # might be more efficient than while loop above, although more risky?
    
    bacteria = [] # will contain instances of Bacteria3D
    
    # initialising bacteria instances
    for i in range(lines):
        bacteria.append(bac.new_b3d(infile))
        
    #print(bacteria) # checked to see if correct number of bacteria appear - they do :D
    
    # We now have a list of bacteria created as point particle instances from
    # the bacteria3D class 
    
    # GENERATING INITIAL CONDITIONS ###########################################
    
    initial_positions = np.zeros([lines, 3])
    
    # reading inital position of bacteria
    for i in range(len(bacteria)):        
            # Saving initial positions
            initial_positions[i] = bacteria[i].pos
      
    #print(initial_positions)
    
    # Setting up initial parameters
    time = 0.0 # in seconds
    dt = float(configuration.readline()) # Length of each timestep (seconds)
    total_time = int(configuration.readline()) # Total simulation length (seconds)
    numstep = round(total_time/dt) # number of steps that sim will consist of, rounded to int as used as np sizing
    
    # Storage for data
    pos_array = np.zeros([lines, numstep, 3]) # xyz position of every bacteria every timestep
    time_array = np.zeros(numstep)
    
    # generating N random noise vectors (N = numstep)
    #noise = np.zeros([lines, numstep+1, 3])
    #noise_vectors = f.multi_noise(numstep+1) # all working okay so far, generates the a number of vectors equivalent to numstep
    # + 1 for an extra vector for the initial velocity
    #print(noise_vectors)
    # for i in range(lines):
    #     noise_vectors = f.multi_noise(numstep+1)
    #     noise[i] = f.multi_noise(numstep+1) 
    
    #print(noise)
    # establishing initial velocity of each bacteria
    
    for i in range(lines):
        bacteria[i].terminal_vel(viscosity_coefficient, density, g, a)
        #bacteria[i].initial_vel(dt, diffusion_coefficient, noise_vectors[-1]) # figure out how to do within class - will improve efficiency
    
    # BEGINNING OF TIME INTEGRATION  ##########################################
    
    for i in range(numstep):  # Anything that happens per each timestep 
        print('Progress: ' + str(i+1) + ' out of ' + str(numstep)) # this prints quickly telling me that the loop is very quick
        time += dt
        time_array[i] = time
        for j in range(lines): # Anything for each particle
             
            noise = np.random.normal(0, 1, size=3)
            #print(noise)
            # establishing initial particle velocity
            #bacteria[j].initial_vel(viscosity_coefficient, density, g, a)
            
            # updating bacterial velocity
            #diffusion = noise[j, i]*np.sqrt(2*diffusion_coefficient/dt)
            #print(diffusion)
            #print(noise[j, i]) # each bacteria using a different noise matrix of vectors from gauss distribution, mean = 0, stdev = 0
            bacteria[j].update_vel(dt, diffusion_coefficient, noise)
            
            # Update position of each object
            bacteria[j].update_pos(dt) 
            pos_array[j, i] = bacteria[j].pos # store each position
            
            # updating bacterial velocity
            ##diffusion = noise[j, i]*np.sqrt(2*diffusion_coefficient/dt)
            #print(diffusion)
            #print(noise[j, i]) # each bacteria using a different noise matrix of vectors from gauss distribution, mean = 0, stdev = 0
           ## bacteria[j].update_vel(dt, diffusion)
            #print(bacteria[j].pos)
    
            #time_array[i] = time
            
            #print('Progress: ' + i + ' out of ' + numstep + 'completed') 
            
   # print(pos_array) # all of the x coords
    
    # coordinate visualisation
    #bacteria 1
    x_coords = pos_array[0,:,0] # bacteria number, numstep (all of sim), coordinate
    y_coords = pos_array[0,:,1]
    z_coords = pos_array[0,:,2]
    
    #bacteria 2
    x_coords1 = pos_array[1,:,0] # bacteria number, numstep (all of sim), coordinate
    y_coords1 = pos_array[1,:,1]
    z_coords1 = pos_array[1,:,2]   
    
    #bacteria 2
    # x_coords2 = pos_array[2,:,0] # bacteria number, numstep (all of sim), coordinate
    # y_coords2 = pos_array[2,:,1]
    # z_coords2 = pos_array[2,:,2]
    
    #loc = ticker.MultipleLocator(.5)
    
    #ax.yaxis.set_minor_locator(loc)
    
    fig,ax = plt.subplots(1,2, figsize = (12,5))
    ax[0].scatter(x_coords, z_coords, s=2)
    ax[0].scatter(x_coords1, z_coords1, s = 2)
    #ax[0].scatter(x_coords2, z_coords2)
    
    ax[0].set_xlabel('x', fontsize = 15)
    ax[0].set_ylabel('z', fontsize = 15)
    #ax[0].yaxis.set_minor_locator(loc)
    
    ax[1].scatter(time_array, y_coords, s = 2)
    ax[1].scatter(time_array, y_coords1, s = 2 )
    #ax[1].scatter(time_array, y_coords2)
    ax[1].set_xlabel('t (s)', fontsize = 15)
    ax[1].set_ylabel('y', fontsize = 15)
    fig.suptitle('Sim length = ' + str(total_time) + 's' + ', dt = ' + str(dt) + 's', fontsize=20)
    
    
    #plt.plot()
# Execute main method, but only when directly invoked
if __name__ == "__main__":
    main()