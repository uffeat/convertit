def main(use, **kwargs) -> None:
    """."""
    

   

   
    js = use("/js/js.py")
    Hook = use("/use/hook.py")

    
    

    @use.hook("js")
    class cls(Hook):
        hook = "transpile"

        def __init__(self, owner=None):
            Hook.__init__(self, owner=owner)

        def __call__(self, path, text: str, *args, **kwargs) -> str:
            """Returns parcel text."""
            if not isinstance(text, str):
                return
            if path.path in self.cache:
                return self.cache[path.path]

            text = f"{text}\n//# sourceURL={path.path}"
            blob = js.new(js.Blob)([text],type="text/javascript")
            url = js.URL.createObjectURL(blob)
            module = js.use(url)
            js.URL.revokeObjectURL(url)
            # XXX  TODO checks
            main = module.default
            result = main(self.owner, dict(path=path.path, text=text))
            type_name = js.type(result)
            if type_name == "Array" or type_name == "Object":
                result = js.freeze(result)

            self.cache[path.path] = result
            return result

    return use
