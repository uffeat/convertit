def main(use: callable, Base: type=None, **kwargs) -> dict:
    """."""
    

    class Foo(Base):
        def __init__(self):
            Base.__init__(self, foo="Foo")
           

        
        
    def foo():
        return 'foo'
       

    
    return Foo, foo
    ##return dict(Foo=Foo, foo=foo)
