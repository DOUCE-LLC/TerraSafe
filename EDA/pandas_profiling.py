import pandas as pd
import ydata_profiling as ydata

# https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv
df = pd.read_csv('../Data/Raw data/query.csv')

# Generate the profile report
profile = ydata.ProfileReport(df)

# Export as HTML
profile.to_file('./routes/example1.html')