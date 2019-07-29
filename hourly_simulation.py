import sys
sys.path.insert(1, r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from building_physics import Building
import supply_system
import emission_system
from radiation import Location
from radiation import Window
from radiation import PhotovoltaicSurface



### Initialise the Location with a weather file

Zurich = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator\auxiliary\Zurich-Kloten_2013.epw")


#### Initialise Building Study

Office=Building(window_area=4.0,
                external_envelope_area=15.0,
                room_depth=7.0,
                room_width=5.0,
                room_height=3.0,
                lighting_load=11.7,
                lighting_control = 300.0,
                lighting_utilisation_factor=0.45,
                lighting_maintenance_factor=0.9,
                u_walls = 0.15,
                u_windows = 0.9,
                ach_vent=1.5,
                ach_infl=0.5,
                ventilation_efficiency=0.6,
                thermal_capacitance_per_floor_area = 165000,
                t_set_heating = 20.0,
                t_set_cooling = 26.0,
                max_cooling_energy_per_floor_area=0,
                max_heating_energy_per_floor_area=np.inf,
                heating_supply_system=supply_system.HeatPumpAir,
                cooling_supply_system=supply_system.HeatPumpAir,
                heating_emission_system=emission_system.NewRadiators,
                cooling_emission_system=emission_system.AirConditioning,)

## Define a window to this building

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

energy_demand = []
electricity_demand=[]

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


plt.plot(electricity_demand)
plt.plot(energy_demand, color="red")
plt.show()

