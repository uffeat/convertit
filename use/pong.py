def main(
    use: callable, log=None, path: str = None, session: callable = None, **kwargs
) -> callable:

    def pong(*args, **kwargs):
        return f"{path}"

    def load(session):
        log("session:", session)
        ##return pong
        return dict(pong=pong)

    return load
