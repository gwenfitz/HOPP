import numpy as np

from hopp.utilities import load_yaml
from hopp.simulation.technologies.sites import SiteInfo
from hopp.simulation import HoppInterface

import greenheart.simulation.technologies.dac.direct_air_capture as dac

def runsimulation(showplots == false)
#load floris config
floris_config = load_yaml("./DAC/Inputs/gch_dacdisk_turbine.yaml")

# load base hopp config
hopp_config = load_yaml("./DAC/Inputs/dac_hopp.yaml")

# load hopp site
hopp_site = SiteInfo(**hopp_config["site"])
wind_data = hopp_site.wind_resource._data["data"]
wind_speed = [W[2] for W in wind_data]        # at 10m height, could use equation to find at diff heights.


dac_disk = floris_config['farm']['turbine_type'][0] # Single disk of DAC stack
turb = floris_config['farm']['turbine_type'][1]  # Wind turbine model

# print(dac_disk)

# Now, set up the x, y locations for each of the DACs (two rows of four DACS)
dacs_layout_x = np.array([0, 500, 1000, 1500, 0, 500, 1000, 1500])
dacs_layout_y = np.array([0, 0, 0, 0, 500, 500, 500, 500])
n_dacs = len(dacs_layout_x)

# Generate a list of the "hub heights" of the DAC disks in a single DAC
dac_heights = [2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5]

# # Generate a list of turbine definitions that specify a single DAC
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

# Check it worked... expect 2, 2.5, 4.5, 2 for the hub heights,
# at the (0,0) DAC and then the (500,0) DAC
print("Some DAC locations before assignment (x, y, height):")
for i in [0, 1, 5, 6]:
    print(dacs_layout_x[i], dacs_layout_y[i], dacs_all[i]["hub_height"])

# Now, we'll create the layout and list of actual wind turbines
turbs_layout_x = [2000, 2000, 4000, 4000]
turbs_layout_y = [0, 2000, 0, 2000]
turbs_all = [turb] * len(turbs_layout_x) # List of 4 turbines

# Join the layouts of DACs and turbines, as well as their dictionary lists
layout_x = dacs_layout_x + turbs_layout_x
layout_y = dacs_layout_y + turbs_layout_y
type_defs = dacs_all + turbs_all

# update floris config definitions
floris_config["farm"]["layout_x"] = layout_x
floris_config["farm"]["layout_y"] = layout_y
floris_config["farm"]["turbine_type"] = type_defs

# load floris config into hopp config
hopp_config["technologies"]["wind"]["floris_config"] = floris_config

#run DAC
co2, _, power = dac.driver(wind_speed) # 

## WIND SPEED: 8760 list of wind speed at 10m. Could make a 2D array or repeatedly call
# change wind profile at each module height down from 10 meters using equation
# have driver take in wind speed series at 10m, convert internally to array of wind speeds at each module height. 
# give hourly wind time series, get CO2 produced, power required
# add up for each stack of DAC
# within driver multiply by theoretical number of DAC modules/units?? Maybe another input to driver
# return array or pandas data frame of CO2 captured at each height over time series, and return 1D list of CO2 from 
# that stack for the hour
# From driver return module CO2 produced (array), stack CO2 (1D list), total DAC farm CO2 produced (stack * number of DAC units)


# # battery requirements
dac_power_requirements = [x / 1000 for x in power] #[MW]
hopp_config["site"]["desired_schedule"] = dac_power_requirements

# load hopp interface
hi = HoppInterface(hopp_config)
print(hi.system.site.wind_resource)

# run hopp simulation
hi.simulate(project_life=20)

if showplots:
    # show plot code

if name == '__main__'
    run_simulation(showplots= true)



hopp_results = {
    "hopp_interface": hi,
    "hybrid_plant": hi.system,
    "combined_hybrid_power_production_hopp": \
        hi.system.grid._system_model.Outputs.system_pre_interconnect_kwac[0:8760],
    "combined_hybrid_curtailment_hopp": hi.system.grid.generation_curtailed,
    "energy_shortfall_hopp": hi.system.grid.missed_load,
    "annual_energies": hi.system.annual_energies,
}