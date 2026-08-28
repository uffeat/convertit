export default async (use, { log, path, meta }) => {

  console.log('meta:',meta)

  log(path)
 
  
  function ping() {
    return `${path}`;
  }

  return ping
};
