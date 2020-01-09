import definition
import numpy as np
import pandas as pd
import data_prep as dp
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import random
import numpy as np

# wall_name = "Betonwand, Wärmedämmung mit Lattenrost, Verkleidung"
wall_name = "Holzblockwand, Aussenwärmedämmung, Verkleidung"
# wall_name = "Sichtbetonwand, Aussenwärmedämmung verputzt"
# wall_name = "Sichtbacksteinmauerwerk, Aussenwärmedämmung verputzt"

dirname = os.path.dirname(__file__)
wall_data_path = os.path.join(dirname, 'data/walls.xlsx')


window_area = 5.0
## Add window g-value here!
external_envelope_area=15.0  # m2 (south oriented)
room_depth= 7.0  # m
room_width= 5.0  # m
room_height= 3.0  # m
u_windows = 1.0  # W/m2K
ach_vent= 2.0  # Air changes per hour through ventilation [Air Changes Per Hour]
ach_infl= 1.5 # Air changes per hour through infiltration [Air Changes Per Hour]
ventilation_efficiency=0.4
max_cooling_energy_per_floor_area= [-np.inf, -np.inf, -np.inf]  # W/m2
max_heating_energy_per_floor_area= [np.inf, np.inf, np.inf]  # W/m2
pv_area = 2.5 #m2
pv_efficiency = 0.18
pv_tilt = 45
pv_azimuth = 0
lifetime = 30.0 ## Here this is only the lifetime of the building systems, not the building.
strom_mix = "d"

year_of_construction = 2020

grid_decarbonization_until = 2050  # Choose from 2050, 2060 and 2080
grid_decarbonization_type = 'linear'  # Choose from 'linear', exponential, quadratic, constant

u_walls = dp.extract_wall_data(wall_data_path, name=wall_name, type="U-value")
print("U value: " + str(u_walls))

## efficient configuration
# u_walls = 0.1
# u_windows = 0.5
# ventilation_efficiency = 0.75


## unefficient configuration
# u_walls = 0.6
# u_windows = 2.5
# ventilation_efficiency = 0.1


thermal_capacitance_per_floor_area = dp.extract_wall_data(wall_data_path, name=wall_name,
                                                              type ="Thermal capacitance [kJ/m2K]",
                                                              area=external_envelope_area-window_area)/\
                                         (room_width*room_depth)*1000  #factor 1000 coming from the conversion of kJ to J

# print("Thermal capacitance per floor area: ", thermal_capacitance_per_floor_area)



## Scenario preparation

# Weather data
weather_file_folder = r"C:\Users\walkerl\Documents\code\proof_of_concept\data\future_weather_data"
weather_scenarios = os.listdir(weather_file_folder)

# Electricity grid decarbonization
grid_decarbonization_until = [2050, 2060, 2080]  # Choose from 2050, 2060 and 2080
grid_decarbonization_types_l = ['linear', 'exponential', 'quadratic', 'constant'] # Choose from 'linear', exponential, quadratic, constant
grid_decarbonization_path = r'C:\Users\walkerl\Documents\code\proof_of_concept\data\future_decarbonization\Decarbonization sceanrios.xlsx'
from_year = 2020
to_year = from_year+lifetime

# Occupancy Schedule
# Needs to be added here


# PV technology development

# Price development etc.


# Carbon Tax
#--> will be added later when cost data is considered




### Choose the design case:

# random design case
weather_file = random.choice(weather_scenarios)
grid_decarbonization_year = random.choice(grid_decarbonization_until)
grid_decarbonization_type = random.choice(grid_decarbonization_types_l)

# calculate required system sizing

# store results


### Going through all scenarios approach:

# counter = 0
# for weather_file in weather_scenarios:
#     for grid_decarbonization_year in grid_decarbonization_until:
#         for grid_decarbonization_type in grid_decarbonization_types_l:
#             print(weather_file, grid_decarbonization_year, grid_decarbonization_type)
#             counter+=1
#             print(counter)


########### random reference scenario  ############
weather_file = random.choice(weather_scenarios)
grid_decarbonization_year = random.choice(grid_decarbonization_until)
grid_decarbonization_type = random.choice(grid_decarbonization_types_l)
weatherfile_path = os.path.join(weather_file_folder, weather_file)
decarb_grid_factors = dp.extract_decarbonization_factor(grid_decarbonization_path, grid_decarbonization_year,
                                                            grid_decarbonization_type, from_year, to_year)

