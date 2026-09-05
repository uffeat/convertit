def main(use, path: str=None, **kwargs):
    """."""
    print("use.meta.DEV:", use.meta.DEV)  ##

    def is_part(key: str):
        if key.startswith('_') and key.endswith('_') and len(key) > 2:
            return key[1:-1].isnumeric()
    

    def main(*args, **kwargs):
        print("args:", args)  ##
        print("kwargs:", kwargs)  ##

        
        parts = [v for k, v in kwargs.items() if is_part(k)]
        print("parts:", parts)  ##

    return main


    
