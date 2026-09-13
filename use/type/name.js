export default async (use) => {
  return (target) => Object.prototype.toString.call(target).slice(8, -1);
};
