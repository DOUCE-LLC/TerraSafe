#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#------ Import necessary libraries -----------------------------------------------------------------------------------------------------------------------------------------------

import os                                               # Operating system interface
import streamlit as st                                  # Web app framework for creating interactive applications
import pandas as pd                                     # Data manipulation library, used for handling data in tabular format
import numpy as np                                      # Numerical computing library, used for mathematical operations
import matplotlib.pyplot as plt                         # Plotting library for creating data visualizations
from datetime import datetime                           # Date and time manipulation library
from PIL import Image                                   # Python Imaging Library, used for image processing and manipulation

#------ Google Cloud libraries for working with BigQuery -------------------------------------------------------------------------------------------------------------------------------------

from google.cloud import bigquery                       # Client library for accessing BigQuery data
from google.oauth2 import service_account               # Library for handling authentication with Google Cloud services

#------ Scikit-learn libraries for machine learning tasks ----------------------------------------------------------------------------------------------------------------

from sklearn.model_selection import train_test_split    # Splitting data into training and testing sets
from sklearn.preprocessing import StandardScaler        # Standardize features by removing the mean and scaling to unit variance
from sklearn.linear_model import LinearRegression       # Linear regression model
from sklearn.metrics import mean_absolute_error         # Metric for evaluating model performance


#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#------ Set some Functions & variables ----------------------------------------------------------------------------------------------------------------------------------------------------------------


#------ Set Google Cloud ----------------------------------------------------------------------------------------------------------------------------------------------------------------

path = './Streamlit/terrasafe-2-a2b1cdf482ec.json'          # Specify the path to the Google Cloud service account key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path         # Set the environment variable 'GOOGLE_APPLICATION_CREDENTIALS' to the path of the Google Cloud service account key file. This key file is required to authenticate and access Google Cloud services, such as BigQuery.
bq_client = bigquery.Client()                               # Create a BigQuery client with the credentials                                                 

#----- Get the current date ----------------------------------------------------------------------------------------------------------

current_date = datetime.now()                               # Get the current date and time as a datetime object using the 'datetime.now()' function from the 'datetime' module.
formatted_date = current_date.strftime('%Y-%m-%d')          # Format the current date (stored in 'current_date') as a string in the format 'YYYY-MM-DD'. The 'strftime' method is used to convert the datetime object to a string representation with the desired format.

#------ Define function for sinusoidal features --------------------------------------------------------------------------------------

def sinusoidal_features(X):                                 # Function to compute sinusoidal features for the input array X.
    frequency = 2 * np.pi / (365.25 * 24 * 3600)            # Calculate the frequency of one year in seconds. 365.25 days is used to account for leap years.
    sinusoidal_X = np.hstack([np.sin(X), np.cos(X)])        # Compute the sinusoidal features for the input array X. The sinusoidal features are obtained by stacking the sine and cosine values of each element in X.
    return sinusoidal_X                                     # Return the array containing the computed sinusoidal features.

#------ Define function for generating future sinusoidal features --------------------------------------------------------------------------------------------------------------------------------------------------------------------

def generate_future_sinusoidal_features(X, num_days):                                               # Function to generate future sinusoidal features based on the input array X and the number of days to predict (num_days).
    frequency = 2 * np.pi / (365.25 * 24 * 3600)                                                    # Calculate the frequency of one year in seconds. 365.25 days is used to account for leap years.
    future_X = X[-1] + np.arange(1, num_days + 1) * 24 * 3600                                       # Generate future time points in seconds.
    future_sinusoidal_X = np.hstack([np.sin(frequency * future_X), np.cos(frequency * future_X)])   # Compute the future sinusoidal features for the generated future time points. The future sinusoidal features are obtained by stacking the sine and cosine values of each future time point, multiplied by the calculated frequency.
    return future_sinusoidal_X                                                                      # Return the array containing the computed future sinusoidal features.

