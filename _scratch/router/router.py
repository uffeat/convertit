def setup(depth=3):
  for i in range(depth):
    signature = ''.join([f'/:_{j}_' for j in range(i+1)])
    print(signature)


setup()