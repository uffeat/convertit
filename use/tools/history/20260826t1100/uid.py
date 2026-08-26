def main(use, Base=None, **kwargs)-> callable:

    
    print("Loading Uid parcel")


    class Uid(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _value=0, **kwargs)

        def __call__(self) -> int:
            result = self._value
            self._value += 1
            return result

  

    def load(caller):
        return Uid

    return load

    
        


    

