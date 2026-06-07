from pathlib import Path
from jinja2 import Template

UTF_8 = "utf-8"


def render(_arg, *args, **kwargs) -> str:
    """Returns rendered template."""
    if isinstance(_arg, str):
        text = (Path.cwd() / _arg).read_text(encoding=UTF_8)
    else:
        text = _arg
    template = Template(text)
    return template.render(*args, **kwargs)
