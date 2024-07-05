
from hopp.simulation import HoppInterface
import numpy as np
import matplotlib.pyplot as plt

"""""
model_name: floris
timestep: [0,8760]
floris_config: inputs/floris/gch.yaml

hi = HoppInterface("inputs/gch.yaml")
"""

from floris.tools import FlorisInterface
import floris.tools.visualization as wakeviz

# Load an arbitrary FLORIS input file, which we'll then modify. Assume that 
# a single DAC disc is specified, but we'll set the hub height later
fmodel = FlorisInterface("examples/inputs/floris/gch.yaml")

turb_def = fmodel.floris.farm.turbine_definitions[0] 
# This is a dictionary form of the turbine yaml that was specified in the gch.yaml file
# (the NREL-5MW turbine in this case, but will be your single DAC disc)

# Now, set up the x, y locations for each of the turbines (DACs)
# Two rows of four turbines (DACs)
layout_x = np.array([0, 500, 1000, 1500, 0, 500, 1000, 1500])
layout_y = np.array([0, 0, 0, 0, 500, 500, 500, 500])
n_dacs = len(layout_x)

dac_heights = [2, 2.5, 3, 3.5, 4, 4.5] # For example, these will be the "hub heights" 
# of the discs representing a single DAC

# Generate a list of turbine definitions that specify a single DAC
dac_turbs = []
for i, hub_height in enumerate(dac_heights):
    turb_def_i = turb_def.copy()
    turb_def_i["hub_height"] = hub_height
    turb_def_i["turbine_type"] = "NREL-5MW-HH"+str(hub_height) # Need to rename to avoid a bug
    dac_turbs.append(turb_def_i)

# Tile this list to match the number of DACs
turbs_all = dac_turbs * n_dacs

# We'll need to extend the  (x,y) layouts to match the number of hub heights
layout_x = np.repeat(layout_x, len(dac_heights))
layout_y = np.repeat(layout_y, len(dac_heights))

# Check it worked... expect 2, 2.5, 4.5, 2 for the hub heights, at the (0,0) turbine
# and then the (500,0) turbine
print("Locations before assignment:")
for i in [0, 1, 5, 6]:
    print(layout_x[i], layout_y[i], turbs_all[i]["hub_height"])

# Assign and check again
fmodel.reinitialize(layout_x=layout_x, layout_y=layout_y, turbine_type=turbs_all)

print("\n\nLocations after assignment:")
for i in [0, 1, 5, 6]:
    print(
        fmodel.layout_x[i],
        fmodel.layout_y[i],
        fmodel.floris.farm.turbine_map[i].hub_height,
    )

# This sets up the model, and now we can assign and run specific wind conditions.

# fmodel.reinitialize(wind_speeds= 12)
fmodel.reinitialize(reference_wind_height = 5)

horizontal_plane = fmodel.calculate_horizontal_plane(
    x_resolution=200,
    y_resolution=100,
    height=2.5
)

fig, ax_list = plt.subplots(1, 1, figsize=(10, 8))

wakeviz.visualize_cut_plane(horizontal_plane, ax=ax_list, title="Horizontal")

wakeviz.show_plots()