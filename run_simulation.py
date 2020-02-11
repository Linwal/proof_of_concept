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


# Zurich = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator\auxiliary\Zurich-Kloten_2013.epw")
# Recife = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\BRA_Recife.828990_IWEC.epw")
# SaoPaolo = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\BRA_Sao.Paulo-Congonhas.837800_SWERA.epw")
# Vancouver = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\CAN_BC_Vancouver.718920_CWEC.epw")
# PuntaArenas = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\CHL_Punta.Arenas.859340_IWEC.epw")
# Stuttgart = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\DEU_Stuttgart.107380_IWEC.epw")
# Copenhagen = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\DNK_Copenhagen.061800_IWEC.epw")
# Algier = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\DZA_Algiers.603900_IWEC.epw")
# Barcelona = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\ESP_Barcelona.081810_IWEC.epw")
# London = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\GBR_London.Gatwick.037760_IWEC.epw")
# Milano = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\ITA_Milano-Linate.160800_IGDG.epw")
# Rome =Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\ITA_Roma-Ciampino.162390_IGDG.epw")
# Kiruna = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\SWE_Kiruna.020440_IWEC.epw")
# Ostersund = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\SWE_Ostersund.Froson.022260_IWEC.epw")
# LongBeach_LA = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\USA_CA_Long.Beach-Daugherty.Field.722970_TMY3.epw")
# DesMoines = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\USA_IA_Des.Moines.Intl.AP.725460_TMY3.epw")
# Chicago = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\proof_of_concept\data\USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw")


dirname = os.path.dirname(__file__)
wall_data_path = os.path.join(dirname, 'data/walls.xlsx')
weatherfile_path = r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator\auxiliary\Zurich-Kloten_2013.epw"



## Bauteile / Construction parts
window_area = 526
## Add window g-value here!
external_envelope_area=1650  # m2 (south oriented)
room_depth=22.5  # m
room_width=22.5  # m
room_height=4.5*3  # m
u_windows = 0.6 # W/m2K
ach_vent= 0.7*0.4  # Air changes per hour through ventilation [Air Changes Per Hour]
ach_infl= 0.0 # Air changes per hour through infiltration [Air Changes Per Hour] must be very low for good buildings.
ventilation_efficiency=0.
max_cooling_energy_per_floor_area=[-np.inf, -np.inf, -np.inf]
max_heating_energy_per_floor_area=[np.inf, np.inf, np.inf]

## Domestic hot water
annual_dhw_p_person = 582000  # Wh/(p*a) SIA2024  für Office 36400 für MFH wären es 582000 Wh/(p*a) aus hard code rausnehmen
dhw_supply_temperature = 60  # degC

## SIA use type
use_type = 1  # only goes into electrical appliances according to SIA (1=residential, 3= office)


pv_area = 360 #m2
pv_efficiency = 0.18
pv_tilt = 5
pv_azimuth = 0
lifetime = 30.0 ## Here this is only the lifetime of the building systems, not the building.
strom_mix = "d"

grid_decarbonization_until = 2050  # Choose from 2050, 2060 and 2080
grid_decarbonization_type = 'linear'  # Choose from 'linear', exponential, quadratic, constant


###
# u_walls = dp.extract_wall_data(wall_data_path, name=wall_name, type="U-value")
# print("U value: " + str(u_walls))
u_walls = 0.08




grid_decarbonization_year = 2060  # Choose from 2050, 2060 and 2080
grid_decarbonization_types = 'linear'  # Choose from 'linear', exponential, quadratic, constant
grid_decarbonization_path = r'C:\Users\walkerl\Documents\code\proof_of_concept\data\future_decarbonization\Decarbonization sceanrios.xlsx'
from_year = 2020
to_year = from_year+lifetime
decarb_grid_factors = dp.extract_decarbonization_factor(grid_decarbonization_path, grid_decarbonization_year,
                                                            grid_decarbonization_type, from_year, to_year)


thermal_capacitance_per_floor_area = dp.extract_wall_data(wall_data_path, name=wall_name,
                                                              type ="Thermal capacitance [kJ/m2K]",
                                                              area=external_envelope_area-window_area)/\
                                         (room_width*room_depth)*1000  #factor 1000 coming from the conversion of kJ to J

print("Thermal capacitance per floor area: ", thermal_capacitance_per_floor_area)

heating_temp = 20.0
cooling_temp = 26.0





normalized_total_emissions, normalized_annual_operational_emissions, normalized_annual_embodied_emissions, \
u_windows, u_walls, thermal_capacitance_per_floor_area, max_required_heating_per_floor_area, \
max_required_cooling_per_floor_area, indoor_temperature_list\
    = definition.run_rc_simulation(external_envelope_area=external_envelope_area,
                                window_area=window_area,
                                room_width=room_width,
                                room_depth =room_depth,
                                room_height=room_height,
                                thermal_capacitance_per_floor_area=thermal_capacitance_per_floor_area,
                                u_walls=u_walls,
                                u_windows=u_windows,
                                ach_vent=ach_vent,
                                ach_infl=ach_infl,
                                ventilation_efficiency=ventilation_efficiency,
                                max_heating_energy_per_floor_area=max_heating_energy_per_floor_area,
                                max_cooling_energy_per_floor_area=max_cooling_energy_per_floor_area,
                                pv_area=pv_area,
                                pv_efficiency=pv_efficiency,
                                pv_tilt=pv_tilt,
                                pv_azimuth=pv_azimuth,
                                lifetime=lifetime,
                                strom_mix=strom_mix,
                                weatherfile_path=weatherfile_path,
                                grid_decarbonization_factors=decarb_grid_factors,
                                t_set_heating=heating_temp,
                                t_set_cooling=cooling_temp,
                                annual_dhw_p_person=annual_dhw_p_person,
                                dhw_supply_temperature=dhw_supply_temperature,
                                use_type=use_type)


print(normalized_annual_operational_emissions)


