


def main(
    use: callable, log=None, path: str = None, test: bool = None, **kwargs
) -> callable:

    if test:
        log(f"Unbuilt version of {path.full}")

    count = dict(value=0)

    def ping(*args, **kwargs) ->str:
        
        result = f"PING x {count['value']}"
      
        count['value'] +=  1
        return result

    return ping
