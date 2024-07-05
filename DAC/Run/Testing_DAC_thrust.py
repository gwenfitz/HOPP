from hopp.simulation import HoppInterface
import numpy as np
import matplotlib.pyplot as plt

from floris.tools import FlorisInterface
import floris.tools.visualization as wakeviz

# hi = HoppInterface('/Users/gfitzsim/github/DAC/Inputs/dac_hopp.yaml')
# fmodel = hi.system.wind.fi

# Load an arbitrary FLORIS input file, which we'll then modify. Assume that 
# a single DAC disc is specified, but we'll set the hub height later

fmodel = FlorisInterface("./DAC/Inputs/gch_dacdisk_turbine.yaml")

dac_disk = fmodel.floris.farm.turbine_definitions[0] # Single disk of DAC stack
# turb = fmodel.floris.farm.turbine_definitions[1] # Wind turbine model

# Now, set up the x, y locations for each of the DACs (two rows of four DACS)
dacs_layout_x = np.array([0, 500, 1000, 1500, 0, 500, 1000, 1500])
dacs_layout_y = np.array([0, 0, 0, 0, 500, 500, 500, 500])
n_dacs = len(dacs_layout_x)

# Generate a list of the "hub heights" of the DAC disks in a single DAC
dac_heights = [2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]

# Generate a list of turbine definitions that specify a single DAC
dac_stack = []
for i, hub_height in enumerate(dac_heights): # Loop over the hub heights
    dac_disk_i = dac_disk.copy() # create a copy of the dictionary
    dac_disk_i["hub_height"] = hub_height
    # Need to rename to avoid a bug
    dac_disk_i["turbine_type"] = "dac-disk-"+str(hub_height)
    dac_stack.append(dac_disk_i)

# Tile this list to match the number of DACs (8, in this case)
dacs_all = dac_stack * n_dacs

# We'll need to extend the  (x,y) layouts to match the number of hub heights
dacs_layout_x = np.repeat(dacs_layout_x, len(dac_heights)).tolist()
dacs_layout_y = np.repeat(dacs_layout_y, len(dac_heights)).tolist()

""""
# Check it worked... expect 2, 2.5, 4.5, 2 for the hub heights,
# at the (0,0) DAC and then the (500,0) DAC
print("Some DAC locations before assignment (x, y, height):")
for i in [0, 1, 5, 6]:
    print(dacs_layout_x[i], dacs_layout_y[i], dacs_all[i]["hub_height"])


# Now, we'll create the layout and list of actual wind turbines
turbs_layout_x = [2000, 2000, 4000, 4000]
turbs_layout_y = [0, 2000, 0, 2000]
turbs_all = [turb] * len(turbs_layout_x) # List of 4 turbines
"""

# Join the layouts of DACs and turbines, as well as their dictionary lists
layout_x = dacs_layout_x # + turbs_layout_x
layout_y = dacs_layout_y # + turbs_layout_y
type_defs = dacs_all # + turbs_all

# Assign and check again
# might need to include reinitialized wind info here too
fmodel.reinitialize(layout_x=layout_x, layout_y=layout_y, turbine_type=type_defs)

""""
print("\n\nSome DAC locations after assignment (x, y, height):")
for i in [0, 1, 5, 6]:
    print(
        fmodel.layout_x[i],
        fmodel.layout_y[i],
        fmodel.floris.farm.turbine_map[i].hub_height,
    )

print("\n\nLocation of the last turbine (x, y, hub height):")
print(
    fmodel.layout_x[-1],
    fmodel.layout_y[-1],
    fmodel.floris.farm.turbine_map[-1].hub_height # 90m, the NREL 5MW HH.
)
"""

# This sets up the model, and now we can assign and run specific wind
# conditions.

# try to make plot: DAC turbines appear to have no impact on wake even at height = 6.5. Not sure if that's from the error 
# (I think from setting power = 0)

fmodel.calculate_wake()
# fmodel.calculate_horizontal_plane(6.5)

# try to plot
horizontal_plane = fmodel.calculate_horizontal_plane(x_resolution=200, y_resolution=100, height= 7, x_bounds = [-100, 1600], y_bounds = [-100,600])

fig, ax_list = plt.subplots(1, 1, figsize=(10, 8))

im = wakeviz.visualize_cut_plane(horizontal_plane, ax=ax_list, title= "Horizontal", clevels = 100)
fig.colorbar(im)
wakeviz.show_plots()
