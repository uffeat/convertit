def main(use: callable, **kwargs) -> callable:

    def foo():
        return "FOO"

    return foo
