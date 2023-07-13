import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

color_pal = sns.color_palette()
plt.style.use('fivethirtyeight')

df = pd.read_csv('./jpn - USGS_JPN.csv')

# df.plot(style='.',
#         figsize=(15, 5),
#         color=color_pal[0],
#         title='Función ciclica')
# plt.show()

# train, test = train_test_split(df, test_size=0.2, random_state=42)

split_index = int(len(df) * 0.8)  # Calculate the index to split the data
train = df.iloc[:split_index]  # Select the rows up to the split index
test = df.iloc[split_index:]  # Select the rows from the split index onwards

fig, ax = plt.subplots(figsize=(15, 5))
train.plot(ax=ax, label='Training Set', title='Data Train/Test Split')
test.plot(ax=ax, label='Test Set')
ax.axvline('01-01-2023', color='black', ls='--')
ax.legend(['Training Set', 'Test Set'])
plt.show()

# Train the model

FEATURES = ['time','cdi','mmi','dmin','place','earthquakeType','sig','tsunami','longitude','latitude','depth']
TARGET = 'mag'

X_train = pd.to_numeric(train[FEATURES].index).values.reshape(-1, 1)
y_train = train[TARGET]

X_test = pd.to_numeric(test[FEATURES].index).values.reshape(-1, 1)
y_test = test[TARGET]

reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',
                       n_estimators=1000,
                       early_stopping_rounds=50,
                       objective='reg:squarederror',
                       max_depth=5,
                       learning_rate=0.1)
reg.fit(X_train, y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        verbose=100)

# Predictions

test['prediction'] = reg.predict(X_test)
df = df.merge(test[['prediction']], how='left', left_index=True, right_index=True)
# ax = df[['mag']].head(100).plot(figsize=(15, 5))  # Select the first 100 records
# df['prediction'].head(100).plot(ax=ax, style='.')  # Select the first 100 records
ax = df[['mag']].plot(figsize=(15, 5))  # Select the first 100 records
df['prediction'].plot(ax=ax, style='.')  # Select the first 100 records

plt.legend(['Truth Data', 'Predictions'])
ax.set_title('Raw Data and Prediction')
plt.show()

# Score RMSE

score = np.sqrt(mean_squared_error(test['mag'], test['prediction']))
print(f'RMSE Score on Test set: {score:0.2f}')

# Calculate Error

test['error'] = np.abs(test[TARGET] - test['prediction'])
test['date'] = test['time']
test.groupby(['date'])['error'].mean().sort_values(ascending=True).head(10)