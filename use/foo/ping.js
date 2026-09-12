export default async (use, { path, ...parcel }) => {
  console.log("use:", use); //

  //console.log("parcel:", parcel); //

  function ping() {
    return `${path}`;
  }

  return { ping };
};
