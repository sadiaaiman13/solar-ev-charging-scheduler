def estimate_ev_energy_usage(daily_km, efficiency_kWh_per_km=0.2):
    """
    Estimate daily energy usage based on distance driven.
    """
    return daily_km * efficiency_kWh_per_km

def battery_status(current_charge, usage_kWh, battery_capacity=60):
    """
    Calculate remaining battery after usage and how much needs recharging.
    """
    new_charge = max(0, current_charge - usage_kWh)
    recharge_needed = battery_capacity - new_charge
    return new_charge, recharge_needed