import sys
sys.path.insert(1, r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator")
import os
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


def run_simulation(external_envelope_area, window_area, room_width, room_depth, room_height,
                   thermal_capacitance_per_floor_area, u_walls, u_windows, ach_vent, ach_infl, ventilation_efficiency,
                   max_heating_energy_per_floor_area, max_cooling_energy_per_floor_area, pv_area, pv_efficiency,
                   pv_tilt, pv_azimuth, lifetime, strom_mix, weatherfile_path, grid_decarbonization_factors):



    # dirname = os.path.dirname(__file__)
    # wall_data_path = os.path.join(dirname, 'data/walls.xlsx')

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

    # wall_name = "Betonwand, Wärmedämmung mit Lattenrost, Verkleidung"
    # wall_name = "Holzblockwand, Aussenwärmedämmung, Verkleidung"
    # wall_name = "Sichtbetonwand, Aussenwärmedämmung verputzt"
    # wall_name = "Sichtbacksteinmauerwerk, Aussenwärmedämmung verputzt"





    # LocList = [Zurich, Recife, SaoPaolo, Vancouver, PuntaArenas, Stuttgart, Copenhagen, Algier, Barcelona, London, Milano,
    #            Rome, Kiruna, Ostersund, LongBeach_LA, DesMoines, Chicago]

    # Loc = Zurich

    Loc = Location(epwfile_path=weatherfile_path)



    lighting_load=11.7  # [W/m2] (source?)
    lighting_control = 300.0  # lux threshold at which the lights turn on.
    lighting_utilisation_factor=0.45
    lighting_maintenance_factor=0.9


    t_set_heating = 20.0
    t_set_cooling = 26.0


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
                    max_cooling_energy_per_floor_area=max_cooling_energy_per_floor_area[0],
                    max_heating_energy_per_floor_area=max_heating_energy_per_floor_area[0],
                    heating_supply_system=supply_system.ElectricHeating,
                    cooling_supply_system=supply_system.DirectCooler, # What can we choose here for purely electric case?
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
                    max_cooling_energy_per_floor_area=max_cooling_energy_per_floor_area[1],
                    max_heating_energy_per_floor_area=max_heating_energy_per_floor_area[1],
                    heating_supply_system=supply_system.HeatPumpAir,
                    cooling_supply_system=supply_system.HeatPumpAir,
                    heating_emission_system=emission_system.FloorHeating,
                    cooling_emission_system=emission_system.FloorHeating,)

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
                    max_cooling_energy_per_floor_area=max_cooling_energy_per_floor_area[2],
                    max_heating_energy_per_floor_area=max_heating_energy_per_floor_area[2],
                    heating_supply_system=supply_system.HeatPumpWater,
                    cooling_supply_system=supply_system.HeatPumpWater,
                    heating_emission_system=emission_system.FloorHeating,
                    cooling_emission_system=emission_system.FloorHeating,)


    ### emission factors according to empa_Alice Chevrier Semester Project in g/Wh

    # aproximated values from the graph



    SouthWindow = Window(azimuth_tilt=0., alititude_tilt = 90.0, glass_solar_transmittance=0.5,
                         glass_light_transmittance=0.5, area =window_area)

    ## Define PV to this building

    RoofPV = PhotovoltaicSurface(azimuth_tilt=pv_azimuth, alititude_tilt = pv_tilt, stc_efficiency=pv_efficiency,
                         performance_ratio=0.8, area = pv_area)


    ## Define occupancy
    occupancyProfile=pd.read_csv(r"C:\Users\walkerl\Documents\code\RC_BuildingSimulator\rc_simulator\auxiliary\schedules_el_SINGLE_RES.csv")


    ## Define constants

    gain_per_person = 100 # W per sqm
    appliance_gains= 14 #W per sqm
    max_occupancy=4.0

    ## Define embodied emissions: # In a later stage this could be included in the RC model "supply_system.py file"
    coeq_gshp = 272.5 #kg/kW [KBOB 2016]
    coeq_borehole = 28.1 #kg/m[KBOB 2016]
    coeq_ashp = 363.75 #kg/kW [KBOB 2016]
    coeq_underfloor_heating = 5.06 #kg/m2 [KBOB]
    coeq_pv = 2080 # kg/kWp [KBOB 2016]

    coeq_el_heater = 7.2/5.0  #kg/kW [ecoinvent auxiliary heating unit production, electric, 5kW]

    #standard on GWP100, 0.18m insulation
    # coeq_wall = dp.extract_wall_data(wall_data_path, name=wall_name, area=external_envelope_area-window_area)


    #electricity demand from appliances

    electric_appliances = dp.electric_appliances_sia(energy_reference_area=room_depth*room_width, type=use_type, value="ziel")


    #Starting temperature of the builidng:
    t_m_prev=20.0


    # hourly_emission_factors = dp.build_yearly_emission_factors(strom_mix)
    # hourly_emission_factors = dp.build_monthly_emission_factors(strom_mix)
    hourly_emission_factors = dp.build_yearly_emission_factors(strom_mix)
    hourly_emission_factors = hourly_emission_factors*grid_decarbonization_factors.mean()
    office_list = [Office_1X, Office_2X, Office_32]


    electricity_demands_list = []
    pv_yields_list = []
    heating_demands_list = []
    cooling_demands_list = []
    indoor_temperature_list = []
    heat_emission_list = []
    cold_emission_list = []


    for Office in office_list:
        electricity_demand = np.empty(8760)
        solar_yield = np.empty(8760)
        heating_demand = []
        cooling_demand = []
        solar_gains = []
        indoor_temperature = []
        emission_heat_demand = []
        emission_cold_demand = []

        for hour in range(8760):

            #Occupancy for the time step
            occupancy = occupancyProfile.loc[hour,'People'] * max_occupancy
            #Gains from occupancy and appliances
            internal_gains = occupancy*gain_per_person + appliance_gains*Office.floor_area

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
                                         t_m_prev=t_m_prev)

            Office.solve_building_lighting(illuminance=SouthWindow.transmitted_illuminance, occupancy=occupancy)

            #Set the previous temperature for the next time step

            t_m_prev=Office.t_m_next



            heating_demand.append(Office.heating_sys_electricity)
            cooling_demand.append(Office.cooling_sys_electricity)
            solar_gains.append(SouthWindow.solar_gains)
            electricity_demand[hour] = Office.heating_sys_electricity + Office.cooling_sys_electricity
            solar_yield[hour]=RoofPV.solar_yield
            emission_heat_demand.append(Office.heating_demand)
            emission_cold_demand.append(Office.cooling_demand)
            indoor_temperature.append(Office.t_air)

        plt.plot(indoor_temperature)
        plt.axhline(20)
        plt.axhline(26)
        plt.show()
        electricity_demand = electricity_demand + electric_appliances
        heating_demands_list.append(heating_demand)  # This is the electricity needed for heating with the respective system
        heat_emission_list.append(emission_heat_demand)  # This is the actual heat emitted
        cooling_demands_list.append(cooling_demand)  # This is the electricity needed for cooling with the respective system
        cold_emission_list.append(emission_cold_demand) # This is the actual heat emitted
        electricity_demands_list.append(electricity_demand) # in Wh
        pv_yields_list.append(solar_yield) #in Wh
        indoor_temperature_list.append(indoor_temperature)
    floor_area = room_width * room_depth
    max_required_heating_per_floor_area = [max(heat_emission_list[0])/floor_area,
                                           max(heat_emission_list[1])/floor_area,
                                           max(heat_emission_list[2])/floor_area]  # W/m2
    max_required_cooling_per_floor_area = [min(cold_emission_list[0])/floor_area,
                                           min(cold_emission_list[1])/floor_area,
                                           min(cold_emission_list[2])/floor_area]  # W/m2


    net_electricity_demands_list = np.subtract(electricity_demands_list, pv_yields_list)

    net_self_consumption = np.empty((len(office_list), 8760))
    for i in range(len(office_list)):
        for hour in range(8760):
            net_self_consumption[i][hour] = min(pv_yields_list[i][hour], electricity_demands_list[i][hour])


    # this is the ratio of electricity used to electricity produced and thus the emissions that are allocated to the building.
    embodied_pv_ratio = net_self_consumption.sum(axis=1)/np.array(pv_yields_list).sum(axis=1)



    net_operational_emissions = np.multiply(net_electricity_demands_list/1000.,hourly_emission_factors)
    operational_emissions = np.copy(net_operational_emissions)
    operational_emissions[operational_emissions<0] = 0.00


    ## embodied emissions:

    #PV
    kwp_pv = RoofPV.area * RoofPV.efficiency # = kWp
    pv_embodied = kwp_pv*coeq_pv


    # direct electrical
    el_underfloor_heating_embodied = coeq_underfloor_heating * Office_2X.floor_area # kgCO2eq [wird als zusatz genommen weil mit heater alleine ja noch nicht geheizt]
    embodied_direct = coeq_el_heater * np.percentile(heating_demands_list[0],97.5)/1000. +el_underfloor_heating_embodied + pv_embodied * embodied_pv_ratio[0] #_embodied emissions of the electrical heating system

    # ASHP
    ashp_power = np.percentile(heating_demands_list[1],97.5)/1000. #kW
    ashp_embodied = coeq_ashp*ashp_power # kgCO2eq
    underfloor_heating_embodied = coeq_underfloor_heating * Office_2X.floor_area # kgCO2eq
    embodied_ashp = ashp_embodied + underfloor_heating_embodied + pv_embodied*embodied_pv_ratio[1]

    # GSHP
    borehole_depth = 20 #m/kW - entspricht einer spezifischen Entzugsleistung von 50W/m
    gshp_power = np.percentile(heating_demands_list[2],97.5)/1000 #kW
    gshp_embodied = coeq_gshp * gshp_power # kgCO2eq
    # underfloor_heating_embodied = coeq_underfloor_heating * Office_2X.floor_area # kgCO2eq
    borehole_embodied = coeq_borehole * borehole_depth * gshp_power
    embodied_gshp = gshp_embodied + underfloor_heating_embodied + borehole_embodied + pv_embodied * embodied_pv_ratio[2]
    embodied_emissions = np.array([embodied_direct, embodied_ashp, embodied_gshp])


    # Annual for 25years lifetime
    annual_embodied_emissions = embodied_emissions/lifetime
    normalized_annual_embodied_emissions = annual_embodied_emissions/(room_width*room_depth)
    #### Total emissions
    annual_operational_emissions = operational_emissions.sum(axis=1)
    normalized_annual_operational_emissions = annual_operational_emissions/(room_width*room_depth)

    normalized_total_emissions = normalized_annual_embodied_emissions+normalized_annual_operational_emissions

    annual_heating_demand = sum(heating_demand)/(room_depth*room_width)
    annual_cooling_demand = sum(cooling_demand)/(room_depth*room_width)
    #
    # #
    # fig, ax1 = plt.subplots()
    # ax1.bar([0,1,2], normalized_annual_embodied_emissions, color="lightblue", label="embodied systems")
    # ax1.bar([0,1,2], normalized_annual_operational_emissions, bottom=normalized_annual_embodied_emissions,
    #              color="blue", label="grid allocated")
    # ax1.bar([0,1,2], [pv_embodied*embodied_pv_ratio[0]/lifetime/(room_depth*room_width),
    #                        pv_embodied*embodied_pv_ratio[1]/lifetime/(room_depth*room_width),
    #                        pv_embodied*embodied_pv_ratio[2]/lifetime/(room_depth*room_width)], color="y",
    #         label="PV allocated")
    #
    # ax1.set_title("U_opaque=" + str(u_walls) + " and U windows=" + str(u_windows) + "\nAirChangeInf=" +str(ach_infl) + " AirChangeVent=" + str(ach_vent) + " PV=" + str(kwp_pv) +"kW" )
    # ax1.set_ylabel("kgCO2eq/(a*m2)")
    # plt.xticks([0,1,2], ("Pure electric", "ASHP", "GSHP"))
    # ax2 = ax1.twinx()
    # ax2.axhline(annual_heating_demand/1000, color="red", label="heating demand")
    # ax2.axhline(annual_cooling_demand/1000, color= "blue", label="cooling demand")
    # ax2.set_ylabel("kWh/(a*m2)")
    # ax2.set_ylim(0)
    # plt.figlegend(loc="center right", bbox_to_anchor=(0.88,0.67))
    # plt.show()





    return normalized_total_emissions, normalized_annual_operational_emissions, normalized_annual_embodied_emissions,\
           u_windows, u_walls, thermal_capacitance_per_floor_area, max_required_heating_per_floor_area,\
           max_required_cooling_per_floor_area, indoor_temperature_list




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