#------ Function to execute the query and get the data -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def execute_query(selected_table):              # Function to execute a query on BigQuery and retrieve the data for the specified 'selected_table'.
    query = f"""
                SELECT *
                FROM `terrasafe-2.AIRFLOW.{selected_table}`
                WHERE time > TIMESTAMP('2020-01-01') AND time < TIMESTAMP('{formatted_date}') AND mag > 2.5
                ORDER BY time ASC;
            """                                 # Construct the SQL query as a string using a formatted query with the 'selected_table' parameter and 'formatted_date'.
    df = bq_client.query(query).to_dataframe()  # Execute the constructed query using the BigQuery client ('bq_client') and convert the result to a pandas DataFrame ('df').
    return df                                   # Return the DataFrame containing the retrieved data from the BigQuery table.

#------------------ Function to generate future time points ----------------------------------------------------------------------------------------

def generate_future_time_points(num_days, max_date):                            # Function to generate future time points based on the number of days and the maximum date.
    future_dates = pd.date_range(start=max_date, periods=num_days, freq='D')    # Generate future dates starting from the 'max_date' with 'num_days' periods and a daily frequency ('freq='D''). The 'pd.date_range' function creates a DatetimeIndex containing future dates based on the specified parameters.
    return future_dates.tolist()                                                # Return the list of future dates converted to a Python list. The 'tolist()' method converts the DatetimeIndex to a list of Python datetime objects.

#-------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------
#------ Streamlit Function for the website -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def Sinusoidal():

#------ Display the title, introductory text, Imgs ------------------------------------------------------------------------------------------------------------------------------

    st.title('TerraSafe - Sinusoidal Regression')                                           # Set the title of the web application to 'TerraSafe - Sinusoidal Regression'.
    st.write("While you wait for the model to run the predictions, you can watch this amazing recap of the model's performance over the last 3 years...")
    image = Image.open("./Img/Senuidal.png")                                                # Open and load an image from the specified path './Img/Senuidal.png'.
    st.image(image, caption="Japan: 2020-2022", use_column_width=True)                      # Display the loaded image with an optional caption "Japan: 2020-2022". 'use_column_width=True' allows the image to be displayed with the width of the column in the application.

#------ Create a selector for the table choice -------------------------------------------------------------------------------------------------------------------------------

    selected_table = st.selectbox("Select a table:", ["USGS_JPN", "USGS_CHI", "USGS_USA"])  # Create a selector for the table choice

#------ Execute query and predict button ---------------------------------------------------------------------------------------------------------------------------------------

    if st.button("Execute Query and Predict"):                  # Check if the user clicks the "Execute Query and Predict" button.
        df = execute_query(selected_table)                      # If the button is clicked, execute the query and prediction function ('execute_query') for the selected table. The result is stored in the 'df' variable, which will contain the retrieved data from the selected table.

#------ Group by date and select the row with the highest 'mag' value for each date -------------------------------------------------------------------------

        df['timeIndex'] = pd.to_datetime(df['time'])            # Create a new column 'timeIndex' with the same values as 'time'
        df.set_index('timeIndex', inplace=True)                 # Set the new 'timeIndex' column as the DataFrame's index
        df = df.resample('W').max()                             # Resample the data by week and take the maximum magnitude value for each week

