export default async (use, { log, path, session }) => {
  const pong = await use("use/pong.js");
  console.log("pong:", pong());

  //console.log("text:", await use("use/pong.js", { key: "text" }));//

  function ping() {
    console.log("session():", session());
    return `${path}`;
  }

  return (session) => {
    console.log("session:", session);
    return ping;
  };
};
