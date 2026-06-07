class parse_query:

    def __call__(
        self,
        **query,
    ):
        return {k: self.cast(v) for k, v in query.items()}

    def cast(self, value):
        """Returns query item value as per conventions."""
        if value in ["None", "null"]:
            return
        if value in ["", "true"]:
            # NOTE Aligns with html attributes
            return True
        if value == "false":
            return False
        if isinstance(value, str):

            parts = value.split(".")
            ##print("parts:", parts)  ##
            if len(parts) == 2:
                main, decimals = parts
                print("main:", main)  ##
                print("decimals:", decimals)  ##
                if main.startswith("-"):
                    _main = main[1:]
                    if _main.isdigit() and decimals.isdigit():
                        return float(value)
                if main.isdigit() and decimals.isdigit():
                    return float(value)

                

            if value.startswith("-"):
                _value = value[1:]
                ##print("_value:", _value)  ##
                if _value.isdigit():
                    return -1 * int(_value)

            if value.isdigit():
                return int(value)

            return value
        return value


parse_query = parse_query()


query = dict(number="-42", letter="a", trick="-b.c", price="-9.90", trickster='-')
parsed = parse_query(**query)
print("parsed:", parsed)
