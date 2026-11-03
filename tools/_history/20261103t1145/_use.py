from pathlib import Path


class use:
    _cache = {}

    def __call__(self, path: str):
        if path not in self._cache:
            _ = {}
            exec((Path.cwd() / path).read_text(encoding="utf-8").strip(), {}, _)
            self._cache[path] = _["main"](self)
        return self._cache[path]


use = use()