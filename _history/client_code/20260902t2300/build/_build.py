from anvil import HtmlTemplate
from anvil.server import call
from .. import tools

Path = tools.path.Path




def use(path: str):
    """."""
    text = call("_build", path)
    locals = {}
    exec(text, {}, locals)
    main = locals["main"]
    result = main(use, Path=Path)
    return result





class build(HtmlTemplate):
    def __init__(self, path: str = None, **query):
        """."""
        print("path:", path)  ##
        print("query:", query)  ##

        use("/browser/browser.py")
        
