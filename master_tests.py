'''
This script produces numerous plots on different parameters from within BacStroke
to ensure that the physics is working correctly.

It runs the following scripts one at a time:
    
    SedvsG.py - testing the relation between sedimentation speed and gravity
    TestRotation.py - testing the rotation period against the rotation rate of the clinostat
'''

# imports #####################################################################

# modules #
import matplotlib.pyplot as plt
from matplotlib import style
plt.style.use('seaborn-v0_8-poster')
import numpy as np
import pandas as pd

# external files #
import Functions as f
import BacStroke as bs
import SedvsG as Gtest # sedimentation speed vs gravity test
import TestRotation as Rtest # rotation period against rotation rate
import SwimmingRandomTest as Stest
###############################################################################

# gravity test
Gtest.main()

# setting config file back to Ecoli if not already

# opening config file to edit value of g
with open('test_config.txt', 'r') as file:
    # read a list of lines into data
    data = file.readlines()       

# resetting gravitational acceleration [m/s]
data[1] = 'Object_initial_conditions/Ecoli.txt\n'

# and write everything back to config file
with open('test_config.txt', 'w') as file:
    file.writelines(data)

# rotation test
Rtest.main()

# swimming direction test
Stest.main()


