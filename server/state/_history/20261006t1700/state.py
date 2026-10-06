def main(
    use,
    Base: type = None,
    log: callable = None,
    path: str = None,
    **kwargs,
):
    from anvil.server import session

    ##from server import Log
    ##from tools import Dictionary

    ##log("dir(app):", dir(app))  ##
    ##log("dir(app.environment):", dir(app.environment))  ##

    ##log("app.environment.tags:", app.environment.tags)  ##

    ##log("app.get_server_config():", app.get_server_config())  ##

    ##log("dir(session):", dir(session))  ##

    ##log("session.session:", session.session)  ##
    ##log("session.call_id:", session.call_id)  ##
    ##log("session.session_id:", session.session_id)  ##
    ##log("session.stack_id:", session.stack_id)  ##

    class State(Base):
        def __init__(self):
            if "_state" in session:
                _state = session["_state"]
                if not isinstance(_state, dict):
                    _state = dict()
                    session["_state"] = _state
            else:
                _state = dict()
                session["_state"] = _state

            self.__dict__.update(__=_state)

        def __call__(self, **kwargs):
            for key, value in kwargs.items():
                if value is None:
                    self._.pop(key, None)
                else:
                    self._.update(**{key: value})
            return self

        def __setitem__(self, key, value):
            self(**{key: value})

        @property
        def id(self) -> str:
            return session.session_id

    return State