print("Reference Scenario")
print(weather_file, grid_decarbonization_year, grid_decarbonization_type)
result_values = definition.run_simulation(external_envelope_area, window_area, room_width, room_depth, room_height,
                              thermal_capacitance_per_floor_area, u_walls, u_windows, ach_vent, ach_infl,
                              ventilation_efficiency, max_heating_energy_per_floor_area,
                              max_cooling_energy_per_floor_area, pv_area, pv_efficiency, pv_tilt, pv_azimuth,
                              lifetime, strom_mix, weatherfile_path, decarb_grid_factors)

required_heating_power_per_floor_area = result_values[6]
required_cooling_power_per_floor_area = result_values[7]

max_cooling_energy_per_floor_area = required_cooling_power_per_floor_area  # W/m2
max_heating_energy_per_floor_area = required_heating_power_per_floor_area  # W/m2


########### going through random scenarios   ###########
number_of_simulations = 5
total_emission_array = np.empty((number_of_simulations,3))
operational_emission_array = np.empty((number_of_simulations,3))
embodied_emission_array = np.empty((number_of_simulations,3))
discomfort_array = np.empty((number_of_simulations,3))


for i in range(number_of_simulations):
    weather_file = random.choice(weather_scenarios)
    grid_decarbonization_year = random.choice(grid_decarbonization_until)
    grid_decarbonization_type = random.choice(grid_decarbonization_types_l)

    print(weather_file, grid_decarbonization_year, grid_decarbonization_type)



    weatherfile_path = os.path.join(weather_file_folder,weather_file)

    decarb_grid_factors = dp.extract_decarbonization_factor(grid_decarbonization_path, grid_decarbonization_year,
                                                            grid_decarbonization_type, from_year, to_year)

    total_emissions, operational_emissions, embodied_emissions, u_windows, u_walls, thermal_capacitance_per_floor_area,\
    required_heating_energy_per_floor_area, required_cooling_energy_per_floor_area, indoor_temperature_list\
        = definition.run_simulation(external_envelope_area, window_area, room_width, room_depth, room_height,
                                        thermal_capacitance_per_floor_area, u_walls, u_windows, ach_vent, ach_infl,
                                        ventilation_efficiency, max_heating_energy_per_floor_area,
                                        max_cooling_energy_per_floor_area, pv_area, pv_efficiency, pv_tilt, pv_azimuth,
                                        lifetime, strom_mix, weatherfile_path, decarb_grid_factors)

    print(indoor_temperature_list)
    plt.plot(indoor_temperature_list)
    plt.title("indoor_temperature list")
    plt.show()
    total_emission_array[i,] = total_emissions
    operational_emission_array[i,] = operational_emissions
    embodied_emission_array[i,] = embodied_emissions
    # print(emission_array)

    print("Discomfort hours")
    print(definition.comfort_assessment(indoor_temperature_list, [20,26], 'hod')) ## make sure to have these values lower/higher than the heating set point

############  Ploting results ###################

###### line plots ######

plt.plot([1,2,3], total_emission_array.T)
plt.title("Normalized annual emissions per Scenario")
plt.ylabel("normalized emissions kgCO2eq/(m2a)")
tix = ['electric', 'ashp', 'gshp']
plt.xticks([1,2,3], tix)

plt.show()


###### Box plots ######

# results = np.concatenate([total_emission_array, operational_emission_array, embodied_emission_array]) ## hier weitermachen
# print(results)
#
# fig, ax1 = plt.subplots(figsize=(6,6))
# fig.canvas.set_window_title('A Boxplot Example')
# fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
# bp = ax1.boxplot(results, notch=0, sym='+', vert=1, whis=1.5)
#
# plt.setp(bp['boxes'], color='black')
# plt.setp(bp['whiskers'], color='black')
# plt.setp(bp['fliers'], color='red', marker='+')
# ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
#                alpha=0.5)
#
# plt.boxplot(total_emission_array)
## plt.boxplot(operational_emission_array)
## plt.boxplot(embodied_emission_array, patch_artist=True)
# plt.title( "Normalized Emissions with different climate scenarios")
# plt.ylabel("Annual Emissions CO2eq/m2")
# plt.legend(["1 pure electric", "2 ASHP", "3 GSHP"])
## plt.savefig(r"C:/Users/walkerl/polybox/phd/proof_of_concept/plots/19_10_01/low_area/" + str(xlabel) + ".png")
# plt.show()

data = pd.DataFrame(data = (window_area, external_envelope_area, room_depth, room_width, room_height, u_windows, u_walls,
                    ach_vent,ach_infl, ventilation_efficiency, max_cooling_energy_per_floor_area,
                    max_heating_energy_per_floor_area, pv_area, pv_efficiency, pv_tilt, pv_azimuth, lifetime, strom_mix,
                    thermal_capacitance_per_floor_area))




