# HA_heating_nordpool
Home Assistant automation for heating the house and jacuzzi

Explanation:
Trigger: The automation runs daily at 00:01
Variables Calculation: It calculates the combined prices for the next 24 hours using the raw_today data from nordpool, including the transfer price based on the time and whether it's a weekend or holiday.
MQTT Publish: It publishes the calculated hour_adjustment for each hour to the home/temperature/CurveL topic.
This approach ensures that the heating is adjusted based on the prices for the upcoming 24 hours, taking into account the transfer prices and the time of day and then fed into heatpump MQTT hourly.
