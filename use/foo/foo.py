def main(use: callable, **kwargs) -> dict:
    """."""
    

    class Foo(use.Base):
        def __init__(self):
            use.Base.__init__(self, foo="Py foo")
           

        
        
    def foo():
        return 'foo'
       

    
    return Foo, foo
    return dict(Foo=Foo, foo=foo)
