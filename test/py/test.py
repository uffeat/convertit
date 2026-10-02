"""
test/py/test.py
"""


def main(
    use, Base=None, log: callable = None, test: callable = None, **kwargs
) -> callable:
    """."""
    Py = use("use/use/py.py")


    ##text = test('test/py/ping.py', text=True)
    ##log("text:", text)  ##
   

    ##use("use/_test/ping.test.py")
    parcel = use.get("use/_test/ping.test.py")
    ##parcel = {k: v for k, v in use.get("use/_test/ping.test.py").items() if k != "text"}
    ##log("parcel:", parcel)  ##
    log("meta:", parcel.get('meta'))  ##
