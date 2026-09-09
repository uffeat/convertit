export default async (use, { meta, path }) => {

  console.log("use:", use); //

  console.log("use.foo:", use.foo); //
  console.log("use.meta:", use.meta); //


  console.log("meta:", meta); //

  function ping() {
    return `${path}`;
  }

  return ping;
};
