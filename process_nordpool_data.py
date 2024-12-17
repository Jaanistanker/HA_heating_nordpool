def process_nordpool_data(hass):
    # Ensure the sensor exists and get the raw data
    nordpool_sensor = hass.states.get('sensor.nordpool_kwh_ee_eur_6_05_022')
    if nordpool_sensor is None:
        hass.states.set('sensor.debug_nordpool', 'Nordpool sensor not found')
        return  # Exit if sensor doesn't exist

    raw_today = nordpool_sensor.attributes.get('raw_today')
    if not raw_today:
        hass.states.set('sensor.debug_nordpool', 'No raw data found')
        return

    # Calculate adjusted prices
    adjusted_prices = []
    for item in raw_today:
        if item.get('start') and item.get('value') is not None:
            hour = item['start'].hour  # Get the hour from the timestamp
            weekday_sensor = hass.states.get('sensor.weekday')
            if weekday_sensor is None or weekday_sensor.state == 'unknown':
                hass.states.set('sensor.debug_nordpool', 'Weekday sensor not found or state is unknown')
                return

            weekday = int(weekday_sensor.state)
            transfer_cost = 0.0428 if hour >= 22 or hour < 7 or weekday >= 5 or not hass.states.is_state('binary_sensor.workday_sensor', 'on') else 0.0741
            adjusted_price = item['value'] + transfer_cost
            adjusted_prices.append({'hour': hour, 'value': adjusted_price})

    # Sort the prices in descending order to get the top 8 and bottom 8 hours
    sorted_prices = sorted(adjusted_prices, key=lambda x: x['value'], reverse=True)
    top_8_hours = [entry['hour'] for entry in sorted_prices[:8]]
    bottom_8_hours = [entry['hour'] for entry in sorted_prices[-8:]]

    # Get the current hour
    time_sensor = hass.states.get('sensor.time_date')
    if time_sensor is None:
        hass.states.set('sensor.debug_nordpool', 'Time sensor not found')
        return

    current_hour = int(time_sensor.state.split(':')[0])

    # Check if the current hour is in the top or bottom 8 hours
    top_boolean_state = 'on' if current_hour in top_8_hours else 'off'
    bottom_boolean_state = 'on' if current_hour in bottom_8_hours else 'off'

    # Update the state of the input_booleans
    hass.states.set('input_boolean.nordpool_top8_hours', top_boolean_state)
    hass.states.set('input_boolean.nordpool_bottom8_hours', bottom_boolean_state)

    # Set debug information
    debug_info = f'Top: {top_boolean_state}, Bottom: {bottom_boolean_state}, Top8: {top_8_hours}, Low8 {bottom_8_hours}'
    hass.states.set('sensor.debug_nordpool', debug_info)

# Ensure the function is called
process_nordpool_data(hass)
