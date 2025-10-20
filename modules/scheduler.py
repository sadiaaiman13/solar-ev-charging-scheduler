def schedule_charging(solar_forecast, grid_tariffs, ev_need):
    """
    Decide when to charge based on solar output and grid tariffs.
    """
    schedule = []
    for hour, solar_kWh in enumerate(solar_forecast):
        if solar_kWh >= ev_need and grid_tariffs[hour] > 0.15:
            schedule.append((hour, 'Charge from solar'))
        elif grid_tariffs[hour] <= 0.10:
            schedule.append((hour, 'Charge from grid'))
        else:
            schedule.append((hour, 'No charging'))
    return schedule