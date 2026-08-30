def main(use: callable, **kwargs) -> callable:

    import plotly.graph_objects as go
    import anvil
    import anvil.js as js
    import anvil.media as media
    import anvil.server as server
    import anvil.tz as tz
    import anvil.users as users

    window = js.window


    class Works:

        def __getattr__(self, key):
            """Returns anvil item."""
            return self[key]

        def __getitem__(self, key):
            """Returns anvil item."""
            if hasattr(anvil, key):
                return getattr(anvil, key)
            if hasattr(js, key):
                return getattr(js, key)
            if hasattr(server, key):
                return getattr(server, key)
            if hasattr(users, key):
                return getattr(users, key)
            if hasattr(media, key):
                return getattr(media, key)
            if hasattr(tz, key):
                return getattr(tz, key)
            if hasattr(window, key):
                return getattr(window, key)
            raise AttributeError(f"Invalid key: {key}.")

        @property
        def anvil(self):
            return anvil

        @property
        def app(self):
            return anvil.app

        @property
        def document(self):
            return window.document

        @property
        def go(self):
            return go

        @property
        def js(self):
            return js

        @property
        def media(self):
            return media

        @property
        def server(self):
            return server

        @property
        def tz(self):
            return tz

        @property
        def users(self):
            return users

        @property
        def window(self):
            return window


   


    return Works()
