class Attempt:

    @property
    def _(self) -> dict:
        return self.__dict__.setdefault("__", {})
    
    def resolver(self, *args, **kwargs) -> callable:
        if args:
            target = args[0]
            if callable(target):
                self._.update(resolve=target)
                return target

    def rejector(self, *args, **kwargs) -> callable:
        if args:
            target = args[0]
            if callable(target):
                self._.update(reject=target)
                return target
        

    def __call__(self, *args, **kwargs):
        """."""
        resolve = self._.get('resolve')
        reject = self._.get('reject')
        try:
            if resolve:
                return resolve(*args, **kwargs)
        except:
            if reject:
                return reject(*args, **kwargs)


attempt = Attempt()

@attempt.resolver
def resolve(value):
    return dict(value)

@attempt.rejector
def reject(value):
    return {}


print('result:', attempt(42))
print('result:', attempt({"foo": 42}))


data = {}

[data.update(attempt(v)) for v in [42, {"foo": 42}]]

print('data:', data)