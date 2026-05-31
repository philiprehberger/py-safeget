"""Safely access nested dictionary keys without exceptions."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any


__all__ = [
    "delete_path",
    "flatten",
    "safeget",
    "safeset",
    "has_path",
    "pluck",
    "walk",
]

_MISSING = object()


def safeget(data: dict | list, path: str, default: Any = None, *, separator: str = ".") -> Any:
    """Safely access a nested value using dot-notation path.

    Supports dict keys and list indices (numeric segments).

    Args:
        data: The dict or list to traverse.
        path: Dot-separated path string (e.g., ``"a.b.0.c"``).
        default: Value to return if the path is not found.
        separator: Path separator. Defaults to ``"."``.

    Returns:
        The value at the path, or *default* if not found.
    """
    keys = path.split(separator)
    current: Any = data

    for key in keys:
        if isinstance(current, dict):
            current = current.get(key, _MISSING)
            if current is _MISSING:
                return default
        elif isinstance(current, (list, tuple)):
            try:
                current = current[int(key)]
            except (ValueError, IndexError):
                return default
        else:
            return default

    return current


def safeset(data: dict, path: str, value: Any, *, separator: str = ".") -> dict:
    """Set a nested value using dot-notation path, creating intermediates.

    Args:
        data: The dict to modify (mutated in place).
        path: Dot-separated path string.
        value: The value to set.
        separator: Path separator. Defaults to ``"."``.

    Returns:
        The original dict (for chaining).
    """
    keys = path.split(separator)
    current = data

    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]

    current[keys[-1]] = value
    return data


def has_path(data: dict | list, path: str, *, separator: str = ".") -> bool:
    """Check whether a nested path exists.

    Args:
        data: The dict or list to check.
        path: Dot-separated path string.
        separator: Path separator. Defaults to ``"."``.

    Returns:
        True if the full path exists.
    """
    result = safeget(data, path, default=_MISSING, separator=separator)
    return result is not _MISSING


def pluck(data: dict | list, *paths: str, default: Any = None, separator: str = ".") -> dict[str, Any]:
    """Extract multiple paths from a nested structure.

    Args:
        data: The dict or list to extract from.
        *paths: Dot-separated path strings.
        default: Default for missing paths.
        separator: Path separator.

    Returns:
        Dict mapping each path to its value.
    """
    return {path: safeget(data, path, default=default, separator=separator) for path in paths}


def flatten(data: dict[str, Any], *, separator: str = ".") -> dict[str, Any]:
    """Flatten a nested dictionary into a single-level dict with path keys.

    Args:
        data: The nested dict to flatten.
        separator: Key separator. Defaults to ``"."``.

    Returns:
        A flat dict where keys are dot-separated paths.

    Example::

        >>> flatten({"a": {"b": 1, "c": {"d": 2}}})
        {"a.b": 1, "a.c.d": 2}
    """
    result: dict[str, Any] = {}

    def _flatten(obj: Any, prefix: str) -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_key = f"{prefix}{separator}{key}" if prefix else key
                _flatten(value, new_key)
        elif isinstance(obj, (list, tuple)):
            for i, value in enumerate(obj):
                new_key = f"{prefix}[{i}]"
                _flatten(value, new_key)
        else:
            result[prefix] = obj

    _flatten(data, "")
    return result


def delete_path(
    data: dict | list,
    path: str,
    *,
    separator: str = ".",
) -> bool:
    """Remove the value at *path* from *data*. Mutates in place.

    Args:
        data: The dict or list to modify.
        path: Dot-separated path string.
        separator: Path separator. Defaults to ``"."``.

    Returns:
        True if anything was removed; False if the path was absent.
    """
    keys = path.split(separator)
    parent: Any = data

    for key in keys[:-1]:
        if isinstance(parent, dict):
            if key not in parent:
                return False
            parent = parent[key]
        elif isinstance(parent, (list, tuple)):
            try:
                parent = parent[int(key)]
            except (ValueError, IndexError):
                return False
        else:
            return False

    last = keys[-1]
    if isinstance(parent, dict):
        if last in parent:
            parent.pop(last)
            return True
        return False
    if isinstance(parent, list):
        try:
            parent.pop(int(last))
            return True
        except (ValueError, IndexError):
            return False
    return False


def walk(
    data: dict | list,
    *,
    leaves_only: bool = False,
    separator: str = ".",
) -> Iterator[tuple[str, Any]]:
    """Yield ``(path, value)`` pairs for every node in *data*.

    Args:
        data: The dict or list to traverse.
        leaves_only: When True, only yield leaf nodes (non-dict, non-list values).
        separator: Path separator. Defaults to ``"."``.

    Yields:
        Tuples of ``(path, value)`` for each node encountered.
    """

    def _walk(node: Any, prefix: str) -> Iterator[tuple[str, Any]]:
        if isinstance(node, dict):
            items: Iterator[tuple[Any, Any]] = iter(node.items())
        elif isinstance(node, list):
            items = iter(enumerate(node))
        else:
            return

        for key, value in items:
            new_path = f"{prefix}{separator}{key}" if prefix else str(key)
            is_container = isinstance(value, (dict, list))
            if is_container:
                if not leaves_only:
                    yield new_path, value
                yield from _walk(value, new_path)
            else:
                yield new_path, value

    yield from _walk(data, "")
