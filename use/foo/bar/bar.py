def main(use, log=None, **kwargs):

    Foo, foo = use("use/foo/foo.py")
  

    class Bar(use.Base):
        def __init__(self):
            use.Base.__init__(self, bar="Py bar")


    def bar():
        log(f'From bar function: {foo()}')
          

       

    return dict(Bar=Bar, bar=bar)
