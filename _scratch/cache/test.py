from cache import Cache

colors = dict(red="RED", green="GREEN", blue="BLUE")


def create(key):
    color = colors.get(key)
    if color:
        return color.lower()


foo = Cache(create=create)

foo(yellow='YELLOW')
foo('orange', 'ORANGE')
print(foo('orange'))


print(foo)