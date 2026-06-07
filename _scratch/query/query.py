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
            try:
                return int(value)
            except:
                pass
            try:
                return float(value)
            except:
                pass
        return value


parse_query = parse_query()


query = dict(number="-42", letter="a", trick="-b.c", price="-9.90", trickster='-')
parsed = parse_query(**query)
print("parsed:", parsed)
