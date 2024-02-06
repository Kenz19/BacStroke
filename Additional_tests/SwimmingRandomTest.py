"""
This script tests the random number generation within the swimming term.
The first step in the simulation requires the generation of a random unit vector
representing the bacteriums swimming direction.

To generate this vector angles theta and phi are randomly generated within uniform
distributions. As both of these angles allow generation of a random direction
within the unit circle.

Theta is generated via the random generation of a value of cos(theta) between 
the values of 0 and 1 as this distribution is uniform.

Both Phi & Theta are generated randomly as a number between 0 and 2pi.

These values are then used to generate the xyz components of a random direction
by using the polar to cartesian coordinate transformations.

x = r*sin(phi)*cos(theta)
y = r*sin(phi)*sin(theta)
z = r*cos(phi)

where r is one in this case as we are working with unit vectors.
"""

# imports #####################################################################

# modules
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-poster')
import seaborn as sns

# external files
import Functions as f

# seed
np.random.seed(1912)

###############################################################################

# modified version of function in Functions file to output phi and theta
def initialise_swimming_direction():
    '''
    Initialises an initial unit vector direction of bacteria swimming
    by generating two random angles on the unit sphere and converting
    to cartesian coordinates.
    
    :returns: randomly generated unit vector, from the unit sphere, where each 
    component is sampled from a uniform distribution.
    '''
    
    # generating random angles from the circular coordinate system
    # cos theta is generated as this is uniform unlike theta
    #costheta = np.random.uniform(-1, 1)
    #theta = np.arccos(costheta)
    theta = np.random.uniform(0, np.pi)
    phi = np.random.uniform(0, 2*np.pi)
    
    # random unit vector generated from the circular coordinate system
    return theta, phi


def main():
    
    # number of run iterations
    runs = int(1E6)
    
    # theta and phi generated from each run
    theta = np.zeros(runs)
    phi = np.zeros(runs)
    
    # generating all theta and phi angles
    for i in range(runs):
        theta[i] = initialise_swimming_direction()[0]
        phi[i] = initialise_swimming_direction()[1]
    
    # normalising to between 0 and 1
    theta = (theta/np.pi)
    phi = (phi/(2*np.pi))
    
    # plotting PDF function on histogram
    plt.hist(theta, density=True, bins = 50, edgecolor = 'black', label = '$ \Theta $/2$\pi$')
    plt.hist(phi, density=True, bins = 50, label = '$\Phi$/$\pi$', alpha=0.8)
    plt.xlabel('Normalised angle')
    plt.ylabel('PDF')
    plt.legend()
    plt.show()

# Execute main method, but only when directly invoked
if __name__ == "__main__":
    main()
