export default async (use, { node, path, text, test, ...rest } = {}) => {
  if (test) {
    console.log("Unbuilt version of", path);
  }

  function ping() {
    return "PING.JS";
  }

  return ping;
};
