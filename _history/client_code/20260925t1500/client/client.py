from anvil import HtmlComponent
from anvil.js import get_dom_node
from ..tools import Base, Log
from .use import use

log = Log(__file__)


class client(Base, HtmlComponent):
    def __init__(self, *args, **kwargs):
        """."""
        Base.__init__(self)
        ##log("args:", args)  ##
        ##log("kwargs:", kwargs)  ##
        node = get_dom_node(self)
        node.setAttribute("owner", self.__class__.__name__)
        self._(node=node)

        def on_mount(**event):
            """."""
            ##log("node.parentElement:", node.parentElement)  ##
            main = use("use/main/main.py")
            main(*args, **kwargs)

        self.add_event_handler("x-anvil-page-added", on_mount)
