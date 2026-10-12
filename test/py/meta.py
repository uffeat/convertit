def main(
    use, Base=None, log: callable = None, test: callable = None, **kwargs
) -> callable:
    """test/py/meta.py"""

    meta = use.get("use/test/ping.test.py", "meta")

    log("meta:", meta)  ##
