"""
test/path/bug.py
"""
def main(
    use: callable,
    Base: type = None,
    locals: dict = None,
    log: callable = None,
    path: str = None,
    test: callable = None,
    **kwargs
) -> dict:
    """."""
   

    Path = use("use/path/path.py")
    log("Path:", Path)  ##

    

    Path = use.Path
    log("Path:", Path)  ##

    
