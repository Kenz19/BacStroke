# BacStroke
Python code for simulating a dilute (non-interacting) sample of planktonic bacteria swimming within a Clinostat

Files:

BacStoke.py - The main script. The current version of this script takes some initial conditions (from initialconditions.txt) and tracks and plots the trajectories of these bacteria over a specified simulation time from within the configuration file (test_config.txt). 

Positions of bacteria are currently updated under the assumption that their movement is only influenced by gravity and diffusion, but effects from rotation by the clinostat and bacterial swimming (run and tumble motion) will be added in due course. There is currently no ability to place limits on the size of the clinostat so bacteria may travel infinitely far if the simulation is run for long enough but again this will be added in due course.

Bacteria3D.py - This script contains the bacteria3D class which describes the velocity, positional, and physical properties of each bacteria. It has self-functions used to update the position and velocities of the bacteria at each timestep within BacStroke.py. 

initialconditions.txt - Text file containing the initial properties of each bacteria at the start of the simulation. Its format is as follows (all values are floats):

bacterial mass [kg], bacterial radius [m], x position, y position, z position.

in the current example, this looks like this:

1E-12 1E-6 0.0 0.0 0.0

Currently, the origin is defined as (0, 0, 0)

test_config.txt - This file contains the parameters of the simulation. Its format is as follows:

initialconditions.txt # file containing initial parameters of bacteria
timestep of simulation [s]
Simulation length [s]


