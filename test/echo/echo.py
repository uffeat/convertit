def main(use: callable, log: callable = None, **kwargs):
    """test/echo/echo.py"""
    from anvil.server import call

    log("session:", use.session)

    result = call("main", "echo", session=use.session)
    log("result:", result)  ##

    result = call("main", "echo", args=[1, 2, 3, use.dict(foo=42)], kwargs=dict(foo=42))
    log("result:", result)  ##
