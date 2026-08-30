export default async (use, { path }) => {
  function ping() {
    return `${path}`;
  }

  return ping;
};
