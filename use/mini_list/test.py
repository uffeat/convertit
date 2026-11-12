import json
import pathlib

cache = {}

class use:

    def __call__(self, specifier: str, *args, **kwargs):
        if specifier in cache:
            parcel = cache[specifier]
        else:
            parcel = {}
            text = (pathlib.Path.cwd() / specifier).read_text(encoding="utf-8").strip()
            parcel.update(text=text)
            if specifier.endswith('.py'):
                locals = {}
                exec(text, {}, locals)
                value = locals["main"](self, path=specifier, **parcel)
                parcel.update(default='value', value=value)
            if parcel.get('cache', True):
                cache[specifier] = parcel

        key = {True: k for k, v in kwargs.items() if k is True and v in parcel}.get(True, parcel.get('default', 'text'))
        
       
        result = parcel.get(key)

        return result
            
use = use()

if __name__ == "__main__":

    ##print("keys:", Path().keys())##

    ##print("hooks:", use.hooks)  ##

    def test():
        MiniList = use('use/mini_list/mini_list.py')
        print('MiniList:', MiniList)

    test()
