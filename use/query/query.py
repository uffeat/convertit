def main(
    use,
    **kwargs,
) -> callable:
    """."""

    class Query:
        def __call__(self, *args, **kwargs) -> dict:
            return {k: self.cast(v) for k, v in kwargs.items()}

        @staticmethod
        def cast(value: str):
            if value in ["", "true", "True"]:
                return True
            if value in ["false", "False"]:
                return False
            if value.isnumeric():
                return int(value)
            if (value.startswith("{") and value.endswith("}")) or (
                value.startswith("[") and value.endswith("]")
            ):
                import json

                return json.loads(value)
            return value

    Query = Query()

    return Query
