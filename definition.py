import sys
sys.path.insert(1, r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator")
from building_physics import Building
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import supply_system
import emission_system
from radiation import Location
from radiation import Window





Zurich = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator\auxiliary\Zurich-Kloten_2013.epw")


window_area = 4.0
external_envelope_area=15.0
room_depth=7.0
room_width=5.0
room_height=3.0
lighting_load=11.7
lighting_control = 300.0
lighting_utilisation_factor=0.45
lighting_maintenance_factor=0.9
u_walls = 0.15
u_windows = 0.9
ach_vent=1.5
ach_infl=0.5
ventilation_efficiency=0.6
thermal_capacitance_per_floor_area = 165000
t_set_heating = 20.0
t_set_cooling = 26.0
max_cooling_energy_per_floor_area=0
max_heating_energy_per_floor_area=np.inf



Office_1X = Building(window_area=window_area,
                external_envelope_area=external_envelope_area,
                room_depth=room_depth,
                room_width=room_width,
                room_height=room_height,
                lighting_load=lighting_load,
                lighting_control = lighting_control,
                lighting_utilisation_factor=lighting_utilisation_factor,
                lighting_maintenance_factor=lighting_maintenance_factor,
                u_walls = u_walls,
                u_windows = u_windows,
                ach_vent=ach_vent,
                ach_infl=ach_infl,
                ventilation_efficiency=ventilation_efficiency,
                thermal_capacitance_per_floor_area = thermal_capacitance_per_floor_area,
                t_set_heating = t_set_heating,
                t_set_cooling = t_set_cooling,
                max_cooling_energy_per_floor_area=max_cooling_energy_per_floor_area,
                max_heating_energy_per_floor_area=max_heating_energy_per_floor_area,
                heating_supply_system=supply_system.ElectricHeating,
                cooling_supply_system=supply_system.HeatPumpAir,
                heating_emission_system=emission_system.FloorHeating,
                cooling_emission_system=emission_system.AirConditioning,)

Office_2X = Building(window_area=window_area,
                external_envelope_area=external_envelope_area,
                room_depth=room_depth,
                room_width=room_width,
                room_height=room_height,
                lighting_load=lighting_load,
                lighting_control = lighting_control,
                lighting_utilisation_factor=lighting_utilisation_factor,
                lighting_maintenance_factor=lighting_maintenance_factor,
                u_walls = u_walls,
                u_windows = u_windows,
                ach_vent=ach_vent,
                ach_infl=ach_infl,
                ventilation_efficiency=ventilation_efficiency,
                thermal_capacitance_per_floor_area = thermal_capacitance_per_floor_area,
                t_set_heating = t_set_heating,
                t_set_cooling = t_set_cooling,
                max_cooling_energy_per_floor_area=max_cooling_energy_per_floor_area,
                max_heating_energy_per_floor_area=max_heating_energy_per_floor_area,
                heating_supply_system=supply_system.HeatPumpAir,
                cooling_supply_system=supply_system.HeatPumpAir,
                heating_emission_system=emission_system.FloorHeating,
                cooling_emission_system=emission_system.AirConditioning,)

Office_32 = Building(window_area=window_area,
                external_envelope_area=external_envelope_area,
                room_depth=room_depth,
                room_width=room_width,
                room_height=room_height,
                lighting_load=lighting_load,
                lighting_control = lighting_control,
                lighting_utilisation_factor=lighting_utilisation_factor,
                lighting_maintenance_factor=lighting_maintenance_factor,
                u_walls = u_walls,
                u_windows = u_windows,
                ach_vent=ach_vent,
                ach_infl=ach_infl,
                ventilation_efficiency=ventilation_efficiency,
                thermal_capacitance_per_floor_area = thermal_capacitance_per_floor_area,
                t_set_heating = t_set_heating,
                t_set_cooling = t_set_cooling,
                max_cooling_energy_per_floor_area=max_cooling_energy_per_floor_area,
                max_heating_energy_per_floor_area=max_heating_energy_per_floor_area,
                heating_supply_system=supply_system.HeatPumpWater,
                cooling_supply_system=supply_system.HeatPumpAir,
                heating_emission_system=emission_system.FloorHeating,
                cooling_emission_system=emission_system.AirConditioning,)


### emission factors according to empa_Alice Chevrier Semester Project in g/Wh

# aproximated values from the graph
grid_emission_factor = {"jan":.110, "feb":.130, "mar":.120, "apr":.85, "may":.40, "jun":.45, "jul":.55, "aug":.85, "sep":.110, "oct":.140, "nov":.130, "dec":.130}

##
# jan:  0 - 743
# feb:  744 - 1415
# mar:  1440 - 2159
# apr:  2160 - 2906
# may:  2907 - 3623
# jun:  3624 - 4343
# jul:  4344 - 5087
# aug:  5088 - 5831
# sep:  5832 - 6551
# oct:  6552 - 7295
# nov:  7296 - 8015
# dec:  8016 - 8759

hourly_emission_factors = np.concatenate([
    np.repeat(grid_emission_factor["jan"], 744),
    np.repeat(grid_emission_factor["feb"], 672),
    np.repeat(grid_emission_factor["mar"], 744),
    np.repeat(grid_emission_factor["apr"], 720),
    np.repeat(grid_emission_factor["may"], 744),
    np.repeat(grid_emission_factor["jun"], 720),
    np.repeat(grid_emission_factor["jul"], 744),
    np.repeat(grid_emission_factor["aug"], 744),
    np.repeat(grid_emission_factor["sep"], 720),
    np.repeat(grid_emission_factor["oct"], 744),
    np.repeat(grid_emission_factor["nov"], 720),
    np.repeat(grid_emission_factor["dec"], 744)
    ])


SouthWindow = Window(azimuth_tilt=0, alititude_tilt = 90, glass_solar_transmittance=0.2,
                     glass_light_transmittance=0.5, area = 4)


## Define occupancy
occupancyProfile=pd.read_csv(r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator\auxiliary\schedules_el_OFFICE.csv")

## Define constants

gain_per_person = 100 # W per sqm
appliance_gains= 14 #W per sqm
max_occupancy=3.0

#Starting temperature of the builidng:
t_m_prev=20




office_list = [Office_1X, Office_2X, Office_32]


electricity_demands_list = []
for Office in office_list:
    energy_demand = []
    electricity_demand = []
    for hour in range(8760):

        #Occupancy for the time step
        occupancy = occupancyProfile.loc[hour,'People'] * max_occupancy
        #Gains from occupancy and appliances
        internal_gains = occupancy*gain_per_person + appliance_gains*Office.floor_area

        #Extract the outdoor temperature in Zurich for that hour
        t_out = Zurich.weather_data['drybulb_C'][hour]

        Altitude, Azimuth = Zurich.calc_sun_position(latitude_deg=47.480, longitude_deg=8.536, year=2015, hoy=hour)

        SouthWindow.calc_solar_gains(sun_altitude = Altitude, sun_azimuth = Azimuth,
                                     normal_direct_radiation= Zurich.weather_data['dirnorrad_Whm2'][hour],
                                     horizontal_diffuse_radiation = Zurich.weather_data['difhorrad_Whm2'][hour])

        SouthWindow.calc_illuminance(sun_altitude = Altitude, sun_azimuth = Azimuth,
                                     normal_direct_illuminance = Zurich.weather_data['dirnorillum_lux'][hour],
                                     horizontal_diffuse_illuminance = Zurich.weather_data['difhorillum_lux'][hour])


        Office.solve_building_energy(internal_gains=internal_gains, solar_gains=SouthWindow.solar_gains,t_out=t_out,
                                     t_m_prev=t_m_prev)

        Office.solve_building_lighting(illuminance=SouthWindow.transmitted_illuminance, occupancy=occupancy)

        #Set the previous temperature for the next time step

        t_m_prev=Office.t_m_next



        energy_demand.append(Office.energy_demand)
        electricity_demand.append(Office.heating_sys_electricity)

    electricity_demands_list.append(electricity_demand)
    operational_emissions = np.multiply(electricity_demands_list,hourly_emission_factors)

#Visualize hourly values
plt.plot(range(8760), operational_emissions[0], label="direct_power", c="red" )
plt.plot(range(8760), operational_emissions[1], label="ASHP", c="blue")
plt.plot(range(8760), operational_emissions[2], label="GSHP", c="green")

plt.plot(range(8760), electricity_demands_list[0], label="direct_power", c="lightcoral")
plt.plot(range(8760), electricity_demands_list[1], label="ASHP", c="lightblue")
plt.plot(range(8760), electricity_demands_list[2], label="GSHP", c="lightgreen")
plt.legend()
plt.show()


#Visualize yearly value:

plt.bar([0,1,2],[operational_emissions[0].sum()/1000.,operational_emissions[1].sum()/1000.,operational_emissions[2].sum()/1000.])
plt.show()