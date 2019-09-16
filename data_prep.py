import numpy as np
import pandas as pd





def electric_appliances_sia(energy_reference_area, type=1, value="standard"):
    """
    This function calculates the use of electric appliances according to SIA 2024
    :param energy_reference_area: float, m2, energy reference area of the room/building
    :param type: int, use type according to SIA2024
    :param value: str, reference value according to SIA choice of "standard", "ziel" and "bestand"
    :return: np.array of hourly electricity demand for appliances in Wh
    """
    if type==1:  # Typ 1 SIA Wohnen (1.1 MFH, 1.2 EFH)
        max_hourly = {"standard":8.0, "ziel": 4.0, "bestand":10.0}
        demand_profile = max_hourly[value] * np.repeat(
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.8, 0.2, 0.1, 0.1, 0.1, 0.1, 0.8, 0.2, 0.1, 0.1, 0.1, 0.2, 0.8, 1.0, 0.2,
             0.2, 0.2, 0.1], 365)
    elif type==3: #Typ 3 SIA Einzel-, Gruppenbüro
        max_hourly = {"standard": 7.0, "ziel": 3.0, "bestand": 15.0}
        demand_profile = max_hourly[value] * np.repeat(
            [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.6, 0.8, 1.0, 0.8, 0.4, 0.6, 1.0, 0.8, 0.6, 0.2, 0.1, 0.1, 0.1,
             0.1, 0.1, 0.1], 365)

    else:
        print("No demand schedule for electrical appliances has been defined for this case.")

    return demand_profile #Wh


def build_yearly_emission_factors(export_assumption="c"):

    choice = "TEF" + export_assumption
    emissions_df = pd.read_excel(r"C:\Users\walkerl\Documents\code\proof_of_concept\data\emission_factors_AC.xlsx",
                                 index="Time")
    emissions_df = emissions_df.set_index('Time')
    emissions_df.resample('Y').mean()
    hourly_emission_factor = np.repeat(emissions_df.resample('Y').mean()[choice].to_numpy(),8760)/1000.0 #kgCO2eq/kWh
    return hourly_emission_factor


def build_monthly_emission_factors(export_assumption="c"):
    """
    This function creates simple monthly emission factors of the Swiss consumption mix based on the year 2015.
    It returns an hourly list of the monthly values. No input is needed. The list is generated here to omit hard coding
    values within the simulatin process.
    :return: np array of length 8760 with monthly emission factors on hourly resolution.
    """
    if export_assumption=="c":
        grid_emission_factor = {"jan": .1366, "feb": .1548, "mar": .1403, "apr": .1170, "may": .0578, "jun": .0716,
                                "jul": .0956, "aug": .1096, "sep": .1341, "oct": .1750, "nov": .1644, "dec": .1577}  # for TEFc (AC)

    elif export_assumption=="d":
        grid_emission_factor = {"jan": .1108, "feb": .1257, "mar": .1175, "apr": .0937, "may": .0400, "jun": .0463,
                                "jul": .0594, "aug": .0931, "sep": .1111, "oct": .1418, "nov": .1344, "dec": .1343}  # for TEFd (AC)

    else:
        "Choice of export assumption not valid"

    ## Factors above According to ST Alice Chevrier
    ## hours of the months:
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
    ])  # in g/kWh
    return hourly_emission_factors

def build_grid_emission_hourly(export_assumption="c"):
    emissions_df = pd.read_excel(r"C:\Users\walkerl\Documents\code\proof_of_concept\data\emission_factors_AC.xlsx")
    choice="TEF"+export_assumption
    hourly_emission_factors = emissions_df[choice].to_numpy()/1000.0
    return(hourly_emission_factors)

