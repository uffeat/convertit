export default async (use, {path, session}) => {

  function pong() {
      console.log("session():", session());
      return `${path}`;
    };
  

  return (session) => {
    console.log("session:", session);
    return pong
  };
};
