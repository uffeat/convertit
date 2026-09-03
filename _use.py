from tools import file, server





if __name__ == "__main__":
    with server("Running local server for serving uncommitted raw code."):

        @server.function
        def _use(path: str) -> str:
            print("path:", path)  ##
            return file(path)

            
