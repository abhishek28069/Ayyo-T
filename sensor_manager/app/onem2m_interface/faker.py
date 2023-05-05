import random


# celsius
def generate_fake_temperature():
    # Define the temperature range and precision
    MIN_TEMP = -20
    MAX_TEMP = 40
    PRECISION = 0.1

    # Generate a random temperature value
    temperature = round(random.uniform(MIN_TEMP, MAX_TEMP), int(abs(PRECISION)))

    # Return the temperature value
    return temperature


# percent
def generate_fake_humidity():
    # Define the humidity range and precision
    MIN_HUMIDITY = 0
    MAX_HUMIDITY = 100
    PRECISION = 0.1

    # Generate a random humidity value
    humidity = round(random.uniform(MIN_HUMIDITY, MAX_HUMIDITY), int(abs(PRECISION)))

    # Return the humidity value
    return humidity


# lux
def generate_fake_luminosity():
    # Define the luminosity range and precision
    MIN_LUMINOSITY = 0
    MAX_LUMINOSITY = 1000
    PRECISION = 1

    # Generate a random luminosity value
    luminosity = round(
        random.uniform(MIN_LUMINOSITY, MAX_LUMINOSITY), int(abs(PRECISION))
    )

    # Return the luminosity value
    return luminosity


# kilowatt-hour
def generate_fake_electricity_consumption():
    # Define the electricity consumption range and precision
    MIN_CONSUMPTION = 0
    MAX_CONSUMPTION = 1000
    PRECISION = 1

    # Generate a random electricity consumption value
    consumption = round(
        random.uniform(MIN_CONSUMPTION, MAX_CONSUMPTION), int(abs(PRECISION))
    )

    # Return the electricity consumption value
    return consumption


def generate_fake_presence():
    # Generate a random occupancy sensor value
    is_occupied = random.choice([1, 0])

    # Return the occupancy sensor value
    return is_occupied


def generate_fake_lamp_clicks():
    # Generate a random lamp value
    is_occupied = random.choice([1, 0])

    # Return the lamp value
    return is_occupied


def generate_fake_buzzer():
    # Generate a random occupancy sensor value
    is_occupied = random.choice([1, 0])

    # Return the occupancy sensor value
    return is_occupied

# Generate solar energy generation data kWh
def generate_fake_solar_energy():
    # Define the solar energy generation range and precision
    MIN_ENERGY = 0
    MAX_ENERGY = 1000
    PRECISION = 1

    # Generate a random solar energy generation value
    energy = round(
        random.uniform(MIN_ENERGY, MAX_ENERGY), int(abs(PRECISION))
    )
    # Return the solar energy generation value
    return energy

# Generate air quality data ppm
def generate_fake_air_quality():
    # Define the air quality range and precision
    MIN_AIR_QUALITY = 0
    MAX_AIR_QUALITY = 500
    PRECISION = 1

    # Generate a random air quality value
    air_quality = round(
        random.uniform(MIN_AIR_QUALITY, MAX_AIR_QUALITY), int(abs(PRECISION))
    )

    # Return the air quality value
    return air_quality