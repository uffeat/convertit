from anvil import HtmlTemplate
from anvil.server import UplinkDisconnectedError, call
from anvil.js.window import console, document, localStorage, window
from ..client_tools import Future
from ..js import js
from ..tools import Base, Path, meta
from ..works import works
from ..use import use

document.documentElement.dataset.bsTheme = "dark"


def keydown(event):
    if event.code == "KeyU" and event.shiftKey:
        stored = localStorage.getItem("__test__")
        path = window.prompt("Path:", stored)
        if path:
            localStorage.setItem("__test__", path)
            path = Path(path)
            text = call("_test", path.path)

            locals = {}
            exec(text, {}, locals)

            main = locals["main"]

            result = main(
                use,
                Base=Base,
                Future=Future,
                anvil=works,
                console=console,
                document=document,
                js=js,
                meta=meta,
                window=window,
            )

window.addEventListener('keydown', keydown)


# HACK Inherit from Spacer -> simplest component that allows server routing
class test(HtmlTemplate):
    def __init__(self, path: str = None, **query):
        print("path:", path)  ##
        print("query:", query)  ##