#------ Train the model -------------------------------------------------------------------------------------------------------------------

        df['time'] = df['time'].apply(lambda x: int(datetime.timestamp(x)))         # Convert the 'time' column in the DataFrame 'df' to Unix timestamps (integer representation of the time in seconds since epoch). The 'lambda x: int(datetime.timestamp(x))' is a lambda function applied to each element of the 'time' column to convert it to Unix timestamps.
        X = df['time'].values.reshape(-1, 1)                                        # Extract the 'time' column from the DataFrame 'df' and reshape it into a 2D array with one column and as many rows as the DataFrame has. The 'X' variable will be used as the input feature for the model.
        y = df['mag'].values                                                        # Extract the 'mag' column from the DataFrame 'df'. The 'y' variable will be used as the target variable for the model.
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.9, random_state=1) # Split the data into training and testing sets using the 'train_test_split' function from scikit-learn. The data is split such that 90% is used for training ('X_train' and 'y_train') and 10% for testing ('X_test' and 'y_test'). The 'random_state=1' ensures reproducibility of the split.
        
        scaler = StandardScaler()                                                   # Create a StandardScaler object from scikit-learn. StandardScaler is used to standardize features by removing the mean and scaling to unit variance.
        X_train_scaler = scaler.fit_transform(X_train)                              # Standardize the training data features ('X_train') using the 'fit_transform' method of the scaler object. This computes the mean and standard deviation of the training data and applies the transformation.
        X_test_scaler = scaler.transform(X_test)                                    # Standardize the testing data features ('X_test') using the 'transform' method of the scaler object. This applies the same transformation as used for the training data, based on the mean and standard deviation computed during training.
        
        lin = LinearRegression()                                                    # Create a LinearRegression object from scikit-learn. Linear regression is a machine learning algorithm used for modeling the relationship between a dependent variable and one or more independent variables.
        X_train_sinusoidal = sinusoidal_features(X_train_scaler)                    # Compute the sinusoidal features for the standardized training data ('X_train_scaler') using the 'sinusoidal_features' function.
        X_test_sinusoidal = sinusoidal_features(X_test_scaler)                      # Compute the sinusoidal features for the standardized testing data ('X_test_scaler') using the 'sinusoidal_features' function.
        
        lin.fit(X_train_sinusoidal, y_train)                                        # Train the linear regression model using the training data with sinusoidal features ('X_train_sinusoidal') and the target variable ('y_train').
        y_pred = lin.predict(X_test_sinusoidal)                                     # Make predictions on the testing data using the trained model ('lin') and the sinusoidal features of the testing data ('X_test_sinusoidal'). The predicted values are stored in the 'y_pred' variable.
        y_pred_train = lin.predict(X_train_sinusoidal)                              # Make predictions on the training data using the trained model ('lin') and the sinusoidal features of the training data ('X_train_sinusoidal'). The predicted values are stored in the 'y_pred_train' variable.

#------ Future predictions ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        X_test_dates = pd.to_datetime(X_test.flatten(), unit='s')                                   # Convert the flattened testing data ('X_test') from Unix timestamps to pandas datetime objects using the 'pd.to_datetime' function. The 'unit='s'' argument specifies that the input is in seconds.
        num_days = (pd.to_datetime('2023-01-01') - pd.to_datetime('2020-01-01')).days               # Calculate the number of days between '2020-01-01' and '2023-01-01' using the 'pd.to_datetime' function and the '.days' attribute. The result is stored in the 'num_days' variable.
        X_future_sinusoidal = generate_future_sinusoidal_features(X, num_days)                      # Generate future sinusoidal features based on the input array 'X' and the calculated 'num_days' using the 'generate_future_sinusoidal_features' function.
        X_future_sinusoidal = X_future_sinusoidal.reshape(-1, 2)                                    # Reshape the 'X_future_sinusoidal' array to have two columns (features) and as many rows as required. This step ensures the data has the correct shape for future predictions.
        future_predictions = lin.predict(X_future_sinusoidal)                                       # Use the trained linear regression model ('lin') to predict the target variable for the future sinusoidal features ('X_future_sinusoidal'). The predicted values are stored in the 'future_predictions' variable.
        future_time_points = pd.date_range(start=df.index[0] + pd.Timedelta(days=7), periods=num_days, freq='W') # Generate future time points starting from the first date in the DataFrame 'df' plus 7 days using the 'pd.date_range' function. The 'num_days' parameter specifies the number of future time points, and the 'freq='W'' argument sets the frequency to weekly.
        df_predictions = pd.DataFrame({'time': future_time_points, 'pred': future_predictions})     # Create a new DataFrame 'df_predictions' containing the 'time' and 'pred' columns. 'time' contains the future time points, and 'pred' contains the corresponding predicted values.
        future_time_points_unix = generate_future_time_points(num_days, formatted_date)             # Generate a list of future time points in Unix timestamps format using the 'generate_future_time_points' function.
        empty_y_values = [5] * len(future_time_points_unix)                                         # Create an empty array filled with the value 5 for the Y-axis data of the predicted future points. This step is used to create a placeholder for the predicted data to be plotted later.

#------ Create the figure and axes separately ------------------------------------------------------------------------------------------

        fig = plt.figure(figsize=(10, 6), facecolor='black')                # Create a new matplotlib figure with a size of 10x6 inches and a black background ('facecolor='black''). The 'fig' variable will hold the reference to the created figure.
        ax = fig.add_subplot(111)                                           # Add a subplot (axes) to the figure with a single plot at position 1, 1, 1 (1 row, 1 column, 1st position). The 'ax' variable will hold the reference to the created subplot (axes).
        ax.set_facecolor('black')                                           # Set the facecolor (background color) of the subplot to black to match the overall dark theme of the plot.

