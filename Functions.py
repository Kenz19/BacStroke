# Imports #####################################################################

# modules
#import random
import numpy as np
import math
import random
import matplotlib.pyplot as plt

#np.random.seed(1912)

###############################################################################

def initialise_swimming_direction():
    '''
    Initialises an initial unit vector direction of bacteria swimming
    by generating two random angles on the unit sphere and converting
    to cartesian coordinates.
    '''
    
    # generating random angles from the circular coordinate system
    # cos theta is generated as this is uniform unlike theta
    costheta = np.random.uniform(0, 1)
    phi = np.random.uniform(0, 2*np.pi)
    
    # components of 3D unit vector on unit circle
    # converting from circular to cartesian coordinates
    x = np.sin(phi)*costheta
    y = np.sin(phi)*np.sqrt(1-costheta**2)
    z = np.cos(phi)
    
    # random unit vector generated from the circular coordinate system
    return np.array([x, y, z])

# #print(initialise_swimming_direction())

# r = initialise_swimming_direction()
# print(np.sqrt(r[0]**2 + r[1]**2 + r[2]**2)) # checking magnitude of random vector = is 1

def tangential_velocity(current_position, planar_position, current_velocity):
    '''
    Inakes the current velocity of a bacterium and returns the tangential component
    of that velocity.
    
    :param current_position: numpy array [3], xyz components of bacteriums current position
    :param planar_position
    '''
    
    # radial unit vector
    radial_unit_vec = planar_position / np.linalg.norm(planar_position)
    
    # radial component of velocity
    radial_magnitude = np.dot(radial_unit_vec, current_velocity)
    
    # 
    tangential_vel = current_velocity - (radial_magnitude*radial_unit_vec)
    
    return tangential_vel

def convert(lst):
    '''
    This function takes a list and converts it into a space separated 
    string.
    
    :param lst: list of any length
    '''
    return ' '.join(lst)

def change_swimming_speed(initial_conditions_file_path, swimming_speeds):
    '''
    This function opens and changes the swimming speed within an inital
    condition file. The swimming velocity is a supplied parameter, if there
    is multiple lines the initial conditions file then the number of elements
    in the swimming_velocities list or array must match the length of lines in 
    the initial conditions file.
    
    :param initial_conditions_file_path: string, file path to initial conditions file
    :param swimming_speeds: array or list (length equal to number of lines in
    initial conditions file) containing the swimming velocities that are to be
    appended.
    
    '''
    
    # opening initial conditions file
    with open(initial_conditions_file_path, 'r') as file:
        # read each line in configuration file
        data = file.readlines()       
    
    # list of data where each element is a line in the initial conditions file
    lists = []    
    
    # splitting each line and reassigning the desired swimming speed value
    for i in range(len(data)):
        params = data[i].split()
        params[-1] = str(swimming_speeds[i]) + '\n'
        
        # converting split list back into string format
        combined = convert(params)
        # putting params back into correct format for putting back into file
        lists.append(combined)
        
    # and write everything back to config file
    with open(initial_conditions_file_path, 'w') as file:
        file.writelines(lists)
        
def change_starting_coords(initial_conditions_file_path, starting_positions):
    '''
    This function opens and changes the swimming speed within an inital
    condition file. The swimming velocity is a supplied parameter, if there
    is multiple lines the initial conditions file then the number of elements
    in the swimming_velocities list or array must match the length of lines in 
    the initial conditions file.
    
    :param initial_conditions_file_path: string, file path to initial conditions file
    :param starting_positions: n x 3 array where n is the number of lines in the 
    initial conditions file, positions in xyz format.
    '''
    
    # opening initial conditions file
    with open(initial_conditions_file_path, 'r') as file:
        # read each line in configuration file
        data = file.readlines()       
    
    # list of data where each element is a line in the initial conditions file
    lists = []    
    
    # splitting each line and reassigning the desired swimming speed value
    for i in range(len(data)):
        params = data[i].split()
        params[2] = str(starting_positions[0]) # x coord
        params[3] = str(starting_positions[1]) # y coord
        params[4] = str(starting_positions[2]) # z coord
        params[5] = str(params[5]) + '\n' # making sure new line is added
        print(params)
        
        # converting split list back into string format
        combined = convert(params)
        # putting params back into correct format for putting back into file
        lists.append(combined)
        
    # and write everything back to config file
    with open(initial_conditions_file_path, 'w') as file:
        file.writelines(lists)  