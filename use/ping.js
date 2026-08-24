export default async (use, {log}) => {
  const pong = await use("use/pong.js");
  console.log("pong:", pong());

  console.log("text:", await use("use/pong.js", { key: "text" }));

  return (caller) => {
    log("caller:", caller);
    return function ping() {
      return "PING";
    };
  };
};
