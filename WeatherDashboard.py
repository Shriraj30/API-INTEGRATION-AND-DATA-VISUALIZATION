import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

API_KEY = "e3eb3e7b72d0885f4b8cdfd9d833011f"
API_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Streamlit UI elements
st.title("Weather Dashboard")
city_name = st.text_input("Enter City", "Nashik")

if st.button("Get Weather Data"):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }

    weather_response = requests.get(API_URL, params=params)
    forecast_data = weather_response.json()

    if weather_response.status_code == 200:
        timestamps = []
        temp_values = []
        humidity_levels = []

        for record in forecast_data['list']:
            timestamps.append(datetime.fromtimestamp(record['dt']))
            temp_values.append(record['main']['temp'])
            humidity_levels.append(record['main']['humidity'])

        # Display an animated weather icon
        weather_condition = forecast_data['list'][0]['weather'][0]['main']
        if weather_condition == "Clear":
            st.image("https://openweathermap.org/img/wn/01d.png", width=100)  # Sunny icon
        elif weather_condition == "Clouds":
            st.image("https://openweathermap.org/img/wn/03d.png", width=100)  # Cloudy icon
        else:
            st.image("https://openweathermap.org/img/wn/09d.png", width=100)  # Rainy icon

        # Temperature plot
        st.subheader(f"Temperature Trend in {city_name}")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(timestamps, temp_values, label="Temperature (°C)", color='red', marker='o', linestyle='-')
        ax.set_title(f"Temperature Trend for {city_name}")
        ax.set_xlabel("Date & Time")
        ax.set_ylabel("Temperature (°C)")
        plt.xticks(rotation=45)
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)

        # Humidity plot
        st.subheader(f"Humidity Trend in {city_name}")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(timestamps, humidity_levels, label="Humidity (%)", color='blue', marker='o', linestyle='-')
        ax.set_title(f"Humidity Trend for {city_name}")
        ax.set_xlabel("Date & Time")
        ax.set_ylabel("Humidity (%)")
        plt.xticks(rotation=45)
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
        
    else:
        st.error(f"Error: Unable to fetch weather data. Reason - {forecast_data.get('message', 'Unknown error')}")
