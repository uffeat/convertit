export default async (use) => {
  return (source) => {
    return new Proxy(
      function () {
        return 42;
      },
      {
        get(_, key, receiver) {
          return source.get?.(key);
        },

        set(_, key, value, receiver) {
          return true;
        },

        apply(target, thisArg, args) {
          console.log("HERE");

          return target();
        },
      },
    );
  };
};
