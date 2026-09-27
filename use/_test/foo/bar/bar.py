def main(use, Base: type=None, log=None, node=None, text=None, **kwargs):

    Foo, foo = use("use/foo/foo.py")
  

    class Bar(Base):
        def __init__(self):
            Base.__init__(self, bar="BAR")


    def bar():
        log(f'From bar function: {foo()}')
          

       

    return dict(Bar=Bar, bar=bar, node=node, text=text)
