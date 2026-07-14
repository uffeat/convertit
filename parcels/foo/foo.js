export default async (use) => {
  const { component } = await use("@/rollo/");
  const Base = use("@@/base/base.js");
  const foo = use("@@/foo/foo.py").foo;

  foo();

  class Foo extends Base {
    #_ = {};
    constructor() {
      super();
      this._.foo = "JS foo";
    }

    get foo() {
      return this._.foo;
    }
  }

  return { Foo };
};
