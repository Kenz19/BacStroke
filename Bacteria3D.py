'''
This class creates a bacteria instance within a 3D system
'''

# Imports #####################################################################

# modules
import numpy as np

# external files
import Functions as f

###############################################################################

class Bacteria3D(object):
    '''
    Class used to describe bacteria modelled as point particles in space
    '''
    
    def __init__(self, mass, position, radius):
        """
        Initialises a point particle in 3D space

        :param mass: float, mass of the bacteria
        :param position: [3] float array w/ position
        :param radius: float, radius of bacteria assumed to be shape sphere
        """
        
        self.mass = float(mass) # bacterial mass in kg
        self.pos = np.array(position, float) # bacterial position in [x,y,z], each component in m
        self.rad = float(radius) # bacterial radius in m
        
    
    def __str__(self):
        """
        XYZ-compliant string. The format is
        <label>    <x>  <y>  <z>
        """
        xyz_string = f"{self.pos[0]}  {self.pos[1]}\
            {self.pos[2]}"
        
        return xyz_string
    
    def terminal_vel(self, viscosity_coeff, density, g, a):
        '''
        Calculates velocity at t = 0 for each bacteria instance.
        
        :param viscosity_coeff: float, viscosity coefficient in PaS for liquid in sim.
        :param density: float, density in kg/m^3 for the same liquid
        :param g: float, gavitational constant in kg/m^2 for desired environment
        :param a: float, bacterial size in m
        '''   
        # assuming to be at terminal velocity once in system (can add factor from 23/9/23 notes in not assuming this)
        # currently only using Vt and Vd but Vs and Vr will be implemented
        
        # as only VT acting then [x] and [z] vel will be 0
        
        VTy = (0.05*g*density*a**2)/(6*np.pi*viscosity_coeff) # y component of terminal velocity  
        
        self.term_vel = np.array([0, -VTy, 0]) # negative comes from coordinate definition
        
    
    # def initial_vel(self, dt, diffusion_coefficient, noise):
    #     '''
    #     Calculates velocity at t = 0 for each bacteria instance.
        
    #     :param dt: float, timestep of simulation
        
    #     '''   
    #     # assuming to be at terminal velocity once in system (can add factor from 23/9/23 notes in not assuming this)
    #     # currently only using Vt and Vd but Vs and Vr will be implemented
        
    #     # as only VT acting then [x] and [z] vel will be 0
        
    #     diffusion = noise*np.sqrt(2*diffusion_coefficient/dt)
        
    #     self.vel = self.term_vel + diffusion # negative comes from coordinate definition
        
    def update_vel(self, dt, diffusion_coefficient, noise):
        '''
        Calculates velocity at t = 0 for each bacteria instance.
        
        :param dt: float, timestep of simulation
        
        '''   
        # assuming to be at terminal velocity once in system (can add factor from 23/9/23 notes in not assuming this)
        # currently only using Vt and Vd but Vs and Vr will be implemented
        
        # as only VT acting then [x] and [z] vel will be 0
        
        diffusion = noise*np.sqrt(2*diffusion_coefficient/dt)
        
        self.vel = self.term_vel + diffusion # negative comes from coordinate definition
        
        
    def update_pos(self, dt):
        """
        Updates the position of a Particle 3D instance
        
        :param dt: float, timestep
        """
        
        self.pos += self.vel*dt 
        
        
    # def update_vel(self, dt, diffusion):
    #     """
    #     Updates the velocity of a particle to 1st order
        
    #     :param dt: float, timestep
    #     :param diffusion: [3] numpy array, diffusion component of velocity
    #     """
        
    #     self.vel = self.term_vel + diffusion 
        
        
    @staticmethod # meaning it could be written as an independant function 
    def new_b3d(file_handle):
        """
        Initialises a Particle3D instance given an input file handle.
        
        The input file should contain one line per particle in the following
        format:
        <mass>  <x> <y> <z>    <vx> <vy> <vz>
        
        :param file_handle: Readable file handle in the above format
        :return: Particle3D instance
        """
        data = file_handle.readline() # file_handle will contain information about bacteria
        p = data.split() # getting info for each individual bacteria
        
        mass = float(p[0]) # bacterial mass in kg
        radius = float(p[1]) # radius of bacteria in m
        position = np.array([p[2],p[3],p[4]], float) # x,y,z component in m from origin

        return Bacteria3D(mass, position, radius) # instance of Bacteria3D class