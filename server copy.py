from pathlib import Path
from anvil import BlobMedia
from tools import Connection


UTF_8 = "utf-8"

def Bundle() -> BlobMedia:
    """."""
    file = Path.cwd() / "bundle.json"
    content = file.read_text(encoding=UTF_8).strip()
    content = content.encode(UTF_8)
    return BlobMedia('', content, name='bundle')


class Server:
    def __init__(self):
        """."""
        self.__dict__.update(__={})
        self._.update(bundle=Bundle())

    def __call__(self):
        """."""
        

        with Connection("Running local server.") as server_function:

            @server_function
            def _bundle():

                return self._["bundle"]
            
    @property
    def _(self) -> dict:
        return self.__



if __name__ == "__main__":
    Server()()

    
        
