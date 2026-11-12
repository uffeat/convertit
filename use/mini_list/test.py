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

        key = {True: k for k, v in kwargs.items() if v is True and k in parcel}.get(True, parcel.get('default'))

        if key in parcel:
            result = parcel.get(key)
        else:
            result = parcel.get('text', '')
            if specifier.endswith('.json'):
                result = json.loads(result)


            

        
       
        

        return result
            
use = use()

if __name__ == "__main__":

    ##print("keys:", Path().keys())##

    ##print("hooks:", use.hooks)  ##

    def test():
        MiniList = use('use/mini_list/mini_list.py')
        print('MiniList:', MiniList)

        foo_json = use("test/foo/foo.json", text=True)
        print("foo_json:", foo_json)

        foo_parsed = use("test/foo/foo.json")
        print("foo_parsed:", foo_parsed)

    test()
