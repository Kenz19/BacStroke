# BacStroke
Python code for simulating a dilute (non-interacting) sample of planktonic bacteria swimming within a Clinostat

Files:

BacStoke.py - The main script. The current version of this script takes some initial conditions (from initialconditions.txt) and tracks and plots the trajectories of these bacteria over a specified simulation time from within the configuration file (test_config.txt). 

Positions of bacteria are currently updated under the assumption that their movement is influenced by 6 different components:

Gravity,
Thermal Diffusion,
Clinorotation, 
Centripetal force,
Swimming,
Tumbles,

Bacteria3D.py - This script contains the bacteria3D class which describes the velocity, positional, and physical properties of each bacteria. It has self-functions used to update the position and velocities of the bacteria at each timestep within BacStroke.py. 

initialconditions.txt - Text file containing the initial properties of each bacteria at the start of the simulation. Its format is as follows (all values are floats):

bacterial mass [kg], bacterial radius [m], x position, y position, z position, swimming velocity [m/s]

in the current example, this looks like this:

1E-12 1E-6 0.0 0.0 0.0 20E-6

The origin is defined as (0, 0, 0)

test_config.txt - This file contains the parameters of the simulation. It contains explanations of each parameter in the comments of each line. 

How to use:

Ensure that the following files are downloaded in the same directory:

1. BacStroke.py (file)
2. Bacteria3D.py (file)
3. Functions.py (file)
4. Config.txt (file)
5. Object_initial_conditions (folder) with all inner files
6. plot_bacpos.py (folder)

Once this is completed either run BacStroke.py from the terminal (ensure you navigate the directory containing the code first) or from a Python editor to generate a positional data file (default name is bacpos.csv). To visualise this also run plot_bacpos.py. Note that the visualization may need editing as I typically use a specific stylesheet.


