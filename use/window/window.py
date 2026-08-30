def main(use, tools=None, **kwargs):
    import anvil.js
    
   
    new = anvil.js.new
    window = anvil.js.window

    Base = tools.base.Base
    

    CustomEvent = window.CustomEvent
    Reflect = window.Reflect
    globalThis = window.globalThis
    
    new = anvil.js.new
   
    
    class Window(Base):
        

        def __init__(self):
            Base.__init__(self)

        def __call__(self, **updates):
            for key, value in updates.items():
                setattr(globalThis, key, value)
            return self

        def __getattr__(self, key):
            return self[key]

        def __getitem__(self, key):
            return getattr(globalThis, key, None)

        @property
        def window(self):
            return globalThis

        def on(self, *args, run: bool = False, **options) -> callable:
            """Decorates event handler."""

            def register(handler: callable) -> callable:
                """Registers event handler."""
                event_type = next(iter(args), handler.__name__)
                globalThis.addEventListener(event_type, handler, options)

                if run:
                    handler(new(CustomEvent, event_type, dict(detail="run")))

                def remove() -> None:
                    """Removes event handler."""
                    globalThis.removeEventListener(handler)

                return remove

            return register
        
        def remove(self, key: str):
            """Removes item from global namespace."""
            value = self[key]
            Reflect.deleteProperty(globalThis, key)
            return value


    
    

    return Window()
