def main(use, *args, **kwargs):

  ##print("args:", args)

  ##path = args[0]
  ##print("path:", path)
  ##print("path:", kwargs['path'])

  Bar = use("test/foo/bar.py").Bar
  print("Bar from foo:", Bar)

  def foo(*args, **kwargs):
    return 42

  return foo

    