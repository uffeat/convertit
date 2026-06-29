def main(use, **kwargs):

    class Base:

        def __init__(self):
            self.__dict__.update(__={})

        @property
        def _(self) -> dict:
            return self.__
        
    return dict(Base=Base)
        


    
