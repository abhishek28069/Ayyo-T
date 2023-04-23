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
