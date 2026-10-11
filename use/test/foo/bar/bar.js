export default async (use) => {

  //const [Foo, foo] = await use("use/foo/foo.py");
  //console.log('foo:', foo())
 

  function bar() {
    return 'BAR'
  }

  

  return bar;
};
