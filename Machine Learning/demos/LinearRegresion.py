# import streamlit as st
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
from sklearn.preprocessing import PolynomialFeatures 
from sklearn.metrics import mean_absolute_error

# Título de la página de inicio
# st.title('TerraSafe - Polynomial Regression')

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
df = df.loc[df.groupby(df['time'].dt.date)['mag'].idxmax()]

print(df)

df['time'] = df['time'].apply(lambda x: int(datetime.timestamp(x)))

X = df['time'].values.reshape(-1, 1)
y = df['mag'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state = 1)

scaler = StandardScaler()
X_train_scaler = scaler.fit_transform(X_train)
X_test_scaler = scaler.transform(X_test)

lin = LinearRegression()

poly = PolynomialFeatures(degree=10)
X_poly_train = poly.fit_transform(X_train_scaler)
X_test_poly = poly.transform(X_test_scaler)
poly.fit(X_poly_train, y_train)
lin.fit(X_poly_train, y_train)

y_pred = lin.predict(X_test_poly)
y_pred_train = lin.predict(X_poly_train)
print(mean_absolute_error(y_test, y_pred))
print(mean_absolute_error(y_train, y_pred_train))

#----- Convert Unix timestamps to datetime format for X_test and future_time_points ------------------------------------------------------------------------

X_test_dates = pd.to_datetime(X_test.flatten(), unit='s')

#----- Estimate the polynomial function... ------------------------------------------------------------------------------------------------------------------------

# x_values = X_test[:, 0]                                     # Extract 'x'
# y_values = y_test                                           # Extract 'y'
# degree = 5                                                  # Degree of the polynomial
# coefficients = np.polyfit(x_values, y_values, degree)       # Fit the polynomial using polyfit
# polynomial_func = np.poly1d(coefficients)                   # Create the polynomial function based on the coefficients
# print("\n", polynomial_func)                                # Print the estimated polynomial function

#----- Future x points Function() ---------------------------------------------------------------------------------------------------------------------------------------

def generate_future_time_points(df, num_days, max_date):
    future_dates = pd.date_range(start=X_test_dates.max(), periods=num_days.days, freq='D')        # Generate a range of dates with daily intervals from the future date
    future_time_points_unix = future_dates.astype(np.int64) // 10**9                # Convert future dates to Unix timestamp format
    return future_time_points_unix.tolist()                                         # Return dates

max_date = pd.to_datetime(df['time']).max()                                         # Find the maximum date in df['time']
min_date = pd.to_datetime(df['time']).min()                                         # Find the minimum date in df['time']
num_days = (X_test_dates.max() - X_test_dates.min())

future_time_points = generate_future_time_points(df, num_days, max_date)
print(future_time_points)

X_future = np.array(future_time_points).reshape(-1, 1)

scaler_future_time_points = scaler.fit_transform(X_future)

poly_future_time_points = poly.fit_transform(X_future)
future_predictions = lin.predict(poly_future_time_points)
df_predictions = pd.DataFrame({'time': future_time_points, 'pred': future_predictions})
print(df_predictions)

#----- Get the prediction with the polynomial function... ---------------------------------------------------------------------------------------------------

# df_future = pd.DataFrame({                                      # Adjust the dates by adding the offset
#     'time': pd.to_datetime(future_time_points, unit='s'),
#     'mag': polynomial_func(future_time_points)
# })
# print(df_future)

#----- Get the future real data -----------------------------------------------------------------------------------------------------------------------

# query2 = f"""
#             SELECT *
#             FROM `terra-safe-391718.AIRFLOW.USGS_JPN`
#             WHERE time > TIMESTAMP('2020-01-01') AND time < TIMESTAMP('2023-01-01')
#             ORDER BY time ASC;
#         """
# df2 = bq_client.query(query2).to_dataframe()

# # Group by date and select the row with the highest 'mag' value for each date
# df2 = df2.loc[df2.groupby(df2['time'].dt.date)['mag'].idxmax()]

# #----- Plot the predictions for the future time points ------------------------------------------------------------------------------------------------

# plt.figure(figsize=(10, 6))
# plt.scatter(X_test_dates, y_test, color='blue', label='Actual Data', s=5)
# plt.scatter(X_test_dates, y_pred, color='gray', label='Actual Data', s=5)
# plt.scatter(df2['time'], df2['mag'], color='red', label='Future Real Data', s=3)
# plt.scatter(df_future['time'], df_future['mag'], color='green', label='Predicted Future Data', s=5)
# plt.xlabel('Time')
# plt.ylabel('Magnitude')
# plt.title('Polynomial Regression Predictions')
# plt.legend()
# plt.grid(True)
# plt.show()