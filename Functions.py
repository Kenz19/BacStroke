"""

"""

# Imports #####################################################################

# modules
import random
import numpy as np
import math

###############################################################################

# use np.random.rand
# def gauss(mean, stdev):
#     '''
#     This function creates a gaussian distribution from an input mean and 
#     standard deviation and generates a random value from within the 
#     distribution
    
#     mean: float, mean of gaussian distribution
    
#     stdev: float, standard deviation of gaussian distribution
#     '''
#     return random.gauss(mean, stdev)

def noise():
    '''
    Generates a random 3D noise vector with values picked from a gaussian 
    distribution of mean 0 and standard deviation 1.
    
    :return: [3] numpy array, random 3D vector
    '''
    
    return np.random.rand(3)


def multi_noise(N):
    '''
    Generates multiple 3D noise vectors with xyz components picked from a
    gaussian distribution of mean 0 and standard deviation 1. Conditions of 
    these vectors is that their vector mean must equal 0 (vector) and each one
    must be different.
    
    :param N: integer, number of vectors to be generated
    
    :return noise_
    '''
    
    # generating random 3D vectors and checking for uniqueness
    noise = [] # N 3D vectors
    
    while len(noise) < N:
        # create random vector
        rand_vec = np.random.randn(3) # check for second dimension
        
        # checking for uniquness in vector to already generated ones
        unique_check = all(np.all(rand_vec != i) for i in noise)
        
        # if vector is unique stored to list
        if unique_check:
            noise.append(rand_vec) # comment out
    
    # moving unique vectors to array as easier to work with        
    noise_arr = np.array(noise)   
    #print(noise_arr)
    
    # ensuring the average vector is the 0 vector
    
    # mean vector of all noise vectors combined
    mean = np.mean(noise_arr, axis=0)
    
    # subtracting mean vector to ensure average vector is 0
    noise_new = noise_arr - mean # could end up back at the origin
    #print(noise_new)
    #print(np.mean(noise_new, axis=0)) # sufficiently small, each component 10-17
    
    return noise_new

def multinoise(N):
    
    noise = np.random.rand(N,3)
    
    return noise

#print(multinoise(20))

# not 100% sure this is needed
def diffusion(diffusion_coefficient, dt, noise_vector):
    '''
    This function calculates the diffusion velocity component
    
    :param diffusion_coefficient: float, diffusion coefficient
    :param dt: float, timestep of simulation in seconds
    :param noise_vector: [3] numpy array, xyz components of random noise
    
    :return: [3] numpy array, xyz components of velocity from diffusion
    '''
        
    return np.sqrt(2*diffusion_coefficient/dt)*noise_vector

        

