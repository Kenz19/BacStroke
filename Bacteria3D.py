'''
This class creates a bacteria instance within a 3D system
'''

# Imports #####################################################################

# modules
import numpy as np

# external files
import Functions as f

#np.random.seed(1912)

###############################################################################


class Bacteria3D(object):
    '''
    Class used to describe bacteria modelled as point particles in space
    '''
    
    def __init__(self, mass, position, radius, swimming_vel):
        """
        Initialises a point particle in 3D space

        :param mass: float, mass of the bacteria
        :param position: [3] float array w/ position
        :param radius: float, radius of bacteria assumed to be shape sphere
        """
        
        self.mass = float(mass) # bouyant bacterial mass in kg
        self.pos = np.array(position, float) # bacterial position in [x,y,z], each component in m
        self.rad = float(radius) # bacterial radius in m
        
        # initialising direction of swimming
        self.swim = float(swimming_vel) # swimming speed in m/s, float
        self.swim_direction = f.initialise_swimming_direction() # random initial unit direction for swimming velocity, 3D array of mag 1
        #self.swim_direction = np.array([1, 2, 3])
        self.swim_vel = self.swim*self.swim_direction # swimming velocity in m/s, 3D array [vx, vy, vz]
        
    
    def __str__(self):
        """
        XYZ-compliant string. The format is
        <label>    <x>  <y>  <z>
        """
        xyz_string = f"{self.pos[0]}  {self.pos[1]} {self.pos[2]}" # xyz coords in m from origin
            
        return xyz_string
    
    
