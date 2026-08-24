export default async (use) => {
  

  return (caller) => {
    return function pong() {
      return "PONG";
    };
  };
};
