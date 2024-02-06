'''
This script is the main simulation script for BacStroke. It runs a simulation
of a single bacterium within a clinostat based on parameters found within the
configuration file. 

The bacteriums position within the clinostat is updated at each timestep
within the simulation using a velocity verlet integrator. Its movement is 
based on velocity contribution from 6 different components:
    
    Gravity
    Diffusion
    Bacterial swimming
    Bacterial Tumbling
    Centripetal force
    Clinostat rotation
    
Any one of these parameters can be turned off via the configuation file, with the
exception of swimming. This is turned off by setting the swimming
velocity in the initial conditions file to 0 (last element in the line).
'''

# Imports #####################################################################

# modules
import numpy as np
import matplotlib.pyplot as plt

# reseting style sheet - if an error occurs this may be the cause
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)

# external files
import Functions as f 

# class
from Bacteria3D import Bacteria3D as bac
  
###############################################################################

def main(config_file, output_file, tumble_file, time_file, swimming_file, figure_output_file):
    '''
    Main BacStroke function. This function runs the main simulation. 
    '''
    
    ### 1. READ CONFIGURATION FILE ###
    
    # opening config file containing all file paths needed to execute code
    file = open(config_file, "r")
    
    # reading every entry from configuration file (containing constants etc)
    config = file.readlines()[1::3] # this will be in order of items in the config file
    
    # removing trailing new line (\n) (general formatting)
    for i in range(len(config)):
        config[i] = config[i].rstrip()
    
    # get initial conditions file from first line of config
    inputfile_name = config[0] # input data file (containing becterium initial conditions)
    
    # Determining length of inputfile = no. bacteria in system   
    with open(inputfile_name, 'r') as fp:
        lines = len(fp.readlines()) # no. bacteria present 
        
    fp.close() # close input file to ensure no mess or overwriting
    
    # open initial conditions file
    infile = open(inputfile_name, "r")

    bacteria = [] # will contain instances of Bacteria3D, i.e initial conditions of each bacterium
    
    # read bacteria instances from inital conditions file
    for i in range(lines):
        bacteria.append(bac.new_b3d(infile))
        
    ### 2. DEFINING INITIAL CONDITIONS AND CONSTANTS OF CLINOSTAT SYSTEM ###
        
    # Time parmeters of simulation
    time = 0.0 # [s]
    dt = float(config[1]) # length of each timestep [s]
    total_time = float(config[2]) # total length of similation [s]
    numstep = round(total_time/dt) # number of steps that simulation will take, rounded to int as used as np sizing
    
    # rotation parameters 
    clino_rotation_rate = float(config[3]) # rotation rate of clinostat [RPM]
    omega = clino_rotation_rate*2*np.pi/60 # converting rotation rate to angular velocity [rad/s]
    
    # physical clinostat parameters
    R = float(config[4]) # radius of circular face of clinostat [m]
    r = float(config[5]) # inner radius of clinostat on circular face [m]
    H = float(config[6]) # length of clinostat down the z axis [m]
    
    
    # system constants
    density = float(config[7]) # density of medium in clinostat [kg/m^3]
    g = float(config[8]) # acceleration due to gravity [m/s^2]
    rotational_diffusion_coefficient = float(config[9]) # inversely proportional to time it takes bacterium to forget direction its travelling in [1/s]
    viscosity_coefficient = float(config[10]) # viscosity coefficient of clinostat medium at room temp [Pa/s] (water during testing)
    diffusion_coefficient = float(config[11]) # diffusion coefficient for medium within clinostat at room temp [m^2/s]
    tumbling_rate = int(config[12]) # how often in a second a bacterium should tumble
    
    # We now have a list of bacteria created as point particle instances from
    # the bacteria3D class 
    
    ### 3. GENERATING INITIAL CONDITIONS ###

    # array to store inital positions of each bacteria
    initial_positions = np.zeros([lines, 3])
    
    # reading inital position of bacteria
    for i in range(len(bacteria)):        
            # Saving initial positions to previously defined array
            initial_positions[i] = bacteria[i].pos

    # Storage for data
    pos_array = np.zeros([lines, numstep, 3]) # xyz position of every bacteria every timestep
    time_array = np.zeros(numstep) # tracking simulation time [s]
    tumble_array = np.zeros(numstep) # mark when a bacterium tumbles with a 1, 0 if not
    swim_direction = np.zeros([lines, numstep, 3]) # tracking magnitude of swimming vector (done for external test)
    
    # initialising velocity terms (generate the velocity in the first step via Bacteria3D)
    for i in range(lines):
        bacteria[i].terminal_vel(viscosity_coefficient, density, g) # terminal velocity due to gravity
        bacteria[i].rotational_vel(omega) # rotational velocity of the clinostat
        
        # initial planar position on circular face (needed for centripetal force)
        x = initial_positions[i][0]
        y = initial_positions[i][1]
        planar_pos = np.array([x, y, 0])
        
        bacteria[i].centripetal_force(viscosity_coefficient, density, omega, planar_pos) # centripetal velocity
    
    ### 4. BEGINNING OF TIME INTEGRATION (VELOCITY VERLET) ###
    
    for i in range(numstep):  # Anything that happens per timestep 
        
        # progress tracking for loop
        #print('Progress: ' + str(i+1) + ' out of ' + str(numstep)) # uncomment out for progress bar
        
        time += dt # establishing current time in simulation
        time_array[i] = time # storing current time in simulation
        
        for j in range(1): # Anything for each bacterium
  
            # radius of bacterium
            a = bacteria[j].rad
  
            # updating velocity of each bacterium [m/s]
            bacteria[j].update_vel(dt, diffusion_coefficient)
            
            ### 5. BOUNDRY CONDITIONS ###

            # apply xy boundry conditions if applicable
            
            #position on a 2D circle (set z = 0)
            planar_position = bacteria[j].pos - [0, 0, bacteria[j].pos[2]]
            planar_magnitude = np.linalg.norm(planar_position)
            
            # zone where boundry conditions are applied
            outer_bc_zone = R - a # outer radius minus bacterium radii
            inner_bc_zone = r + a # inner radius plus bacterium radii
                
            # if bacterium position, r, within 1 bacterial radii from the edge, apply boundry conditions
            if planar_magnitude >= outer_bc_zone:
                
                # last updated velocity of bacterium
                current_vel = bacteria[j].vel

                # radial magnitude and direction of the velocity
                planar_rad_mag, planar_rad_dir = f.radial_velocity(planar_position, bacteria[j].vel)
                
                # removing radial component of velocity, i.e setting velocity to its tangential component
                bacteria[j].vel = current_vel - (planar_rad_mag*planar_rad_dir)
                             
                # saving swimming direction for output later
                swim_direction[j, i] = bacteria[j].swim_direction # saving swimming direction
                
                # radial direction of position
                rad_dir = np.copy(bacteria[j].pos)
                rad_dir[2] = 0
                rad_dir /= np.linalg.norm(rad_dir)
                
                # moving bacterium to outside of boundry condition zone (but remain inside clinostat)
                frac = 0.1  #Fraction of body size to set inside outer_bc_zone (make parameter later)
                pos_z = bacteria[j].pos[2] # storing z coord of bacterium
                bacteria[j].pos = (R - (1.0 + frac)*a)*rad_dir # setting position to some fraction outside the boundry zone but inside the clinostat, this only sets xy parameters
                bacteria[j].pos[2] = pos_z # setting z parameter back to original
                pos_array[j, i] = bacteria[j].pos # storing new position
                
                # saving variables for output
                
                # getting the swimming direciton vector for saving to output.
                tumble = bac.tumble_probability(dt, tumbling_rate) # does bacterium tumble? 1 = yes, 0 = no
                tumble_array[i] = tumble
                               
                # # apply end boundry conditions if applicable, along side wall conditions
                
                # just before one wall
                if bacteria[j].pos[2] >= (H - a): 
                    
                    # updating z position and re-recording the position
                    bacteria[j].pos[2] = H - (2*a)
                    pos_array[j, i] = bacteria[j].pos
                
                # close to the other wall
                if bacteria[j].pos[2] <= (0 + a):
                    
                    # updating z position and re-recording the position
                    bacteria[j].pos[2] = 0 + (2*a)
                    pos_array[j, i] = bacteria[j].pos
            
            # apply inner wall boundry conditions, if applicable
            elif planar_magnitude <= inner_bc_zone:
                
                #print(planar_magnitude, inner_bc_zone)
                
                # last updated velocity of bacterium
                current_vel = bacteria[j].vel

                # radial magnitude and direction of the velocity
                planar_rad_mag, planar_rad_dir = f.radial_velocity(planar_position, bacteria[j].vel)
                
                # removing radial component of velocity, i.e setting velocity to its tangential component
                bacteria[j].vel = current_vel - (planar_rad_mag*planar_rad_dir)
                
                # saving swimming direction for output later
                swim_direction[j, i] = bacteria[j].swim_direction # saving swimming direction
                
                # radial direction of position
                rad_dir = np.copy(bacteria[j].pos)
                rad_dir[2] = 0
                rad_dir /= np.linalg.norm(rad_dir) # planar radial unit vector of current position
                
                # moving bacterium to outside of boundry condition zone
                frac = 0.1   #Fraction of body size to set inside inner_bc_zone (make parameter later)
                pos_z = bacteria[j].pos[2] # storing z coord of bacterium
                bacteria[j].pos = (r + (1.0 + frac)*a)*rad_dir # setting position to some fraction outside the boundry zone but inside the clinostat, this only sets xy parameters
                bacteria[j].pos[2] = pos_z # setting z parameter back to original
                pos_array[j, i] = bacteria[j].pos # storing new position
                
                # # saving variables for output
                
                # getting the swimming direciton vector for saving to output.
                tumble = bac.tumble_probability(dt, tumbling_rate) # does bacterium tumble? 1 = yes, 0 = no
                tumble_array[i] = tumble
                
                # apply end boundry conditions if applicable, along side wall conditions
                
                # just before one wall
                if bacteria[j].pos[2] >= (H - a): 
                    
                    # updating z position and re-recording the position
                    bacteria[j].pos[2] = H - (2*a)
                    pos_array[j, i] = bacteria[j].pos
                    
                    #bacteria[j].vel[2] = 0
                
                # close to the other wall
                if bacteria[j].pos[2] <= (0 + a):
                    
                    # updating z position and re-recording the position
                    bacteria[j].pos[2] = 0 + (2*a)
                    pos_array[j, i] = bacteria[j].pos
                    
                    # setting z velocity to be 0, therefore velocity only in xy plane
                    #bacteria[j].vel[2] = 0
            
            # upper z boundry condition
            elif bacteria[j].pos[2] >= (H - a): 
                
               # updating z position and re-recording the position
               bacteria[j].pos[2] = H - (2*a)
               pos_array[j, i] = bacteria[j].pos
               
               bacteria[j].vel[2] = 0
             
            # lower z boundry condition   
            elif bacteria[j].pos[2] <= (0 + a):
                
                # updating z position and re-recording the position
                bacteria[j].pos[2] = 0 + (2*a)
                pos_array[j, i] = bacteria[j].pos
                
                bacteria[j].vel[2] = 0

            ### end of boundry conditions
                
            # dont apply wall boundry conditions
            else:
                
                # updating velocity of each bacterium [m/s]
                #bacteria[j].update_vel(dt, diffusion_coefficient) - this makes the bacterium spiral outwards
                
                # Update position of each bacterium, using updated velocity
                bacteria[j].update_pos(dt) 
                pos_array[j, i] = bacteria[j].pos # store each position
                
                # updating rotational velocity as it depends on position
                bacteria[j].rotational_vel(omega)
                
                # updating the swimming velocity and saving variables
                tumble = bac.tumble_probability(dt, tumbling_rate) # does bacterium tumble? 1 = yes, 0 = no
                tumble_array[i] = tumble
                
                bacteria[j].update_swimming_vel(omega, rotational_diffusion_coefficient, dt, tumble) # updating swimming velocity
                swim_direction[j, i] = bacteria[j].swim_direction # saving swimming direction

    ### 6. SAVING OUTPUT ###            

    # saving parameters to output file
    np.savetxt(output_file, pos_array[0], delimiter=",")
    np.savetxt(tumble_file, tumble_array, delimiter=",")
    np.savetxt(time_file, time_array, delimiter=",") # outputting time for ease of analysis
    #np.savetxt(swimming_file, swim_direction[0], delimiter = ",")

  
 
# Execute main method, but only when directly invoked
if __name__ == "__main__":
    main('config.txt', 'bacpos.csv', 'tumbles.csv', 'time.csv', 'swimming_direction.csv', 'trajectory.png')