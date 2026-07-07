def main(use, console=None, document=None, js=None, **kwargs):
    ##print("kwargs:", kwargs)  ##

    properties = dict(
        area=dict(
            base="m\u00b2",
            icon="aspect_ratio",
            units=[
                "cm\u00b2",
                "m\u00b2",
                "km\u00b2",
                "inch\u00b2",
                "ft\u00b2",
                "mile\u00b2",
            ],
        ),
        length=dict(
            base="m",
            icon="arrows",
            units=[
                "cm",
                "m",
                "km",
                "inch",
                "ft",
                "mile",
            ],
        ),
    )

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

    def converter(unit):
        def register(converter):
            units[unit] = converter
        return register
    
    @converter('kg')
    def convert(value):
        return value
    
    @converter('g')
    def convert(value):
        return value / 1_000
    
    @converter('pound')
    def convert(value):
        return value / 0.45359237



    def get_converter(unit):
        """."""
        converter = units.get(unit)
        if converter is None:
            raise KeyError(f"No converter for: {unit}")
        return converter


    def to_normal(value, unit):
        """."""
        return get_converter(unit)(value)

    def from_normal(value, unit):
        """."""
        return value/get_converter(unit)(1)





    def convert(from_value: str, from_unit, to_unit):
        """."""
       
      
        return from_normal(to_normal(float(from_value), from_unit), to_unit)


        

    return dict(convert=convert, properties=properties)
