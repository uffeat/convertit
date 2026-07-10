def main(use, js=None, **kwargs):
    """."""

    Base = use("@@/tools/base.py")

    class Component(Base):
        """Web component controller."""

        def __init__(self, node):
            Base.__init__(self)
            self._.update(node=node)

        def __call__(self, *args, **updates):
            """."""
            if len(args) == 1:
                selector = args[0]
                if isinstance(selector, str):
                    return self.select(selector)

            if updates:
                self.node.update(updates)

            nodes = []
            for a in args:
                if js.isinstance(a, js.HTMLElement) or isinstance(a, str):
                    nodes.append(a)
                elif isinstance(a, Component):
                    nodes.append(a.node)

            if nodes:
                self.node.append(*nodes)

            return self.node

        def __contains__(self, node) -> bool:
            if isinstance(node, Component):
                node = node.node
            return self.node.contains(node)

        def __eq__(self, node) -> bool:
            if isinstance(node, Component):
                node = node.node
            return self.node is node

        def __iter__(self):
            return iter(self.node.children)

        def __getattr__(self, key):
            return getattr(self.node, key, None)

        def __getitem__(self, key):
            item = getattr(self.node, key, ...)

            return getattr(self.node, key, None)

        def __len__(self) -> int:
            return len(self.node.children)

        def __str__(self) -> str:
            return self.node.outerHTML

        @property
        def node(self):
            return self._["node"]

        def on(self, *args, run: bool = False, **options) -> callable:
            """Decorates event handler."""

            def register(handler: callable) -> callable:
                """Registers event handler."""
                name = handler.__name__
                if isinstance(handler, type):
                    handler = handler()

                event_type: str = next(iter(args), name)
                self.node.addEventListener(event_type, handler, options)

                if run:
                    handler(js.CustomEvent(event_type, dict(detail="run")))

                def remove() -> None:
                    """Removes event handler."""
                    self.node.removeEventListener(event_type, handler)

                return remove

            return register

        def select(self, selector: str):
            """."""
            nodes = list(self.node.querySelectorAll(selector))
            return nodes[0] if len(nodes) == 1 else nodes

        def update(self, *children, **updates):
            """."""
            if updates:
                self.node.update(updates)
            if children:
                self.node.append(
                    *[
                        c.node if isinstance(c, Component) else c
                        for c in children
                        if isinstance(c, Component)
                        or js.isinstance(c, js.HTMLElement)
                        or isinstance(c, str)
                    ]
                )
            return self

    class component:
        """Component factory."""

        def __call__(self, node, *args, **updates) -> Component:

            if updates:
                node.update(updates)

            nodes = []
            for a in args:
                if js.isinstance(a, js.HTMLElement) or isinstance(a, str):
                    nodes.append(a)
                elif isinstance(a, Component):
                    nodes.append(a.node)

            if nodes:
                self.node.append(*nodes)

            return Component(node)

        def __getattr__(self, tag):
            return self[tag]

        def __getitem__(self, tag: str) -> callable:

            def factory(*args, **updates) -> Component:
                _Component = use("@/rollo/").Component
                node = _Component(tag)(
                    *[a.node if isinstance(a, Component) else a for a in args], updates
                )
                return Component(node)

            return factory

    return component()
