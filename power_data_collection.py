import pandas as pd
from entsoe import EntsoePandasClient
import matplotlib.pyplot as plt


## Entsoe Transparancy platform login:

key = "285a3e21-c574-453b-9690-e327c7bd73fd"  ## don't publish
client = EntsoePandasClient(api_key=key)

## Time window:

start_time = pd.Timestamp('20160101', tz='Europe/Brussels')
end_time = pd.Timestamp('20161231', tz='Europe/Brussels')

country_code = "CH" # Switzerland

neighbour_countries = ["AT", "DE", "FR", "IT"]

# it is resampled to an hour with mean because the values coming out of the database are acutally given in MW and not in MWh
domestic_production = client.query_generation(country_code, start=start_time, end=end_time, psr_type=None).resample("H").mean()
neighbour_production = []

for country in neighbour_countries:
    neighbour_production.append(client.query_generation(country, start=start_time, end=end_time, psr_type=None).resample("H").mean())


emission_production_matrix_filepath = r"C:\Users\walkerl\Documents\code\proof_of_concept\data\emissions_technology_matrix.xlsx"
emission_production_matrix = pd.read_excel(emission_production_matrix_filepath, index_col=0)


#import emissions per technology (gCO2eq/kWh)
domestic_emissions_df = pd.DataFrame(index=domestic_production.index, columns=domestic_production.keys())

# This selects the data source for the emission factors.
data_source = "EMPA HUESS"


for power_type in domestic_production.keys():
    domestic_emissions_df[power_type] = domestic_production[power_type]
    domestic_emissions_df.loc[:,power_type] *= emission_production_matrix.loc[data_source, power_type]

domestic_emission_factor = domestic_emissions_df.sum(axis=1).divide(domestic_production.sum(axis=1))

neighbour_emission_factors = []
for neighbour in neighbour_production:
    neighbour_emissions_df = pd.DataFrame(index=neighbour.index, columns=neighbour.keys())

    for power_type in neighbour:

        neighbour_emissions_df[power_type] = neighbour[power_type]
        neighbour_emissions_df.loc[:,power_type] *= emission_production_matrix.loc[data_source, power_type]

    neighbour_emission_factors.append(neighbour_emissions_df.sum(axis=1).divide(neighbour.sum(axis=1)))


import_cross_border_flows = [] # if the flows are power and not energy, change the resampling from sum to mean
for country in neighbour_countries:
    # resampling to the hour with mean because quarter hourly values are given in MW not MWh
    import_cross_border_flows.append(client.query_crossborder_flows(country, country_code, start=start_time, end=end_time).resample("H").mean())



#Initialization of tatal factor with total summation of emmissions of domestic production
total_emission_factor = domestic_emissions_df.sum(axis=1)
# print("Gelb")
# print(total_emission_factor)
# print("hier_gopfer")
# print(import_cross_border_flows[0])
# print("am gopfsten")
# print(neighbour_emission_factors[0])
# print("hier_gopf")
# print(import_cross_border_flows[0]*neighbour_emission_factors[0])
# print("hier werden die nefs geprinted:")
# print(neighbour_emission_factors)
# quit()


total_production_and_import = domestic_production.sum(axis=1)

for i in range(len(neighbour_countries)):
    # fill_value=0 resolves the problem of having NANs in the cross_border_flows
    total_emission_factor = total_emission_factor +(import_cross_border_flows[i] * (neighbour_emission_factors[i]))
    total_production_and_import.add(import_cross_border_flows[i])

total_emission_factor = total_emission_factor.divide(total_production_and_import)
print(total_emission_factor)


plt.plot(total_emission_factor)
plt.show()