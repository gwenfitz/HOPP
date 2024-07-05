from hopp.simulation import HoppInterface
from hopp.tools.dispatch.plot_tools import (plot_battery_output, plot_battery_dispatch_error, plot_generation_profile)

hi = HoppInterface("")
hi.simulate(project_life = 10)

hybrid_plant = hi.system

annual_energies = hybrid_plant.annual_energies
npvs = hybrid_plant.net_present_values
cf = hybrid_plant.capacity_factors
wind_installed_cost = hybrid_plant.wind.total_installed_cost


plot_battery_dispatch_error(hybrid_plant)
plot_battery_output(hybrid_plant)

