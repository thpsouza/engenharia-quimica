def celsius_to_kelvin(x):
    return x + 273.15


def celsius_to_fahrenheit(x):
    return x * 9/5 + 32


def kelvin_to_celsius(x):
    return x - 273.15


def kelvin_to_fahrenheit(x):
    return (x - 273.15) * 9/5 + 32


def fahrenheit_to_celsius(x):
    return 5/9 * (x-32)


def fahrenheit_to_kelvin(x):
    return 5/9 * (x-32) + 273.15
