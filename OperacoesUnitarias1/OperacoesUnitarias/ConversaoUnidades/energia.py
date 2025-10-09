def joule_to_kwh(x):
    return x / (3.6 * 1e6)


def joule_to_kcal(x):
    return x / 4184


def kwh_to_joule(x):
    return x * 3.6 * 1e6


def kwh_to_kcal(x):
    return x * 860


def kcal_to_kwh(x):
    return x / 860


def kcal_to_joule(x):
    return x * 4184