#------ Scatter plots with white edgecolor to hide the points' outlines ------------------------------------------------------------------------

        ax.scatter(X_test_dates, y_test, color='blue', label='Real Data', s=10)                 # Create a scatter plot on the subplot ('ax') for the real data points. The 'X_test_dates' represents the x-axis values, and 'y_test' represents the y-axis values. The 'color='blue'' sets the data points' color to blue, and 'label='Real Data'' provides a label for the legend. The 's=10' sets the size of the data points to 10.
        ax.scatter(X_test_dates, y_pred, color='green', label='Predicted Future Data', s=10)    # Create a scatter plot on the subplot ('ax') for the predicted future data points. The 'X_test_dates' represents the x-axis values, and 'y_pred' represents the y-axis values. The 'color='green'' sets the data points' color to green, and 'label='Predicted Future Data'' provides a label for the legend. The 's=10' sets the size of the data points to 10.
        ax.scatter(future_time_points_unix, empty_y_values, color='gray', label='', s=1)        # Create a scatter plot on the subplot ('ax') with an empty array for the y-axis values ('empty_y_values') to create vertical lines on the plot. The 'future_time_points_unix' represents the x-axis values for the predicted future data points. The 'color='gray'' sets the color of the vertical lines to gray, and 'label='' sets no label for these points in the legend. The 's=1' sets the size of the vertical lines to 1, making them almost invisible.

#------ Set the text color for the axes and title ----------------------------------------------------------------------------------------

        ax.set_xlabel('Time', color='white')                                # Set the x-axis label of the subplot ('ax') to 'Time' with white color text. This provides a label for the x-axis indicating the time dimension.
        ax.set_ylabel('Magnitude', color='white')                           # Set the y-axis label of the subplot ('ax') to 'Magnitude' with white color text.  This provides a label for the y-axis indicating the magnitude dimension.
        ax.set_title('Sinusoidal Regression Predictions', color='white')    # Set the title of the subplot ('ax') to 'Sinusoidal Regression Predictions' with white color text. This provides a title for the plot indicating the nature of the predictions.

#------ Set the legend text color and background color --------------------------------------------------------------------------------------

        legend = ax.legend()                                                # Get the legend associated with the subplot ('ax'). The legend will contain labels for the different data series (real data and predicted future data).
        legend.get_frame().set_facecolor('black')                           # Set the facecolor (background color) of the legend to black to match the overall dark theme of the plot.
        legend.get_frame().set_edgecolor('white')                           # Set the edgecolor (border color) of the legend to white to provide a visible border around the legend.
        
        for text in legend.get_texts():                                     # Loop through each text label in the legend and set their color to white. This makes the legend text visible against the black background.
            text.set_color('white')

#------ Set the tick colors and grid lines --------------------------------------------------------------------------------------------------

        ax.tick_params(axis='x', colors='white')                            # Set the tick color of the x-axis to white, making the x-axis tick marks visible against the black background.
        ax.tick_params(axis='y', colors='white')                            # Set the tick color of the y-axis to white, making the y-axis tick marks visible against the black background.
        ax.grid(True, color='white')                                        # Add gridlines to the subplot ('ax') with white color. This provides gridlines to help visualize the data points' positions and their relationships.

#------ Display the plot in Streamlit -----------------------------------------------------------------------------------------------------

        st.pyplot(fig)                                                      # Display the plot (figure) created with matplotlib in Streamlit. The 'fig' variable holds the reference to the figure, and Streamlit renders the plot within the web application.

#----- Example of Sinusoidal Function -------------------------------------------------------------------------------------------------------------------------------------

    image = Image.open("./Img/Fx_Sin.png")                                  # Open and load an image from the specified path './Img/Fx_Sin.png'.
    st.image(image, caption="Example", use_column_width=True)               # Display the loaded image with an optional caption "Example". 'use_column_width=True' allows the image to be displayed with the width of the column in the application.

### Matias Aguilar