# storing old terminal velocity just in case needed
    def terminal_vel(self, viscosity_coeff, density, g):
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
        
        VTy = (0.05*g*density*self.rad**2)/(6*np.pi*viscosity_coeff) # y component of terminal velocity  
        
        self.term_vel = np.array([0, -VTy, 0]) # negative comes from coordinate definition
        
    
    # def terminal_vel(self, viscosity_coeff, fluid_density, g):
    #     '''
    #     Calculates velocity at t = 0 for each bacteria instance.
        
    #     :param viscosity_coeff: float, viscosity coefficient in PaS for liquid in sim.
    #     :param fluid_density: float, density in kg/m^3 for the same liquid
    #     :param object_density: float, density of object in clinostat, kg/m^3
    #     :param g: float, gavitational constant in kg/m^2 for desired environment
    #     '''   
    #     # assuming to be at terminal velocity once in system (can add factor from 23/9/23 notes in not assuming this)
    #     # currently only using Vt and Vd but Vs and Vr will be implemented
        
    #     # as only VT acting then [x] and [z] vel will be 0
        
    #     object_density = self.mass/(np.pi*(4/3)*self.rad**3)
        
    #     bm = self.mass*(1-(fluid_density/object_density))
        
    #     VTy = (bm*g)/(6*np.pi*viscosity_coeff) # y component of terminal velocity  
        
    #     #0.05*g*density*self.rad**2
        
    #     self.term_vel = np.array([0, -VTy, 0]) # negative comes from coordinate definition
        
        
    def rotational_vel(self, omega):
        '''
        This function calculates the rotational velocity of the bacteria
        at its current position.
        
        :param omega: float, rotational speed of clinostat in rad/s
        '''
        x = self.pos[0] # current x position of bacteria
        y = self.pos[1] # current y position of bacteria
        
        self.rot_vel = np.array([-y*omega, x*omega, 0]) # updating the current rotational velocity of the bacteria, calculated from 
    
    
    @staticmethod
    def tumble_probability(dt):
        '''
        Calculates if a bacterium is going to tumble in the current timestep.
        
        Assuming that the rate of tumbling is once per second
        
        :param dt: float, timestep of simulation in s
        '''
        # counting number of decimal places in timestep float
        dps = str(dt)[::-1].find('.')
        
        # generating random number between 0 & 1 with same timestep as dt        
        random_number = round(np.random.uniform(0, 1), dps)
        
        tumbling_rate = 1 # tumble per second
        
        tumble_prob = tumbling_rate*dt # unitless
        
        does_bacterium_tumble = (random_number<=tumble_prob) # returns true or false
        
        return does_bacterium_tumble # true = does tumble, false = does not tumble
        
    
    def update_swimming_vel(self, omega, rotational_diffusion_coefficient, dt):
        '''
        This function updates the swimming velocity of the bacterium.
        
        :param omega: float, rotational speed of clinostat in rad/s
        :param rotational_diffusion_coefficient: float, rotational diffusion coefficient in m^2/s
        :param dt: float, timestep of simulation in s
        '''
        # If tumble_probabilty is true then the bacterium tumbles in a random direction
        if self.tumble_probability(dt) == True:
            #print('tumbling.....................................')
            
            # random new tumbling direction
            new_direction = f.initialise_swimming_direction()           
            magnitude = np.linalg.norm(new_direction)
        
            # updating the swimming direction and then the swimming velocity with that vector
            self.swim_direction = new_direction/magnitude # normalising for unit vector  
            self.swim_vel = self.swim*self.swim_direction
       
        # if tumble probability is false it swims in its new direction
        else:
            #print('swimming')
            # xyz components of current swimming direction unit vector
            ex = self.swim_direction[0]
            ey = self.swim_direction[1]
            #ez = self.swim_direction[2]
        
            # DEFINING RATE OF CHANGE OF SWIMMING UNIT VECTOR #####
        
            # rotation term in rate of change of swimming direction
            rotation = omega*np.array([-ey, ex, 0])
        
            # diffusion term in rate of change of swimming direction
            coeff = np.sqrt((2*rotational_diffusion_coefficient)/dt) # coefficient on second term of rate of change vector
            noise = np.random.normal(0, 1, size=3) # different from noise vector in diffusion velocity (avoids coupling)
            #noise = np.array([1, 2, 3])
            delta = np.identity(3) # rank 2 tensor
            outer_product = np.outer(self.swim_direction, self.swim_direction) # outer product of swimming unit vectors
        
            diffusion_term = coeff*((delta - outer_product)@noise)
            # print(noise)
            # print(delta - outer_product)
            # print((delta - outer_product)@noise)
        
            # rate of change of the swimming unit vector
            dedt = rotation + diffusion_term
            #print(dedt)
        
            # calculating new direction and 
            new_direction = (dedt*dt) + self.swim_direction
            magnitude = np.linalg.norm(new_direction)
        
            # updating the swimming direction and then the swimming velocity with that vecot
            self.swim_direction = new_direction/magnitude # normalising for unit vector  
            #self.swim_vel = self.swim*self.swim_direction


    def update_vel(self, dt, diffusion_coefficient):
        '''
        Calculates velocity at t = 0 for each bacteria instance.
        
        :param dt: float, timestep of simulation
        :param diffusion_coefficient: float, diffusion coefficent of bacteria in medium, in m^2/s
        :param noise: [3] float array, random 3D noise vector taken from a normal distribution (cartesian coords)
        :param rot_vel: [3] float array, 3D vector representing the rotational velocity of a bacteria (cartesian coords)
        
        '''   
        # assuming to be at terminal velocity once in system (can add factor from 23/9/23 notes in not assuming this)
        # currently only using Vt, Vd and Vr but Vs will be implemented
  
        # generating a noise vector from a normal distribution
        noise = np.random.normal(0, 1, size=3)
        
        # diffusion
        diffusion = noise*np.sqrt(2*diffusion_coefficient/dt)
        
        self.vel = self.term_vel + diffusion + self.rot_vel + self.swim*self.swim_direction
        # made swimming change
 
        
    def update_pos(self, dt):
        """
        Updates the position of a Particle 3D instance
        
        :param dt: float, timestep
        """
        
        self.pos += self.vel*dt # adding new position vector to previous position vector
        
        
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
        swimming_vel = float(p[5]) # swimming velocity of bacteria in m/s

        return Bacteria3D(mass, position, radius, swimming_vel) # instance of Bacteria3D class