# philiprehberger-safeget

[![Tests](https://github.com/philiprehberger/py-safeget/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-safeget/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-safeget.svg)](https://pypi.org/project/philiprehberger-safeget/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-safeget)](https://github.com/philiprehberger/py-safeget/commits/main)

Safely access nested dictionary keys without exceptions.

## Installation

```bash
pip install philiprehberger-safeget
```

## Usage

```python
from philiprehberger_safeget import safeget, safeset, has_path, pluck

data = {"user": {"address": {"city": "NYC"}}}

safeget(data, "user.address.city")              # "NYC"
safeget(data, "user.address.zip")               # None
safeget(data, "user.address.zip", default="?")  # "?"

# List index support
data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
safeget(data, "users.0.name")  # "Alice"

# Check existence
has_path(data, "users.0.name")   # True
has_path(data, "users.5.name")   # False

# Set nested values (creates intermediates)
safeset(data, "config.debug", True)

# Extract multiple paths
pluck(data, "users.0.name", "config.debug")
# {"users.0.name": "Alice", "config.debug": True}
```

### Deleting and walking

```python
from philiprehberger_safeget import delete_path, walk

# Remove a nested key (mutates in place); returns True if something was removed
data = {"a": {"b": 1, "c": 2}}
delete_path(data, "a.b")   # True  -> data == {"a": {"c": 2}}
delete_path(data, "x.y")   # False -> data unchanged

# Works on list indices too
data = {"users": [{"id": 1}, {"id": 2}]}
delete_path(data, "users.0")   # True -> data == {"users": [{"id": 2}]}

# Iterate every (path, value) pair in a nested structure
for path, value in walk({"a": {"b": 1, "c": [10, 20]}}):
    print(path, value)
# a {'b': 1, 'c': [10, 20]}
# a.b 1
# a.c [10, 20]
# a.c.0 10
# a.c.1 20

# Only the leaves
list(walk({"a": {"b": 1, "c": [10, 20]}}, leaves_only=True))
# [("a.b", 1), ("a.c.0", 10), ("a.c.1", 20)]
```

## API

- `safeget(data, path, default=None, separator=".")` — Get nested value
- `safeset(data, path, value, separator=".")` — Set nested value
- `has_path(data, path, separator=".")` — Check if path exists
- `pluck(data, *paths, default=None)` — Extract multiple paths
- `delete_path(data, path, separator=".")` — Remove value at path; returns whether anything was removed
- `walk(data, leaves_only=False, separator=".")` — Iterate `(path, value)` pairs for every node (or only leaves)

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-safeget)

🐛 [Report issues](https://github.com/philiprehberger/py-safeget/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-safeget/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
