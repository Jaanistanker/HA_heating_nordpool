# HA_heating_nordpool
Home Assistant automation for heating the house and jacuzzi

Explanation:
Trigger: The py automation runs hourly.
Variables Calculation: It calculates the combined prices for the next 24 hours using the raw_today data from nordpool, including the transfer price based on the time and whether it's a weekend or holiday.
Then it sorts out the top8 and low8 hours and sets the boolean helpers top_boolean_state and bottom_boolean to on or of state for current hour. The automation then sets the temperature and curve values hourly. In addition to this, there is a bypass possibility in Lovelace to be able to adjust the temp when away from home or if something goes wrong with the automation.
Ideally, top8 hours should be no heating, low8 should be 20+2 degrees and other 8 hours normal 20C. 

Jacuzzi part is still tbd
