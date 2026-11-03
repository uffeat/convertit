from pathlib import Path


class use:

    def __init__(self, *args, **kwargs):
        self._.update(_cache={})

    @property
    def _(self) -> dict:
        return self.__dict__.setdefault("__", {})

    def __getattr__(self, key: str):
        # Ensure that getattr and hasattr works
        if key not in self._:
            raise AttributeError(key)
        return self._[key]

    def __getitem__(self, key):
        # Facilitate **-unpacking
        return self._.get(key)

    def keys(self, *args, **kwargs):
        # Facilitate **-unpacking
        return self._.keys()

    def __call__(self, *args, **kwargs):
        # Parse args
        specifier = next((a for a in args if isinstance(a, str)), None)
        if specifier:
            specifier, *args = args
        # Get parcel
        if specifier in self._cache:
            parcel = self._cache[specifier]
        else:
            parcel = {}
            path = Path.cwd() / specifier
            locals = {}
            text = path.read_text(encoding="utf-8").strip()
            parcel.update(text=text)

            file_type = path.suffix[1:]
            file_types = tuple([t[1:] for t in path.suffixes])
            ##print("file_type", file_type)  ##
            ##print("file_types", file_types)  ##

            # .py
            exec(text, {}, locals)
            main = locals.pop("main", None)
            if callable(main):
                value = main(self)
                if value is not None:
                    parcel.update(value=value, default="value")

        # Get key
        options = {"key": k for k, v in kwargs.items() if k in parcel and v is True}
        key = options.get("key", parcel.get("default", "text"))

        # Get result
        result = parcel.get(key)

        return result


use = use()

if __name__ == "__main__":
    foo = use("test/foo.foo.py")
