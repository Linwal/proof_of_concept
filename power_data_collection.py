import pandas as pd
from entsoe import EntsoePandasClient


## Entsoe Transparancy platform login:

key = "285a3e21-c574-453b-9690-e327c7bd73fd"  ## don't publish
client = EntsoePandasClient(api_key=key)

## Time window:

start_time = pd.Timestamp('20150101', tz='Europe/Brussels')
end_time = pd.Timestamp('20151231', tz='Europe/Brussels')

country_code = "CH" # Switzerland

neighbour_countries = ["AT", "DE", "FR", "IT"]


domestic_production = client.query_generation(country_code, start=start_time, end=end_time, psr_type=None)
print(domestic_production.sum(axis=0).sum())

exit()
neighbour_production = []

for country in neighbour_countries:
    neighbour_production.append(client.query_generation(country_code, start=start_time, end=end_time, psr_type=None))

print("Vogel")


cross_border_flows = []
for country in neighbour_countries:
    cross_border_flows.append(client.query_crossborder_flows(country, country_code, start=start_time, end=end_time))

