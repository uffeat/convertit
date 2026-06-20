export default async (use) => {
  class Base {
    #_ = {};
    constructor() {}

    get _() {
      return this.#_;
    }
  }

  return { Base };
};
