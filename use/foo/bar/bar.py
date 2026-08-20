def main(use, log=None, node=None, text=None, **kwargs):

    Foo, foo = use("use/foo/foo.py")
  

    class Bar(use.Base):
        def __init__(self):
            use.Base.__init__(self, bar="BAR")


    def bar():
        log(f'From bar function: {foo()}')
          

       

    return dict(Bar=Bar, bar=bar, node=node)
