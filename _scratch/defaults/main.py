def foo(*args, defaults=[1, 2, 3], **kwargs):
  
  print('defaults:', defaults)

foo()
foo(defaults=[4, 5])
foo()