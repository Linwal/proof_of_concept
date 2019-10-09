import pandas as pd
import entsoe as ee


## Entsoe Transparancy platform login:

key = "285a3e21-c574-453b-9690-e327c7bd73fd "  ## don't publish


## Time window:

start_time = pd.Timestamp('20150101', tz='Europe/Brussels')
end_time = pd.Timestamp('20151231', tz='Europe/Brussels')

country_code = "CH" # Switzerland

neighbour_countries = ["AT", "DE", "FR", "IT"]

