export default (use) => {
  class Base {
    #_ = {};
    constructor() {}

    get _() {
      return this.#_;
    }
  }

  return { Base };
};
