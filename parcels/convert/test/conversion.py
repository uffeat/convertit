"""
/parcels/convert/test/conversion.py
"""


def main(use, **kwargs):
    """."""
    convert = use("@@/convert/convert.py")
    result = convert(1, "km", "m")
    print("result:", result)  ##



try:
    from utils import use
    main(use)
except:
    pass