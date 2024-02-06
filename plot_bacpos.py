'''
This script plots the output file 'bacpos.csv' (name can be changed) of BacStroke. This only plots the first bacterium.

The plot parameters need to be adjusted as I typically use a specific style sheet that I have edited. It can cause issues on other devices.
'''

### imports ### 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

###

# path to output files of BacStroke
positions_file = 'bacpos.csv'
time_file = 'time.csv'

# fetch positions and convert to numpy array
xyz = pd.read_csv(positions_file)
positions = np.array(xyz) # in xyz format

# fetch times and convert to numpy array
time_table = pd.read_csv(time_file)
times = np.array(time_table) 

# plotting path of bacteria
nopoints = 50

# separate xyz positions
x_coords = positions[:,0]
y_coords = positions[:,1]
z_coords = positions[:,2]

# generate figure
fig,ax = plt.subplots(1,3, figsize = (12,8))

# plot side view, x vs z on ax[0]
ax[0].scatter(x_coords[::nopoints], z_coords[::nopoints], s=5, label = 'Bacteria 1')
ax[0].set_xlabel('x', fontsize = 30)
ax[0].set_ylabel('z', fontsize = 30)
ax[0].tick_params(axis='x', labelsize=20)
ax[0].tick_params(axis='y', labelsize=20)


# plot xy view of circular face on ax[1]
# view of circular face of clinostat
cir = plt.Circle((0, 0), 5E-2, facecolor='#c7c7c7', alpha=1, linewidth=3, linestyle='--', edgecolor='black')#color='darkorange',fill=False)
ax[1].add_patch(cir)
cir2 = plt.Circle((0, 0), 0.5E-2, facecolor='white', alpha=1, linewidth=3, linestyle='--', edgecolor='black')#color='darkorange',fill=False)
ax[1].add_patch(cir2)
ax[1].scatter(x_coords[::nopoints], y_coords[::nopoints], s=5, zorder = 1, label = 'Bacteria 1')
ax[1].set_xlabel('x', fontsize = 30)
ax[1].set_ylabel('y', fontsize = 30)
ax[1].tick_params(axis='x', labelsize=20)
ax[1].tick_params(axis='y', labelsize=20)

# plot y vs t on 
# ax[2].scatter(time_array[::10]/1e2, x_coords[::10], s = 5, label = 'Bacteria 1')
ax[2].plot(times[::nopoints]/1e2, y_coords[::nopoints], '-o', label = 'Bacteria 1')
ax[2].set_xlabel('t ($10^2$s)', fontsize = 30)
ax[2].set_ylabel('y', fontsize = 30)
ax[2].tick_params(axis='x', labelsize=20)
ax[2].tick_params(axis='y', labelsize=20)

#fig.suptitle('', fontsize=30)
plt.savefig('Visualisation.png', dpi = 300)
plt.show()