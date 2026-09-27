export default async () => {
  return (target, ...refs) => {
    const name = Object.prototype.toString.call(target).slice(8, -1);
    if (refs.length) {
      for (const ref of refs) {
        if (name == ref) {
          return true;
        }
      }
      return false;
    }
    return name;
  };
};
