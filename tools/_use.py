import json
from mimetypes import guess_type
from pathlib import Path
import traceback

SOURCE = Path.cwd() / "parcels"
UTF_8 = "utf-8"


class meta:
    def __init__(self):
        self.__dict__.update(_=dict(BUILD=True, env="build"))

    def __call__(self, key):
        return self._.get(key)
            

    def __getattr__(self, key):
        return self._.get(key)
    
    def __getitem__(self, key):
        return self._.get(key)
    
meta = meta()


class use:
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
        file = SOURCE / path[1:]
        key = f"/{file.relative_to(SOURCE).as_posix()}"
        print("key:", key)  ##
        text = file.read_text(encoding=UTF_8).strip()
        ##print("text:", text)  ##
        locals = {}
        exec(text, {}, locals)
        main = locals["main"]
        exports: dict = main(self, meta=meta)

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


use = use()
