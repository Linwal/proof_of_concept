import sys
sys.path.insert(1, r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator")
from building_physics import Building
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import data_prep as dp
import supply_system
import emission_system
from radiation import Location
from radiation import Window
from radiation import PhotovoltaicSurface


Zurich = Location(epwfile_path=r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator\auxiliary\Zurich-Kloten_2013.epw")



window_area = 6.0  # m2
external_envelope_area=15.0  # m2 (south oriented)
room_depth=7.0  # m
room_width=5.0  # m
room_height=3.0  # m
lighting_load=11.7  # [W/m2] (source?)
lighting_control = 300.0  # lux threshold at which the lights turn on.
lighting_utilisation_factor=0.45
lighting_maintenance_factor=0.9
u_walls = 0.17  # W/m2K
u_windows = 1.0  # W/m2K
ach_vent= 1.0  # Air changes per hour through ventilation [Air Changes Per Hour]
ach_infl= 0.4 # Air changes per hour through infiltration [Air Changes Per Hour]
ventilation_efficiency=0.6
thermal_capacitance_per_floor_area = 165000
t_set_heating = 20.0
t_set_cooling = 26.0
max_cooling_energy_per_floor_area=0
max_heating_energy_per_floor_area=np.inf
pv_area = 1 #m2

use_type = 3  # only goes into electrical appliances according to SIA (1=residential, 3= office)


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



SouthWindow = Window(azimuth_tilt=0, alititude_tilt = 90, glass_solar_transmittance=0.2,
                     glass_light_transmittance=0.5, area =4)

## Define PV to this building

RoofPV = PhotovoltaicSurface(azimuth_tilt=0, alititude_tilt = 45, stc_efficiency=0.18,
                     performance_ratio=0.8, area = pv_area)


## Define occupancy
occupancyProfile=pd.read_csv(r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator\auxiliary\schedules_el_OFFICE.csv")

## Define constants

gain_per_person = 100 # W per sqm
appliance_gains= 14 #W per sqm
max_occupancy=3.0

## Define embodied emissions: # In a later stage this could be included in the RC model "supply_system.py file"
coeq_gshp = 272.5 #kg/kW [KBOB 2016]
coeq_borehole = 28.1 #kg/m[KBOB 2016]
coeq_ashp = 363.75 #kg/kW [KBOB 2016]
coeq_underfloor_heating = 5.06 #kg/m2 [KBOB]
coeq_pv = 2080 # kg/kWp [KBOB 2016]


#electricity demand from appliances

electric_appliances = dp.electric_appliances_sia(energy_reference_area=room_depth*room_width, type=use_type, value="ziel")


#Starting temperature of the builidng:
t_m_prev=20.0


hourly_emission_factors = dp.build_monthly_emission_factors()

office_list = [Office_1X, Office_2X, Office_32]


electricity_demands_list = []
pv_yields_list = []
heating_demands_list = []
for Office in office_list:
    electricity_demand = np.empty(8760)
    solar_yield = []
    heating_demand = []
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

        RoofPV.calc_solar_yield(sun_altitude = Altitude, sun_azimuth=Azimuth,
                               normal_direct_radiation=Zurich.weather_data['dirnorrad_Whm2'][hour],
                               horizontal_diffuse_radiation=Zurich.weather_data['difhorrad_Whm2'][hour])


        Office.solve_building_energy(internal_gains=internal_gains, solar_gains=SouthWindow.solar_gains,t_out=t_out,
                                     t_m_prev=t_m_prev)

        Office.solve_building_lighting(illuminance=SouthWindow.transmitted_illuminance, occupancy=occupancy)

        #Set the previous temperature for the next time step

        t_m_prev=Office.t_m_next



        heating_demand.append(Office.energy_demand)
        electricity_demand[hour] = Office.heating_sys_electricity
        solar_yield.append(RoofPV.solar_yield)

    electricity_demand = electricity_demand + electric_appliances
    heating_demands_list.append(heating_demand)
    electricity_demands_list.append(electricity_demand) # in Wh
    pv_yields_list.append(solar_yield) #in Wh

net_electricity_demands_list = np.subtract(electricity_demands_list, pv_yields_list)


net_operational_emissions = np.multiply(net_electricity_demands_list/1000.,hourly_emission_factors)
operational_emissions =  np.copy(net_operational_emissions)
operational_emissions[operational_emissions<0] = 0.00
#negative_emissions = np.copy(net_operational_emissions)
#negative_emissions[negative_emissions>0] = 0.00


## embodied emissions:

#PV
kwp_pv = RoofPV.area * RoofPV.efficiency # = kWp
pv_embodied = kwp_pv*coeq_pv


# direct electrical
embodied_direct = 0  #_embodied emissions of the electrical heating system

# ASHP
ashp_power = np.percentile(heating_demands_list[1],97.5)/1000. #kW

ashp_embodied = coeq_ashp*ashp_power # kgCO2eq
underfloor_heating_embodied = coeq_underfloor_heating * Office_2X.floor_area # kgCO2eq

embodied_ashp = ashp_embodied + underfloor_heating_embodied # + pv_embodied

# GSHP
borehole_depth = 20 #m/kW - entspricht einer spezifischen Entzugsleistung von 50W/m
gshp_power = np.percentile(heating_demands_list[2],97.5)/1000 #kW
gshp_embodied = coeq_gshp * gshp_power # kgCO2eq
# underfloor_heating_embodied = coeq_underfloor_heating * Office_2X.floor_area # kgCO2eq
borehole_embodied = coeq_borehole * borehole_depth * gshp_power

embodied_gshp = gshp_embodied + underfloor_heating_embodied + borehole_embodied # + pv_embodied



embodied_emissions = np.array([embodied_direct, embodied_ashp, embodied_gshp])

# Annual for 25years lifetime
lifetime=25. #y
annual_embodied_emissions = embodied_emissions/lifetime
pv_embodied = pv_embodied/lifetime




#### Total emissions


annual_operational_emissions = operational_emissions.sum(axis=1)
#annual_negative_emissions = negative_emissions.sum(axis=1)


total_emissions = annual_embodied_emissions+annual_operational_emissions+pv_embodied # + annual_negative_emissions
print(total_emissions)

p0 = plt.bar([0,1,2], [pv_embodied,pv_embodied,pv_embodied], color="y")
p1 = plt.bar([0,1,2], annual_embodied_emissions, color="lightblue", bottom=pv_embodied)
p2 = plt.bar([0,1,2], annual_operational_emissions, bottom=annual_embodied_emissions+pv_embodied, color="blue")
#p3 = plt.bar([0,1,2], annual_negative_emissions, bottom=[0,0,0], color="orange")
plt.title("U_opaque=" + str(u_walls) + " and U windows=" + str(u_windows) + "\nAirChangeInf=" +str(ach_infl) + " AirChangeVent=" + str(ach_vent) + " PV=" + str(kwp_pv) +"kW" )
plt.ylabel("kgCO2eq/annum")
plt.xticks([0,1,2], ("Pure electric", "ASHP", "GSHP"))
plt.legend((p0[0], p1[0], p2[0]),('embodied PV', 'embodied systems', 'operational'))
plt.axhline(y=total_emissions[0], xmin=0, xmax=1./3.)
plt.axhline(y=total_emissions[1], xmin=1./3., xmax=2./3.)
plt.axhline(y=total_emissions[2], xmin=2./3., xmax=1.)
# plt.ylim(0,100)
plt.show()











#Visualize hourly values
# plt.plot(range(8760), operational_emissions[0], label="direct_power", c="red", ls='--', lw="0.7", marker=".", ms=0.7 )
# plt.plot(range(8760), operational_emissions[1], label="ASHP", c="blue", ls='--', lw="0.7", marker=".", ms=0.7)
# plt.plot(range(8760), operational_emissions[2], label="GSHP", c="green", ls='--', lw="0.7", marker=".", ms=0.7)
#
# plt.plot(range(8760), net_electricity_demands_list[0], label="direct_power", c="lightcoral", ls='--', lw="0.7", marker=".", ms=0.7)
# plt.plot(range(8760), net_electricity_demands_list[1], label="ASHP", c="lightblue", ls='--', lw="0.7",marker=".", ms=0.7)
# plt.plot(range(8760), net_electricity_demands_list[2], label="GSHP", c="lightgreen", ls='--',lw="0.7", marker=".", ms=0.7)
# plt.legend()
# plt.show()