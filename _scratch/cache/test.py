from cache import Cache

colors = dict(red="RED", green="GREEN", blue="BLUE")

foo = Cache()

@foo.onget
def create(key):
    color = colors.get(key)
    if color:
        return color.lower()





##foo = Cache(create)

foo(yellow='YELLOW')

foo['purple'] = 'PURPLE'

print('orange:', foo('orange'))

print('red:', foo('red'))

print('green:', foo['green'])


print(foo)