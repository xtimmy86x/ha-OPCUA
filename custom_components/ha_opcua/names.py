"""Build readable hierarchical names from symbolic OPC UA NodeIds."""

import re

_QUOTED_PATH = re.compile(r'"((?:[^"]|"")*)"(?:\.|$)')


def join_hierarchy(parts) -> str:
    """Join browse names without a dot before an array index."""
    result = ""
    for part in parts:
        result += part if part.startswith("[") else (f".{part}" if result else part)
    return result


def full_hierarchy_name(node_id: str, fallback: str) -> str:
    """Return a PLC symbol's full path, or its browse name for opaque IDs."""
    if ";s=" not in node_id:
        return fallback
    identifier = node_id.split(";s=", 1)[1]
    if identifier.startswith("|var|"):
        identifier = identifier[5:]
    if not identifier:
        return fallback
    if identifier.startswith('"'):
        matches = list(_QUOTED_PATH.finditer(identifier))
        if (
            not matches
            or matches[0].start() != 0
            or matches[-1].end() != len(identifier)
            or any(a.end() != b.start() for a, b in zip(matches, matches[1:]))
        ):
            return fallback
        parts = [match[1].replace('""', '"') for match in matches]
    else:
        parts = identifier.split(".")
    if len(parts) < 2:
        return fallback
    return join_hierarchy(parts)
