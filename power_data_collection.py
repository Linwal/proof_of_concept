import pandas as pd
from entsoe import EntsoePandasClient


## Entsoe Transparancy platform login:

key = "285a3e21-c574-453b-9690-e327c7bd73fd"  ## don't publish
client = EntsoePandasClient(api_key=key)

## Time window:

start_time = pd.Timestamp('20150101', tz='Europe/Brussels')
end_time = pd.Timestamp('20150130', tz='Europe/Brussels')

country_code = "CH" # Switzerland

neighbour_countries = ["AT", "DE", "FR", "IT"]


domestic_production = client.query_generation(country_code, start=start_time, end=end_time, psr_type=None)

neighbour_production = []

for country in neighbour_countries:
    neighbour_production.append(client.query_generation(country, start=start_time, end=end_time, psr_type=None))

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


quit()


cross_border_flows = []
for country in neighbour_countries:
    cross_border_flows.append(client.query_crossborder_flows(country, country_code, start=start_time, end=end_time))


