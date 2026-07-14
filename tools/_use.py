import json
from mimetypes import guess_type
from pathlib import Path
import traceback

SOURCE = Path.cwd() / "parcels"
UTF_8 = "utf-8"


class Use:
    """Local import engine."""
    def __init__(self):
        """."""
        self.__dict__.update(__={})
        self._.update(cache={})

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self, path: str):
        """."""
        cache = self._["cache"]
        if path in cache:
            return cache[path]

        path = path[3:]

        file = SOURCE / path
        key = f"@@/{file.relative_to(SOURCE).as_posix()}"
        ##print("key:", key)  ##
        text = file.read_text(encoding=UTF_8).strip()
        ##print("text:", text)  ##
        locals = {}
        exec(text, {}, locals)
        main = locals["main"]
        result = main(self)

        if isinstance(result, dict):
            exports: dict = result

            class parcel:
                def __call__(self, key):
                    return exports.get(key)

                def __getattr__(self, key):
                    return exports.get(key)

                def __geitem__(self, key):
                    return exports.get(key)

            result = parcel()

        cache[key] = result

        return result


use = Use()
