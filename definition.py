import sys
sys.path.insert(1, r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator")
from building_physics import Building
import numpy as np
import pandas as pd
import data_prep as dp
import supply_system
import emission_system
from radiation import Location
from radiation import Window
from radiation import PhotovoltaicSurface


def run_rc_simulation(external_envelope_area, window_area, room_width, room_depth, room_height,
                   thermal_capacitance_per_floor_area, u_walls, u_windows, ach_vent, ach_infl, ventilation_efficiency,
                   max_heating_energy_per_floor_area, max_cooling_energy_per_floor_area, pv_area, pv_efficiency,
                   pv_tilt, pv_azimuth, lifetime, strom_mix, weatherfile_path, grid_decarbonization_factors,
                   t_set_heating, t_set_cooling, annual_dhw_p_person, dhw_supply_temperature, use_type):


    Loc = Location(epwfile_path=weatherfile_path)

    ## So far the lighting load is still hard coded because it is not looked at.
    lighting_load=11.7  # [W/m2] (source?)
    lighting_control = 300.0  # lux threshold at which the lights turn on.
    lighting_utilisation_factor=0.45
    lighting_maintenance_factor=0.9


    ## Define constants

    gain_per_person = 100 # W per sqm (why is that per sqm when it says per person?)
    appliance_gains= 14 #W per sqm
    max_occupancy=50  # number of occupants (could be simplified by using area per person values)
    floor_area = room_width * room_depth


    Office = Building(window_area=window_area,
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
                    max_cooling_energy_per_floor_area=max_cooling_energy_per_floor_area[0],
                    max_heating_energy_per_floor_area=max_heating_energy_per_floor_area[0],
                    heating_supply_system=supply_system.ElectricHeating,
                    cooling_supply_system=supply_system.DirectCooler, # What can we choose here for purely electric case?
                    heating_emission_system=emission_system.FloorHeating,
                    cooling_emission_system=emission_system.AirConditioning,
                    dhw_supply_temperature=dhw_supply_temperature,)


    SouthWindow = Window(azimuth_tilt=0., alititude_tilt = 90.0, glass_solar_transmittance=0.5,
                         glass_light_transmittance=0.5, area =window_area)

    ## Define PV to this building

    RoofPV = PhotovoltaicSurface(azimuth_tilt=pv_azimuth, alititude_tilt = pv_tilt, stc_efficiency=pv_efficiency,
                         performance_ratio=0.8, area = pv_area)  # Performance ratio is still hard coded.


    ## Define occupancy
    occupancyProfile=pd.read_csv(r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator\auxiliary\occupancy_office.csv")




    ## Define embodied emissions: # In a later stage this could be included in the RC model "supply_system.py file"
    coeq_gshp = dp.embodied_emissions_heat_generation_kbob_per_kW("gshp")  # kgCO2/kW ## zusätzlich automatisieren
    coeq_borehole = dp.embodied_emissions_borehole_per_m() #kg/m
    coeq_ashp = dp.embodied_emissions_heat_generation_kbob_per_kW("ashp")  # kgCO2/kW ## zusätzlich automatisieren
    coeq_underfloor_heating = dp.embodied_emissions_heat_emission_system_per_m2("underfloor heating") #kg/m2
    coeq_pv = dp.embodied_emissions_pv_per_kW()  # kg/kWp
    coeq_el_heater = dp.embodied_emissions_heat_generation_kbob_per_kW("electric heater")  #kg/kW


    #electricity demand from appliances

    electric_appliances = dp.electric_appliances_sia(energy_reference_area=room_depth*room_width, type=use_type, value="ziel")


    #Starting temperature of the builidng:
    t_m_prev=20.0 # This is only for the very first step in therefore is hard coded.


    # hourly_emission_factors = dp.build_yearly_emission_factors(strom_mix)
    # hourly_emission_factors = dp.build_monthly_emission_factors(strom_mix)
    hourly_emission_factors = dp.build_yearly_emission_factors(strom_mix)
    hourly_emission_factors = hourly_emission_factors*grid_decarbonization_factors.mean()




    electricity_demand = np.empty(8760)
    pv_yield = np.empty(8760)
    total_heat_demand = np.empty(8760)
    heating_electricity_demand = np.empty(8760)
    heating_demand = np.empty(8760)
    cooling_electricity_demand = np.empty(8760)
    cooling_demand = np.empty(8760)
    solar_gains = np.empty(8760)
    indoor_temperature = np.empty(8760)


    for hour in range(8760):

        #Occupancy for the time step
        occupancy = occupancyProfile.loc[hour,'People'] * max_occupancy
        #Gains from occupancy and appliances
        internal_gains = occupancy*gain_per_person + appliance_gains*Office.floor_area

        # Domestic hot water schedule
        dhw_demand = annual_dhw_p_person/ occupancyProfile['People'].sum() * occupancy  # Wh

        #Extract the outdoor temperature in Zurich for that hour
        t_out = Loc.weather_data['drybulb_C'][hour]

        Altitude, Azimuth = Loc.calc_sun_position(latitude_deg=47.480, longitude_deg=8.536, year=2015, hoy=hour)

        SouthWindow.calc_solar_gains(sun_altitude = Altitude, sun_azimuth = Azimuth,
                                     normal_direct_radiation= Loc.weather_data['dirnorrad_Whm2'][hour],
                                     horizontal_diffuse_radiation = Loc.weather_data['difhorrad_Whm2'][hour])

        SouthWindow.calc_illuminance(sun_altitude = Altitude, sun_azimuth = Azimuth,
                                     normal_direct_illuminance = Loc.weather_data['dirnorillum_lux'][hour],
                                     horizontal_diffuse_illuminance = Loc.weather_data['difhorillum_lux'][hour])

        RoofPV.calc_solar_yield(sun_altitude = Altitude, sun_azimuth=Azimuth,
                               normal_direct_radiation=Loc.weather_data['dirnorrad_Whm2'][hour],
                               horizontal_diffuse_radiation=Loc.weather_data['difhorrad_Whm2'][hour])


        Office.solve_building_energy(internal_gains=internal_gains, solar_gains=SouthWindow.solar_gains,t_out=t_out,
                                     t_m_prev=t_m_prev, dhw_demand=dhw_demand)

        Office.solve_building_lighting(illuminance=SouthWindow.transmitted_illuminance, occupancy=occupancy)

        #Set the previous temperature for the next time step

        t_m_prev=Office.t_m_next



        heating_electricity_demand[hour] =Office.heating_sys_electricity  # unit? heating electricity demand
        cooling_electricity_demand[hour] = Office.cooling_sys_electricity  # unit?
        solar_gains[hour] = SouthWindow.solar_gains
        electricity_demand[hour] = Office.heating_sys_electricity + Office.dhw_sys_electricity + Office.cooling_sys_electricity  # in Wh
        pv_yield[hour]=RoofPV.solar_yield  # in Wh
        heating_demand[hour] = Office.heating_demand  # this is the actual heat emitted, unit?
        cooling_demand[hour] = Office.cooling_demand
        indoor_temperature[hour] = Office.t_air

        total_heat_demand[hour] = Office.heating_demand + Office.dhw_demand



    electricity_demand = electricity_demand + electric_appliances




    max_required_heating_per_floor_area = max(heating_demand)/floor_area  # W/m2
    max_required_cooling_per_floor_area = min(cooling_demand)/floor_area  # W/m2


    net_electricity_demand = np.subtract(electricity_demand, pv_yield)

    net_self_consumption = np.empty(8760)
    for hour in range(8760):
        net_self_consumption[hour] = min(pv_yield[hour], electricity_demand[hour])


    # this is the ratio of electricity used to electricity produced and thus the emissions that are allocated to the building.
    # This is highly questionable, meaning, it is discussed a lot
    embodied_pv_ratio = net_self_consumption.sum()/pv_yield.sum()



    net_operational_emissions = np.multiply(net_electricity_demand / 1000., hourly_emission_factors)
    operational_emissions = np.copy(net_operational_emissions)
    operational_emissions[operational_emissions < 0] = 0.00


    ## heat calculations:
    annual_normalized_heat_demand = heating_demand.sum()/1000 / floor_area

    print("Annual_normalized_heat_demand:")
    print(annual_normalized_heat_demand)


    ## embodied emissions:    DO NOT YET USE THIS PART OF THE SIMULATION!!!!!
    #
    # #PV
    # kwp_pv = RoofPV.area * RoofPV.efficiency # = kWp
    # pv_embodied = kwp_pv*coeq_pv
    #
    #
    # # direct electrical
    # embodied_direct = coeq_el_heater * np.percentile(heating_electricity_demand, 97.5)/1000. \
    #                   + pv_embodied * embodied_pv_ratio #_embodied emissions of the electrical heating system
    #
    # # ASHP
    # ashp_power = np.percentile(heating_el_demands_list[1],97.5)/1000. #kW
    # ashp_embodied = coeq_ashp*ashp_power # kgCO2eq
    # underfloor_heating_embodied = coeq_underfloor_heating * Office_2X.floor_area # kgCO2eq
    # embodied_ashp = ashp_embodied + underfloor_heating_embodied + pv_embodied*embodied_pv_ratio[1]
    #
    # # GSHP
    # borehole_depth = 20 #m/kW - entspricht einer spezifischen Entzugsleistung von 50W/m
    # gshp_power = np.percentile(heating_el_demands_list[2],97.5)/1000 #kW
    # gshp_embodied = coeq_gshp * gshp_power # kgCO2eq
    # # underfloor_heating_embodied = coeq_underfloor_heating * Office_2X.floor_area # kgCO2eq
    # borehole_embodied = coeq_borehole * borehole_depth * gshp_power
    # embodied_gshp = gshp_embodied + underfloor_heating_embodied + borehole_embodied + pv_embodied * embodied_pv_ratio[2]
    # embodied_emissions = np.array([embodied_direct, embodied_ashp, embodied_gshp])
    #
    #
    # # Annual for 25years lifetime
    # annual_embodied_emissions = embodied_emissions/lifetime
    # normalized_annual_embodied_emissions = annual_embodied_emissions/(room_width*room_depth)

    #### Total emissions
    annual_operational_emissions = operational_emissions.sum()
    normalized_annual_operational_emissions = annual_operational_emissions/(room_width*room_depth)

    # normalized_total_emissions = normalized_annual_embodied_emissions+normalized_annual_operational_emissions

    normalized_total_emissions = 0  # placeholder
    normalized_annual_embodied_emissions = 0  # placeholder




    return normalized_total_emissions, normalized_annual_operational_emissions, normalized_annual_embodied_emissions,\
           u_windows, u_walls, thermal_capacitance_per_floor_area, max_required_heating_per_floor_area,\
           max_required_cooling_per_floor_area, indoor_temperature





def comfort_assessment(indoor_temperature_time_series, comfort_range=[19.0, 25.0], discomfort_type="integrated"):
    """
    :param indoor_temperature_time_series: np.array or list of hourly indoor temperature values
    :param comfort_range: list or numpy array with lower and upper limit of comfort range for room temperature
    :return: Number of hours where Temperature is outside comfort zone
    """

    time_series = np.array(indoor_temperature_time_series)
    comfort_range[0]-=0.01 # This will eliminate stupid 19.9999999995 to be too cold for 20
    comfort_range[1]+=0.01
    hours_of_discomfort = []
    degree_hours_of_discomfort = []
    for j in range(time_series.shape[0]):
        low_temp = time_series[j][time_series[j]<comfort_range[0]]
        high_temp = time_series[j][time_series[j]>comfort_range[1]]

        # hours of discomfort
        if discomfort_type == "hod":
            hours_of_discomfort.append(len(low_temp) + len(high_temp))


        elif discomfort_type == "integrated":
            degree_hours_of_discomfort.append(sum(comfort_range[0] - low_temp) + sum(high_temp - comfort_range[1]))

    if discomfort_type == "hod":
        return hours_of_discomfort
    elif discomfort_type == "integrated":
        return degree_hours_of_discomfort

if __name__ == '__main__':
    pass
