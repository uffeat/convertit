units = {
    # Area
    "cm\u00b2": lambda v: v / (100**2),
    "m\u00b2": lambda v: v,
    "km\u00b2": lambda v: v * (100**2),
    "inch\u00b2": lambda v: v * (0.0254**2),
    "ft\u00b2": lambda v: v * (0.3048**2),
    "mile\u00b2": lambda v: v / v * (1_609.344**2),
    # Length
    "cm": lambda v: v / 100,
    "m": lambda v: v,
    "km": lambda v: v * 1_000,
    "inch": lambda v: v * 0.0254,
    "ft": lambda v: v * 0.3048,
    "mile": lambda v: v * 1_609.344,
}

def get_converter(unit):
    """."""
    converter = units.get(unit)
    if converter is None:
        raise KeyError(f"No converter for: {unit}")
    return converter


def to_normal(value, unit):
    """."""
    normal = get_converter(unit)(value)
    return normal

def from_normal(value, unit):
    """."""
    scale = get_converter(unit)(1)
    return value/scale





def convert(from_value, from_unit, to_unit):
    """."""
    normal = to_normal(from_value, from_unit)
    return from_normal(normal, to_unit)


    


   

print('Result:', convert(1, "m", 'cm'))