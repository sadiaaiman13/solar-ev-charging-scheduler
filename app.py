import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from modules.solar_api import get_solar_forecast
from modules.ev_model import estimate_ev_energy_usage
from modules.scheduler import schedule_charging

st.title("🔋 Smart Solar EV Charging Scheduler")

# Inputs
api_key = st.text_input("Enter your NREL API Key")
lat = st.number_input("Latitude", value=28.0)
lon = st.number_input("Longitude", value=77.0)
daily_km = st.slider("Daily EV Usage (km)", 0, 100, 40)
simulate = st.checkbox("Use simulated solar data")

if api_key or simulate:
    # Get solar forecast
    solar = get_solar_forecast(api_key, lat, lon, simulate=simulate)
    ev_need = estimate_ev_energy_usage(daily_km)
    grid_tariffs = [0.12 + 0.05 * (i % 4) for i in range(24)]  # Simulated hourly tariffs
    schedule = schedule_charging(solar, grid_tariffs, ev_need)

    # Debug info
    st.write(f"🔌 EV energy need: {ev_need:.2f} kWh")
    st.write(f"☀️ Total solar available: {sum(solar):.2f} kWh")

    # Charging schedule
    st.subheader("Charging Schedule")
    for hour, action in schedule:
        st.write(f"{hour}:00 → {action}")

    # Plot solar output and charging decisions
    fig, ax = plt.subplots(figsize=(10, 4))
    hours = list(range(24))
    actions = [1 if "Charge" in act else 0 for _, act in schedule]

    ax.plot(hours, solar, label="Solar Output (kWh)", color="orange")
    ax.step(hours, actions, label="Charging Decision", color="blue", where='mid')
    ax.set_ylim(-0.1, 1.1)
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Energy / Decision")
    ax.set_title("Solar Output vs Charging Schedule")
    ax.legend()

    st.pyplot(fig)