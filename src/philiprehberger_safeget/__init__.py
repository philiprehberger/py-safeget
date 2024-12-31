"""Safely access nested dictionary keys without exceptions."""

from __future__ import annotations

from typing import Any


__all__ = [
    "flatten",
    "safeget",
    "safeset",
    "has_path",
    "pluck",
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
