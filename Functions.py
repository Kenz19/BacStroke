'''
This script contains functions used throughout the other scripts contained within
the BacStroke Repository.
'''

# Imports #####################################################################

# modules
import numpy as np
import math
import random

###############################################################################

# def initialise_swimming_direction():
#     '''
#     Initialises an initial unit vector direction of bacteria swimming
#     by generating two random angles on the unit sphere and converting
#     to cartesian coordinates.
#     '''
    
#     # generating random angles from the circular coordinate system
#     # cos theta is generated as this is uniform unlike theta
#     costheta = np.random.uniform(0, 1)
#     phi = np.random.uniform(0, 2*np.pi)
    
#     # components of 3D unit vector on unit circle
#     # converting from circular to cartesian coordinates
#     x = np.sin(phi)*costheta
#     y = np.sin(phi)*np.sqrt(1-costheta**2)
#     z = np.cos(phi)
    
#     # random unit vector generated from the circular coordinate system
#     return np.array([x, y, z])


def initialise_swimming_direction():
    '''
    Initialises an initial unit vector direction of bacteria swimming
    by generating two random angles on the unit sphere and converting
    to cartesian coordinates.
    '''
    
    # generating random angles from the circular coordinate system
    # cos theta is generated as this is uniform unlike theta
    theta = np.random.uniform(0, np.pi)
    phi = np.random.uniform(0, 2*np.pi)
    
    # components of 3D unit vector on unit circle
    # converting from circular to cartesian coordinates
    x = np.sin(phi)*np.cos(theta)
    y = np.sin(phi)*np.sin(theta)
    z = np.cos(phi)
    
    # random unit vector generated from the circular coordinate system
    return np.array([x, y, z])


def initialise_swimming_direction():
    '''
    Initialises an initial unit vector direction of bacteria swimming
    by generating two random angles on the unit sphere and converting
    to cartesian coordinates.
    '''
    
    # generating random angles from the circular coordinate system
    # cos theta is generated as this is uniform unlike theta
    theta = np.random.uniform(0, np.pi)
    phi = np.random.uniform(0, 2*np.pi)
    
    # components of 3D unit vector on unit circle
    # converting from circular to cartesian coordinates
    x = np.sin(phi)*np.cos(theta)
    y = np.sin(phi)*np.sin(theta)
    z = np.cos(phi)
    
    # random unit vector generated from the circular coordinate system
    return np.array([x, y, z])


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
        
        
def radial_velocity(planar_position, current_velocity):
    '''
    This function calculates the magnitude and direction of the radial velocity 
    component of a bacteriums current velocity. 
    
    :param current_position: numpy array [3], xyz components of bacteriums current position
    :param planar_position: numpy array [3], xyz components of bacteriums position with z component set to 0
    :param current_velocity: numpy array [3], xyz components of bacteriums velocity
    
    each of the above parameters need to be from the same timestep
    
    :returns radial_magnitude: magnitude of bacteriums velocity vector in the radial direction [same units as velocity vector]
    :returns radial_unit_vec: direction of bacterium in radial direction from its current position
    '''

    # set velocity and orientation - !!!
    # radial unit vector
    planar_radial_unit_vec = planar_position / np.linalg.norm(planar_position)
    
    # radial component of velocity
    radial_magnitude = np.dot(planar_radial_unit_vec, current_velocity)
    
    return radial_magnitude, planar_radial_unit_vec


def get_unit_vector(vector):
    '''
    Get the unit vector of any unit vector in any coordinate system.
    
    :param vector: array of any length that the unit vector is desired.
    
    :returns unit: array of length vector, unit vector of input vector 
    '''
    
    mag = np.linalg.norm(vector)
    
    unit = vector/mag
    unit_mag = np.linalg.norm(unit)

    return unit, unit_mag


def peclet(swimming_vel, terminal_vel, centripetal_vel, translational_diffusion_coefficent, bacterium_radius):
    '''
    Calculates the three peclet numbers assositated with the bacterium within
    the system
    '''
    
    # common factor present in each peclet number
    common_factor = bacterium_radius/translational_diffusion_coefficent
    
    Ps = swimming_vel*common_factor # swimming peclet number
    Pg = terminal_vel*common_factor # gravitational peclet number
    Pc = centripetal_vel*common_factor # centripetal peclet number
    
    return Ps, Pg, Pc


def sample_hollow_cylinder(r, R, h):
    '''
    This function randomly samples coordinated from a hollow cylindrical system
    and then converts those coorindates into an xyz coordinate frame.

    Parameters
    ----------
    r : float
        Inner radius of cylinder [m].
    R : float
        Outer radius of cylinder [m].
    h : float
        length of cylinder [m].

    Returns
    -------
    xyz : numpy array, shape 3
        xyz coordinates generated from a uniform distribution within a hollow
        cylinder.

    '''
    
    # generate random angle and radius (from central axis) from a uniform 
    # distribution - this gets the radius on circular face of the cylinder
    theta = random.uniform(0, 2*np.pi)
    radii = random.uniform(r, R) # radius is larger than r, smaller than R
    
    # get x and y coords from theta and radii
    x = radii*np.cos(theta)
    y = radii*np.sin(theta)
    
    # generate z coord from uniform distribution
    z = random.uniform(0, h)
    
    # turn coords into a numpy array
    xyz = np.array([x, y, z])
    
    return xyz