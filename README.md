# philiprehberger-safeget

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

## API

- `safeget(data, path, default=None, separator=".")` — Get nested value
- `safeset(data, path, value, separator=".")` — Set nested value
- `has_path(data, path, separator=".")` — Check if path exists
- `pluck(data, *paths, default=None)` — Extract multiple paths

## License

MIT
