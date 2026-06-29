from tools import parse_query as _parse_query

# Repackage for doc and annotations

def parse_query(**query) -> dict:
    """Returns json-like interpretation of query."""
    return _parse_query(**query)
