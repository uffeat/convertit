"""
test/ping/test.py
"""


def main(use, log=None, **kwargs):
    log("text:\n", use("use/ping.py", raw=True))
    log("ping:\n", use("use/ping.py")())
    log("ping:\n", use("use/ping.py")())

    
    log("node:\n", use("use/ping.py", key="node"), native=True)
    log("node:\n", use("use/ping.py", use.js.object(key="node")), native=True)
