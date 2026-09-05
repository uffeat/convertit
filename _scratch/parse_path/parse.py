def parse_path(path: str):
    """."""
    parts = tuple([p if p else "/" for p in path.split("/")])
    source = parts[0]
    relative = "/" + "/".join(parts[1:])
    parents = tuple(parts[1:-1])
    parent = parents[-1] if parents else ""
    name = parts[-1]
    _file = {}
    if "." in name:
        stem, sep, types = name.partition(".")
        _file.update(
            file=True,
            stem=stem,
            type=types.split(sep)[-1],
            types=types,
        )
    else:
        _file.update(stem=name)

    return dict(
        name=name,
        parent=parent,
        parents=parents,
        parts=parts,
        path=path,
        relative=relative,
        source=source,
        **_file,
    )


path = "use/foo/foo.py"
print(f"{path}:", parse_path(path))

path = "/foo.py"
##print(f"{path}:", parse_path(path))
