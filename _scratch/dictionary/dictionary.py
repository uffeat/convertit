class Dictionary(dict):

    def __init__(self, *args, **kwargs):
        self(*args, **kwargs)

    def __call__(self, *args, **kwargs) -> "Dictionary":
        updates = Dictionary.update({}, *args, **kwargs)
        if self:
            additions = {
                k: v for k, v in updates.items() if k not in self and v is not None
            }
            changes = {
                k: v
                for k, v in updates.items()
                if k in self and v is not None and v != self[k]
            }
            removals = [k for k, v in updates.items() if k in self and v is None]
            self.update(additions, changes)
            self.pop(removals)

        else:
            # Update with None-values filtered out
            dict.update(self, {k: v for k, v in updates.items() if v is not None})
        return self

    def pop(self, key, default=None):
        if isinstance(key, list):
            return [self.pop(k, default) for k in key]
        return dict.pop(self, key, default)

    def update(self, *args, **kwargs):
        # Create intermediary to control update order
        updates = dict()
        # Update intermediary from args
        for a in args:
            # NOTE unpack to accomodate non-dicts
            updates.update(**a)
        # Update intermediary from kwargs
        updates.update(kwargs)
        dict.update(self, updates)
        return self

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Dictionary({k: self[k] for k in list(self.keys())[key]})




           
        return dict.__getitem__(self, key)
    
    def index(self, key, default=None):

        lookup = {k: i for i, k in enumerate(self.keys())}


        return lookup.get(key, default)



        

    def at(self, index: int, default=None):
        if index < 0:
            lookup = {-(i+1): k for i, k in enumerate(reversed(data.keys()))}
        else:
            lookup = {i: k for i, k in enumerate(self.keys())}
        return lookup.get(index, default)


        


if __name__ == "__main__":
    data = Dictionary(foo=42, bad=None)
    data(boom="BOOM")
    data(boom=None, bar="BAR")
    data(dict(ping="PING"), dict(pong="PONG"))

   

    ##print("popped:", data.pop(["pong", "pang"]))

    print("data:", data)

    ##print("foo:", data['foo'])


    




    ##print("index of foo:", data.index("foo"))
    ##print("index of bar:", data.index("bar"))
    ##print("index of bad:", data.index("bad"))


    ##print("at 0:", data.at(0))
    ##print("at 1:", data.at(1))
    ##print("at 2:", data.at(2))

    ##print("at -1:", data.at(-1))
    ##print("at -2:", data.at(-2))
    ##print("at -3:", data.at(-3))

    print('data[0:2]:', data[0:2])
    print('data[0:4]:', data[0:4])
    print('data[1:-1]:', data[1:-1])
    


    
