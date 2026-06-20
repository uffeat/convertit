export default async (use) => {
  const { Base } = await use("@@/base/base.js");

  class Foo extends Base {
    #_ = {};
    constructor() {
      super();
      this._.foo = "JS foo"
    }

    get foo() {
      return this._.foo;
    }
  }

  return { Foo };
};
