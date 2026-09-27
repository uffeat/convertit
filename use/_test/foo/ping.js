export default async (use, { meta, path, test, ...parcel }) => {
  //console.log("use:", use); //

  console.log("meta:", meta); //

  if (test) {
    console.log("Using uncommitted version of", path); //
  }

  let count = 0

  function ping() {
    const result = `${path} x ${count}`
    count++
    return result;
  }

  return { ping };
};
