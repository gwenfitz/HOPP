import numpy as np

from hopp.utilities import load_yaml
from hopp.simulation.technologies.sites import SiteInfo
from hopp.simulation import HoppInterface
import floris.tools.visualization as wakeviz
from hopp.tools.dispatch.plot_tools import (plot_battery_output, plot_battery_dispatch_error, plot_generation_profile)
import matplotlib.pyplot as plt
import pandas as pd

import greenheart.simulation.technologies.dac.direct_air_capture as dac

def runsimulation(showplots = False):
    
    
    #load floris config
    # floris_config = load_yaml("./Inputs/gch_dacdisk_turbine.yaml")
    floris_config = load_yaml("HOPP/DAC/Inputs/gch_dacdisk_turbine.yaml")

    # load base hopp config
    hopp_config = load_yaml("HOPP/DAC/Inputs/dac_hopp.yaml")

    from floris.tools import FlorisInterface
    fmodel = FlorisInterface("HOPP/DAC/Inputs/gch_dac_floris_for_wind.yaml")
    met_mast_option = 0

    # load hopp site
    hopp_site = SiteInfo(**hopp_config["site"])
    wind_data = hopp_site.wind_resource._data["data"]
    wind_speed = [W[2] for W in wind_data]        # at 10m height, could use equation to find at diff heights.
    wind_dirs = [W[3] for W in wind_data] 

    print('wind speed')
    wind_speed = wind_speed[700:724]

    print('wind dir')
    wind_dirs = wind_dirs[700:724]

    turb = floris_config['farm']['turbine_type'][1]  # Wind turbine model

    df = pd.read_csv('HOPP/DAC/Inputs/turbine_coordinates_southplainsii.csv')
    turbs_layout_x = df['x_coords'].to_list()
    turbs_layout_y = df['y_coords'].to_list()
    turbs_all = [turb] * len(turbs_layout_x) # List of turbines

    print('test 1')

    # Join the layouts of DACs and turbines, as well as their dictionary lists
    # layout_x = dacs_layout_x.extend(turbs_layout_x)
    layout_x = np.array(turbs_layout_x)
    layout_y = np.array(turbs_layout_y)
    type_defs = turbs_all

    wind_speed = np.array(wind_speed) # 
    wind_dirs = np.array(wind_dirs)

    print('test 2')
    fmodel.reinitialize(layout_x=layout_x, layout_y=layout_y, turbine_type=type_defs, reference_wind_height=10)
    print('test 3')
    fmodel.reinitialize(wind_speeds = wind_speed)
    print('test 4')
    fmodel.reinitialize(wind_directions= wind_dirs) 


    print('test 5')
    # u_at_points = fmodel.sample_flow_at_points([2860, 2900, 3000, 7442] , [9276, 9276, 9276, 7317], [10,10,10,10])
    # print('the velocity is:')
    # print(u_at_points)

    import greenheart.simulation.technologies.dac.direct_air_capture as dac

    for x in range(51):
        random1 = np.random.random(1)[0] 
        random2 = np.random.random(1)[0]
        x_coord = np.multiply(13000,random1)
        y_coord = np.multiply(10000,random2)
        wind_new = fmodel.sample_flow_at_points([x_coord], [y_coord], [10])
        wind_new = wind_new[0,0:24,0]
        co2, _ = dac.driver(wind_new,11630)
        co2 = np.sum(co2)
        print(f'co2 output in trial{x} = {co2}')


    """"
    wind_loc1 = fmodel.sample_flow_at_points([2860], [9276], [10])
    wind_loc2 = fmodel.sample_flow_at_points([2900], [9276], [10])
    wind_loc3 = fmodel.sample_flow_at_points([3000], [9276], [10])
    wind_loc4 = fmodel.sample_flow_at_points([7442], [7317], [10])

    wind_loc1 = wind_loc1[0,0:24,0]
    wind_loc2 = wind_loc2[0,0:24,0]
    wind_loc3 = wind_loc3[0,0:24,0]
    wind_loc4 = wind_loc4[0,0:24,0]
    
    co2_standard, _ = dac.driver(wind_speed,11630) 
    co2_standard = np.sum(co2_standard)
    print('co2 standard = ', co2_standard)

    co2_1, _ = dac.driver(wind_loc1,11630) 
    co2_1 = np.sum(co2_1)
    print('co2 1 =', co2_1)

    co2_2, _ = dac.driver(wind_loc2,11630) 
    co2_2 = np.sum(co2_2)
    print('co2 2 =', co2_2)

    co2_3, _ = dac.driver(wind_loc3,11630) 
    co2_3 = np.sum(co2_3)
    print('co2 3 =', co2_3)

    co2_4, _ = dac.driver(wind_loc4,11630) 
    co2_4 = np.sum(co2_4)
    print('co2 4 = ', co2_4)

    """




if __name__ == "__main__":
    runsimulation(showplots= True)