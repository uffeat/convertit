class parse_query:

    def __call__(
        self,
        **query,
    ) -> dict:
        """Returns json-like interpretation of query."""
        return {k: self.cast(v) for k, v in query.items()}

    def cast(self, value):
        """Returns query item value as per conventions."""
        
        if value in ["None", "null"]:
            return
        if value in ["", "True", "true"]:
            # NOTE ""-convention aligns with html attributes
            return True
        if value in ["False", "false"]:
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
