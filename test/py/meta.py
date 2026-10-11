def main(
    use, Base=None, log: callable = None, test: callable = None, **kwargs
) -> callable:
    """test/py/meta.py"""

    parcel = use.get("use/test/ping.test.py")

    log("meta:", parcel.get("meta"))  ##
