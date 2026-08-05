from cache import Cache

colors = dict(red="RED", green="GREEN", blue="BLUE")

class Owner:
    """."""
    def create(self):
        """."""

    @staticmethod
    def stat(self):
            """."""


owner = Owner()

print('type_name:', type(owner.create).__name__)
print('type_name:', type(owner.stat).__name__)


def create(key):
    color = colors.get(key)
    if color:
        return color.lower()


print('type_name:', type(create).__name__)


foo = Cache(create)

foo(yellow='YELLOW')
foo('orange', 'ORANGE')
foo['purple'] = 'PURPLE'

print('orange:', foo('orange'))

print('red:', foo('red'))

print('green:', foo['green'])


print(foo)