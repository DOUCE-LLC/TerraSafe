import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

import os
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_absolute_error

# Título de la página de inicio
# st.title('TerraSafe - Sinusoidal Regression')

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../Streamlit/terra-safe.json'

# Create a BigQuery client with the credentials
bq_client = bigquery.Client()

# Query your table
query = f"""
            SELECT *
            FROM `terra-safe-391718.AIRFLOW.USGS_JPN`
            WHERE time > TIMESTAMP('2017-01-01') AND time < TIMESTAMP('2020-01-01')
            ORDER BY time ASC;
        """
df = bq_client.query(query).to_dataframe()

# Group by date and select the row with the highest 'mag' value for each date
# df = df.loc[df.groupby(df['time'].dt.date)['mag'].idxmax()]
df['timeIndex'] = pd.to_datetime(df['time'])  # Create a new column 'timeIndex' with the same values as 'time'
df.set_index('timeIndex', inplace=True)        # Set the new 'timeIndex' column as the DataFrame's index
df = df.resample('W').max()                   # Resample the data by week and take the maximum magnitude value for each week

print(df)

df['time'] = df['time'].apply(lambda x: int(datetime.timestamp(x)))

X = df['time'].values.reshape(-1, 1)
y = df['mag'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=1)

scaler = StandardScaler()
X_train_scaler = scaler.fit_transform(X_train)
X_test_scaler = scaler.transform(X_test)

lin = LinearRegression()

#----- Modify the feature transformation to sinusoidal function----------------------------------------------

def sinusoidal_features(X):
    frequency = 2 * np.pi / (365.25 * 24 * 3600)  # Frequency for one year in seconds
    sinusoidal_X = np.hstack([np.sin(X), np.cos(X)])
    return sinusoidal_X

X_train_sinusoidal = sinusoidal_features(X_train_scaler)
X_test_sinusoidal = sinusoidal_features(X_test_scaler)

lin.fit(X_train_sinusoidal, y_train)

y_pred = lin.predict(X_test_sinusoidal)
y_pred_train = lin.predict(X_train_sinusoidal)
print(mean_absolute_error(y_test, y_pred))
print(mean_absolute_error(y_train, y_pred_train))

#----- Convert Unix timestamps to datetime format for X_test and future_time_points ------------------------

X_test_dates = pd.to_datetime(X_test.flatten(), unit='s')

#----- Estimate the sinusoidal function... --------------------------------------------------------------

def generate_future_time_points(df, num_days, max_date):
    future_dates = pd.date_range(start=X_test_dates.max(), periods=num_days.days, freq='D')
    future_time_points_unix = future_dates.astype(np.int64) // 10**9
    return future_time_points_unix.tolist()

max_date = pd.to_datetime(df['time']).max()
min_date = pd.to_datetime(df['time']).min()
num_days = (X_test_dates.max() - X_test_dates.min())

future_time_points = generate_future_time_points(df, num_days, max_date)
print(future_time_points)

X_future = np.array(future_time_points).reshape(-1, 1)

scaler_future_time_points = scaler.fit_transform(X_future)

X_future_sinusoidal = sinusoidal_features(scaler_future_time_points)

future_predictions = lin.predict(X_future_sinusoidal)
df_predictions = pd.DataFrame({'time': future_time_points, 'pred': future_predictions})
print(df_predictions)

# ----- Get the future real data -----------------------------------------------------------------------------------------------------------------------

query2 = f"""
            SELECT *
            FROM `terra-safe-391718.AIRFLOW.USGS_JPN`
            WHERE time > TIMESTAMP('2020-01-01') AND time < TIMESTAMP('2023-01-01')
            ORDER BY time ASC;
        """
df2 = bq_client.query(query2).to_dataframe()

# Group by date and select the row with the highest 'mag' value for each date
# df2 = df2.loc[df2.groupby(df2['time'].dt.date)['mag'].idxmax()]
df2['timeIndex'] = pd.to_datetime(df2['time'])  # Create a new column 'timeIndex' with the same values as 'time'
df2.set_index('timeIndex', inplace=True)        # Set the new 'timeIndex' column as the DataFrame's index
df2 = df2.resample('W').max()                   # Resample the data by week and take the maximum magnitude value for each week


#----- Plot the predictions for the future time points ------------------------------------------

df_predictions['time'] = pd.to_datetime(df_predictions['time'], unit='s')

plt.figure(figsize=(10, 6))
plt.scatter(X_test_dates, y_test, color='blue', label='Actual Data', s=5)
plt.scatter(X_test_dates, y_pred, color='gray', label='Actual Data', s=5)
plt.scatter(df2['time'], df2['mag'], color='red', label='Future Real Data', s=3)
plt.scatter(df_predictions['time'], df_predictions['pred'], color='green', label='Predicted Future Data', s=5)
plt.xlabel('Time')
plt.ylabel('Magnitude')
plt.title('Sinusoidal Regression Predictions')
plt.legend()
plt.grid(True)
plt.show()
