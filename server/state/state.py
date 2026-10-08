def main(
    use,
    Base: type = None,
    log: callable = None,
    path: str = None,
    state: dict = None,
    **kwargs,
):
    from anvil.server import session

    ##log("state:", state)  ##

    ##from server import Log
    

    ##log("dir(app):", dir(app))  ##
    ##log("dir(app.environment):", dir(app.environment))  ##

    ##log("app.environment.tags:", app.environment.tags)  ##

    ##log("app.get_server_config():", app.get_server_config())  ##

    ##log("dir(session):", dir(session))  ##

    ##log("session.session:", session.session)  ##
    ##log("session.call_id:", session.call_id)  ##
    ##log("session.session_id:", session.session_id)  ##
    ##log("session.stack_id:", session.stack_id)  ##

    class StateSlice(Base):
        def __init__(self, name: str):
            if name in session:
                data = session[name]
                if not isinstance(data, dict):
                    data = dict()
                    session[name] = data
            else:
                data = dict()
                session[name] = data
            self.__dict__.update(__=data)

        def __call__(self, **kwargs):
            for key, value in kwargs.items():
                if value is None:
                    self._.pop(key, None)
                else:
                    self._.update(**{key: value})
            return self

        def __setitem__(self, key, value):
            self(**{key: value})

        def clear(self):
            keys = list(self.keys())
            for key in keys:
                self(**{key: None})
            return self

        def pop(self, key, default=None):
            if key in self:
                value = self[key]
                self(**{key: None})
                return value
            return default

    class State(Base):
        def __init__(self):
            self._(server=StateSlice('_server'), browser=StateSlice('_browser'))


           
        

    return State

    
