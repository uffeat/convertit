def main(
    use: callable,
    Base: type = None,
    log: callable = None,
    path: str = None,
    self: callable = None,
    test: bool = None,
    spec: dict = dict(pong='PONG'),
    **kwargs,
) -> 'main':
    """{"stuff": 42}"""

    log("self.config:", self.config)  ##

    self.config.update(ding="DING")

    ##self.__doc__ = dict(dong='DONG')

    self.__annotations__['return'] = dict(bar=8)

    self.__name__ = '{"stuff": 42}'

    spec.update(boom='BOOM')

    def ping(*args, **kwargs):

        return path

    return ping


config = dict(stuff=42)
