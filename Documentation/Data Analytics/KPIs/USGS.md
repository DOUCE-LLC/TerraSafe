# Worldwide Earthquake Information 🌍📊

Welcome to the worldwide earthquake analysis! Here, you'll find a fun and formal description of each of the potential KPIs to be calculated based on USGS's CSV data files.

## Required Columns

Before we dive into the KPIs, the CSV files contain the following columns:

- `time`: Records the date and time of the earthquake.
- `latitude`: Latitude coordinate of the earthquake.
- `longitude`: Longitude coordinate of the earthquake.
- `depth`: Depth of the earthquake beneath the ground.
- `mag`: Magnitude of the earthquake on a scale from 1 to 10.
- `dmin`: Kilometers around affected by the earthquake.
- `id`: Unique identifier of the earthquake.
- `place`: Location of the earthquake.
- `type`: Type of seismic event (earthquake or tremor).

Now, let's get to the KPIs!

## 1. Total Number of Recorded Earthquakes 📉

This KPI provides you with the total count of earthquakes in the file.

Required Columns: `id`

## 2. Average Magnitude of Earthquakes 📏

Calculate the average magnitude of all recorded earthquakes.

Required Columns: `mag`

## 3. Percentage of High-Magnitude Earthquakes ⚡️

This KPI shows you the percentage of earthquakes that had a magnitude greater than 7 on a scale from 1 to 10.

Required Columns: `mag`

## 4. Geographical Distribution of Earthquakes 🗺️

Analyze the geographical distribution of earthquakes and show which continents or regions are most affected.

Required Columns: `latitude`, `longitude`

## 5. Number of Earthquakes by Type 🌪️

Calculate the number of earthquakes and tremors in the file to get an overview of seismic events.

Required Columns: `type`

## 6. Average Depth of Earthquakes 🌌

This KPI provides you with the average depth of recorded earthquakes.

Required Columns: `depth`

## 7. Top 5 Most Affected Places by Earthquakes 🏞️

Identify the five most affected places by earthquakes and display their frequency.

Required Columns: `place`

## 8. Magnitude Variation of Earthquakes Over Time 📈

Analyze the variation in earthquake magnitudes over time to identify trends or patterns.

Required Columns: `time`, `mag`

## 9. Relationship Between Magnitude and Depth of Earthquakes 🔍

Study the relationship between the magnitude and depth of earthquakes to determine if any correlation exists.

Required Columns: `mag`, `depth`

## 10. Percentage of Earthquakes that Affected a Significant Distance 📍

Calculate the percentage of earthquakes that affected a distance greater than 100 km compared to the total distance covered by all earthquakes.

Required Columns: `dmin`

Have fun exploring these KPIs and discover interesting insights about earthquakes worldwide!

Remember to adjust the instructions according to the specific needs of your data and analysis. Happy analyzing! 🚀🔍