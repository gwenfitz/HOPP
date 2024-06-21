
# Input = array with hourly timescale of wind speeds, m/s (assumes wind speed is the average over the hour)
# This function uses the hourly wind speed data to find CO2 uptake (in tons of CO2 over that hour). 
# Then, the power consumption over the hour is calculated based on the CO2 uptake using the conversion 7.2 GJ
# or 2000 kWh per ton of CO2 adsorbed. 

# This is a little janky because we have set the adsorption/ desorption times to 54 / 6  minutes 
# regardless of how much CO2 is adsorbed during that hour. The total energy requirement should be about 
# equal to the energy of the desorption stage. I'm not sure if a "6 minute desorption time" would 
# require the same amount of energy no matter how much CO2 is being desorbed or not.
# Each unit will be made of one base and then 6 modules, stacked on top of eachother. Each module is 
# 1 meter tall. Theoretically, the models will have staggered adsorption/ desorption stages throughout the 
# hour. Using 6 minutes as the desorption time and 6 modules, this means that every hour there are 36 minutes
# where one of the modules is desorbing CO2 while the other 5 are each adsorbing. The remaining 24 minutes, 
# all modules are adsorbing CO2 (no/ very low energy requirement). 
# However, I propose that we assume each unit requires constant power throughout the hour for easier 
# calculations, especially with the batteries/ intermittent wind power.

import numpy as np
from scipy import interpolate

def driver():

    hourly_CO2_prod, total = calc_CO2_prod(hourly_data)

    hourly_energy_consumed = energyconsumptioncalc(hourly_CO2_prod)

    return hourly_CO2_prod, total, hourly_energy_consumed


# make up series of hourly wind speeds for testing purposes 
hourly_data = np.array([1.2,3.4,2.6,1.3,1.8,2.7,3.6,5.8,6.9,5.6])

# find tons of CO2 produced over that hour (by one module) at the defined wind speed
def calc_CO2_prod(hourly_data):

    # experimentally determined data (from Realff et al.)

    # wind speeds (m/s)
    set_wind_speeds = np.array([0.01, 0.3, 1, 3, 5, 7])

    # CO2 adsorption (moles CO2 adsorbed per kg sorbent in 54 minutes)
        # Note: desorption time set to 6 minutes (assume complete adsorption). No CO2 is adsorbed during 
        # desoprtion stage, so the amount of CO2 adsorbed in 54 minutes represents the hourly total. 
    set_molar_CO2 = np.array([0.04, 0.22, 0.60, 0.90, 0.935, 0.96])

    # molar mass of CO2: kg/ mole
    mCO2 = 0.044

    set_kg_CO2 = set_molar_CO2 * mCO2

    CO2_prod = []

    # at every reported wind speed, use an interpolation of the two surrounding data points to find the 
    # hourly uptake of CO2 (in kg CO2 per kg sorbent, ie. per one module)
    for speed in hourly_data:
        if 0.01<= speed <= 0.3:
           f = interpolate.interp1d(set_wind_speeds[0:2], set_kg_CO2[0:2])
           CO2_prod.append(f(speed))
        elif 0.3 < speed <= 1:
            f = interpolate.interp1d(set_wind_speeds[1:3], set_kg_CO2[1:3])
            CO2_prod.append(f(speed))
        elif 1 < speed <= 3:
            f = interpolate.interp1d(set_wind_speeds[2:4], set_kg_CO2[2:4])
            CO2_prod.append(f(speed))
        elif 3 < speed <= 5:
            f = interpolate.interp1d(set_wind_speeds[3:5], set_kg_CO2[3:5])
            CO2_prod.append(f(speed))
        elif 5 < speed <= 7:
            f = interpolate.interp1d(set_wind_speeds[4:6], set_kg_CO2[4:6])
            CO2_prod.append(f(speed))
        # if wind speed is greater than 7 m/s, assume that CO2 uptake is the same rate as wind speed at 7 m/s
        elif speed >= 7:
            CO2_prod.append(set_kg_CO2[5])

    # convert to numpy array
    hourly_CO2_prod = np.array(CO2_prod)

    # convert CO2 produced from kg to tons
    hourly_CO2_prod = (hourly_CO2_prod)/907.185 
    
    # sum over all hours
    total = np.sum(hourly_CO2_prod)

    return hourly_CO2_prod, total

# Input = amount of CO2 adsorbed over an hour (tons). Output = energy consumed during that hour
def energyconsumptioncalc(hourly_CO2_production):

    # calculate energy consumed in kWh over that hour
    hourly_energy_consumed = 2000*hourly_CO2_production
    return hourly_energy_consumed

# call main function and then print all of the outputs.

hourly_CO2_prod, total, hourly_energy_consumed = driver()

print(f"CO2 uptake per hour in timescale (in tons CO2): {hourly_CO2_prod}",end = "\n\n")
print(f"total CO2 uptake over all hours: {total} tons CO2", end = "\n\n")
print(f"the energy requirement (in kWh) each hour is: {hourly_energy_consumed}", end = "\n\n")
