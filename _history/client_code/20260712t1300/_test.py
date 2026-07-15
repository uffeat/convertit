from anvil import HtmlTemplate
from anvil.server import UplinkDisconnectedError, call
from ..console import console, log
from ..document import document
from ..js import js
from ..tools import Base, Path
from ..works import works
from ..use import app, create_node, get_text, use
from ..window import window


document.documentElement.dataset.bsTheme = "dark"




# Overload source hook to get uncommitted parcel texts from local server
@use.hook("@@")
class cls(Base):
    hook = "source"

    def __init__(self, *args, **kwargs):
        Base.__init__(self)
        self._.update(cache={})

    def __call__(self, path: Path) -> str:
        """Returns parcel text."""
        cache = self._["cache"]
        if path.path in cache:
            result = cache[path.path]
            return result

        
        try:
            result = call("_use", path.path)
            console.warn(f"Using uncommitted version of:", path.path)
            create_node(path.path)
        except:
            result = get_text(path.path)
        

        cache[path.path] = result
        return result


@window.on()
def keydown(event):
    if event.code == "KeyU" and event.shiftKey:
        stored = js.localStorage.getItem("__test__")
        path = window.prompt("Path:", stored)
        if path:
            js.localStorage.setItem("__test__", path)
            path = Path(path)
            text = call("_test", path.path)
            locals = {}
            exec(text, {}, locals)
            main = locals["main"]
            main(
                use,
                anvil=works,
                console=console,
                document=document,
                js=js,
                log=log,
                path=path.path,
                window=window,
            )


class test(HtmlTemplate):
    def __init__(self, path: str = None, **query):
        print("path:", path)  ##
        print("query:", query)  ##
