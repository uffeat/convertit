from anvil import HtmlTemplate
from anvil.js import window
from anvil.server import call
from .. import tools

window.document.documentElement.dataset.bsTheme = "dark"

Log = tools.log.Log
log = Log(__file__)


def use(path: str, *args, **kwargs):
    """."""
    text = call("_use", path)
    locals = {}
    exec(text, {}, locals)
    result = locals["main"](use, log=Log(path), path=path, tools=tools, **kwargs)
    return result


class test(HtmlTemplate):
    def __init__(self, path: str = None, **query):
        log("path:", path)  ##
        log("query:", query)  ##
        result = use("client/test/test.py", component=self, query=query, route=path)
        ##log("result:", result)  ##
