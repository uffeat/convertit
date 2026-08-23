def main(
    use: callable, log=None, **kwargs
) -> callable:

   
    def pong(*args, **kwargs):
        return 'PONG'

    def load(*args, caller=None, session: int = None, **kwargs):
        log("caller:", caller)
        log("session:", session)
        return pong

    return load
