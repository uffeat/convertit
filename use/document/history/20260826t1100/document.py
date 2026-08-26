def main(use, Base=None, anvil=None, **kwargs):
    """."""

    CustomEvent = anvil.window.CustomEvent
    document = anvil.window.document
    new = anvil.js.new

    class Document(Base):
        """document wrapper."""

        def __init__(self):
            Base.__init__(self)

        def __call__(self, **updates):
            for key, value in updates.items():
                setattr(document, key, value)
            return self

        def __getattr__(self, key):
            return self[key]

        def __getitem__(self, key):
            return getattr(document, key, None)

        @property
        def document(self):
            return document

        def on(self, *args, run: bool = False, **options) -> callable:
            """Decorates event handler."""

            def register(handler: callable) -> callable:
                """Registers event handler."""
                event_type = next(iter(args), handler.__name__)
                document.addEventListener(event_type, handler, options)

                if run:
                    handler(new(CustomEvent, event_type, dict(detail="run")))

                def remove() -> None:
                    """Removes event handler."""
                    document.removeEventListener(handler)

                return remove

            return register

    value = Document()

    def load(caller):
        return value

    return load
