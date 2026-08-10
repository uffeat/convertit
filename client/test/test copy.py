def main(
    use,
    Base=None,
    Path=None,
    anvil=None,
    console=None,
    document=None,
    js=None,
    log=None,
    meta=None,
    window=None,
    **kwargs,
):
    """."""


    ping = use("/ping.py")
    print("ping:", ping())







    ping = use("/ping.py")
    print("ping:", ping())

    ping = use("/ping.py")
    print("ping:", ping())

    raw = use("/ping.py", text=True)
    log("raw:", raw)

    raw = use("/ping.py", text=True)
    ##log("raw:", raw)

    ##use("/foo/foo.py").foo()
    ##print("foo:", use("/foo/foo.py").Foo().foo)

    

    
