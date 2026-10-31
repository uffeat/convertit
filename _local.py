from tools import file, connect

class use:
    def __init__(self):
        """."""

    def __call__(self):
        """."""




if __name__ == "__main__":
    ##connect()
    path = input("Path:")


    path = "test/echo/echo.py"


    text = file(path)

    print('text:', text)
