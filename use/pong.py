def main(
    use: callable, log=None, **kwargs
) -> callable:

   
    def pong(*args, **kwargs):
        return 'PONG'

    def load(caller):
        log("caller:", caller)
        return dict(pong=pong)

    return load
