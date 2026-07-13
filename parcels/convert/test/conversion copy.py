"""
/parcels/convert/test/conversion.py
"""






def main(use, **kwargs):
    """."""
    convert = use("@@/convert/convert.py")
    result = convert(1, "km", "m")
    print("result:", result)  ##
    

if __name__ == "__main__":
    from pathlib import Path
    import sys
    # Reboot root to enable import beyond parent
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.resolve()))
    from tools import use

    ##print("use:", use)  ##
    main(use)
