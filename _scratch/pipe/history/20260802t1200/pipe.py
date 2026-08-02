class Pipe:
    def __init__(self, name=None, owner=None):

        class add:
            owner = self

            def __init__(self):
                """For future use."""

            def __call__(self, runner):
                add.owner._['runners'].append(runner)
                return runner

        self._ = dict(add=add, name=name, owner=owner, runners=[])

    def __call__(self, value=None, **detail):
        """Runs pipe and returns result."""
        self._['detail'] = dict(**detail)
        self._['result'] = value
        for index, runner in enumerate(self._['runners']):
            if isinstance(runner, type):
                runner = runner()
            value = runner(value, index, self)
            if isinstance(value, Exception):
                break
            self._['result'] = value
        return self._['result']

    @property
    def add(self) -> callable:
        return self._['add']

    @property
    def detail(self) -> dict:
        return self._.get('detail', {})

    @property
    def name(self):
        return self._['name']

    @name.setter
    def name(self, name):
        self._['name'] = name

    @property
    def owner(self):
        return self._['owner']

    @property
    def result(self):
        return self._.get('result', ...)

    @property
    def runners(self) -> tuple:
        return tuple(self._['runners'])

    def clear(self) -> "Pipe":
        self.detail.clear()
        self._.pop("result", ...)
        self._['runners'].clear()
        return self


