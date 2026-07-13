"""
/parcels/convert/test/conversion.py
"""






def main(use, **kwargs):
    """."""
    convert = use("@@/convert/convert.py")
    result = convert(1, "km", "m")
    print("result:", result)  ##
    

if __name__ == "__main__":
    from utils import use

    ##print("use:", use)  ##
    main(use)
