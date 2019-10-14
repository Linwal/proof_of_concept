import definition
import numpy as np
import pandas as pd
import data_prep as dp
import os
import matplotlib.pyplot as plt

# wall_name = "Betonwand, Wärmedämmung mit Lattenrost, Verkleidung"
wall_name = "Holzblockwand, Aussenwärmedämmung, Verkleidung"
# wall_name = "Sichtbetonwand, Aussenwärmedämmung verputzt"
# wall_name = "Sichtbacksteinmauerwerk, Aussenwärmedämmung verputzt"

dirname = os.path.dirname(__file__)
wall_data_path = os.path.join(dirname, 'data/walls.xlsx')


window_area = 10.0
## Add window g-value here!
external_envelope_area=15.0  # m2 (south oriented)
room_depth=7.0  # m
room_width=5.0  # m
room_height=3.0  # m
u_windows = 1.0  # W/m2K
ach_vent= 2.0  # Air changes per hour through ventilation [Air Changes Per Hour]
ach_infl= 1.5 # Air changes per hour through infiltration [Air Changes Per Hour]
ventilation_efficiency=0.4
max_cooling_energy_per_floor_area=-np.inf
max_heating_energy_per_floor_area=np.inf
pv_area = 2.5 #m2
pv_efficiency = 0.18
pv_tilt = 45
pv_azimuth = 0
lifetime = 25.00
strom_mix = "d"

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

print("Thermal capacitance per floor area: ", thermal_capacitance_per_floor_area)




# data_list = [0.01,0.5, 1., 2, 3.5, 8, 10, 50, 100, 500, 1000] #pv area
# data_list = [15,20,25,30,35,40,45] #lifetime
# data_list = [0.1, 2, 6, 8, 12, 15]  # window area
# data_list = [0.15, 0.18, 0.20, 0.22, .24, 0.26] # PV efficiency
# data_list = [0,10,20,30,40,50,60,70,80,90] # PV tilt
# data_list = [-90, -70, -50, -30, -10, 0, 10, 30, 50, 70, 90]
data_list = [0.1, 0.2, 0.4, 0.5, 0.6, 0.8, 0.9]
# data_list = [1]

emission_array = np.empty((len(data_list),3))


for i in range(len(data_list)) :
    # pv_area = data_list[i]
    # lifetime = data_list[i]
    # window_area = data_list[i]
    # pv_efficiency = data_list[i]
    # pv_tilt = data_list[i]
    # pv_azimuth = data_list[i]
    ventilation_efficiency = data_list[i]
    total_emissions, operational_emissions, embodied_emissions, u_windows, u_walls, thermal_capacitance_per_floor_area\
        = definition.run_simulation(external_envelope_area, window_area, room_width, room_depth, room_height,
                                     thermal_capacitance_per_floor_area, u_walls, u_windows, ach_vent, ach_infl, ventilation_efficiency,
                                     max_heating_energy_per_floor_area, max_cooling_energy_per_floor_area,
                                     pv_area, pv_efficiency, pv_tilt, pv_azimuth, lifetime, strom_mix)

    emission_array[i] = total_emissions

emission_array
print(emission_array)

xlabel = "PV efficiency"

ylabel = "Annual emissions (kgCO2eq/a)"
plt.plot(data_list, emission_array)
plt.title( "emissions vs " + str(xlabel))
plt.ylabel(ylabel)
plt.xlabel(xlabel)
plt.legend(["pure electric", "ASHP", "GSHP"])
# plt.savefig(r"C:/Users/walkerl/polybox/phd/proof_of_concept/plots/19_10_01/low_area/" + str(xlabel) + ".png")
plt.show()

data = pd.DataFrame(data = (window_area, external_envelope_area, room_depth, room_width, room_height, u_windows, u_walls,
                    ach_vent,ach_infl, ventilation_efficiency, max_cooling_energy_per_floor_area,
                    max_heating_energy_per_floor_area, pv_area, pv_efficiency, pv_tilt, pv_azimuth, lifetime, strom_mix,
                    thermal_capacitance_per_floor_area))
print(data)
