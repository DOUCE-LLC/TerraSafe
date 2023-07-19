import requests
import os

for year in range(2023, 2024):
    df1 = pd.DataFrame()

    for month in range(1, 13):
        
        url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv&starttime={year}-{month}-01&endtime={year}-{month}-31"
        response = requests.get(url)
        file_name = f"USGS_{year}_{month}.csv"

        with open(file_name, 'wb') as file:
            file.write(response.content)

        available_columns = pd.read_csv(file_name, nrows=0).columns.tolist()

        if available_columns:
            df2 = pd.read_csv(file_name)
            df2.sort_values(by=['time'], ascending=True, inplace=True)
            df1 = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)
        else:
            print(f'{file_name} have some problems...')
        os.remove(file_name)
    output_file = f'../Data/Raw data/Raw_USGS_{year}.csv'
    df1.to_csv(output_file, index=False)