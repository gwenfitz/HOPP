# Input = 1D array with hourly timescale of wind speeds, m/s (assumes wind speed is the average over the hour)

import numpy as np

def driver(windspeed, numDACs):

    windspeed = np.array(windspeed)
    windspeeds = windspeed
    # Adding row to numpy array
    heights = [3,5,7,9,11,13]
    for _ in heights[0:-1]:
        windspeeds = np.vstack ((windspeeds, windspeed))

    k = 0    
    for height in heights:
        height_var = (height/10)**0.143
        # v = v_ref * (z/z_ref)^0.143
        windspeeds[k,:] = np.multiply(windspeeds[k,:],height_var)
        k = k+1

    windspeeds[windspeeds == 0] = 0.1

    # CO2 produced per DAC module (ie. 1 kg sorbent)
    CO2_permodule = CO2_produced(windspeeds)

    # CO2 produced per hour per DAC unit (ie. 1 stack of six modules)
    CO2_unit = np.sum(CO2_permodule, axis = 0)

    # CO2 produced per hour per farm with numDACs DAC units (in moles CO2)
    CO2_total = np.multiply(numDACs,CO2_unit)

    # tons of CO2 collected per hour
    # mole CO2 to US ton conversion: 0.044 kg/mole, 907.185 kg/ton
    convert = 0.044 / 907.185
    CO2_total = np.multiply(CO2_total,convert)

    # power input required per hour (kWh) = 0.10479 kWh per desorption per kg sorbent
    kg_sorbent = np.multiply(numDACs, 24)
    power_per_hour = np.multiply(0.10479,kg_sorbent)

    print(power_per_hour)
    power_total = np.multiply(np.ones(np.shape(CO2_total)), power_per_hour)


    return CO2_total, power_total

def CO2_produced(x):
    # find CO2 uptake by 1 kg sorbent in one hour (specifically 54 minutes but with 6 minute desorption) at a wind speed x.
    # the wind speed x is defined at the midpoint height of the individual DAC module. 

    y = np.multiply(4, np.multiply(0.1503,np.log(x)) + 0.6377)
    
    return y

    """""
    # data from Lively et al. 
    wind_speed = [0.1, 0.3, 1, 3, 5, 7]
    # CO2 uptake in 54 minutes (moles CO2 / kg sorbent)
    CO2_uptake = [0.04202532,0.24860759, 0.61721519, 0.86025316,0.92506329,0.95949367]
    # molar mass of CO2: kg/ mole
    mCO2 = 0.044
    # convert moles CO2 to kg CO2
    CO2_uptake = np.multiply(mCO2, CO2_uptake)
    # convert kg CO2 to US tons CO2
    CO2_uptake = np.multiply(0.00110231, CO2_uptake)

    tck = interpolate.splrep(wind_speed, CO2_uptake)
    return interpolate.splev(x, tck)
    """

# windarray = [1,4.3,2.8,7,6.5,5.2,8]
# num_dac = 20
# CO2_total, power_total = driver(windarray,num_dac)
# print(CO2_total)
# print(power_total)
