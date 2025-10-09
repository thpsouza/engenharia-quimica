## Sistema métrico:
def cm3_to_m3(x):
    return x * 1e-6


def cm3_to_L(x):
    return x * 1e-3


def m3_to_cm3(x):
    return x * 1e6


def m3_to_L(x):
    return x * 1e3


def L_to_cm3(x):
    return x * 1e3


def L_to_m3(x):
    return x * 1e-3


## Sistema inglês
def in3_to_ft3(x):
    return x / 1728


def ft3_to_in3(x):
    return x * 1728


## Conversão entre sistemas
def in3_to_cm3(x):
    return x / 1728


def ft3_to_m3(x):
    return x * 1728 * 16.387064 * 1e-6


def m3_to_ft3(x):
    return x / (1728 * 16.387064) * 1e6
