def rpm_to_radps(x):
    # Lazy import
    from math import pi
    return x * 2*pi / 60


def radps_to_rpm(x):
    # Lazy import
    from math import pi
    return x * 60 / (2 * pi)
