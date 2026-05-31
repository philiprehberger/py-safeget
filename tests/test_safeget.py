from philiprehberger_safeget import safeget, safeset, has_path, pluck


def test_simple_get():
    assert safeget({"a": 1}, "a") == 1


def test_nested_get():
    data = {"a": {"b": {"c": 42}}}
    assert safeget(data, "a.b.c") == 42


def test_missing_returns_default():
    assert safeget({"a": 1}, "b") is None
    assert safeget({"a": 1}, "b", default="x") == "x"


def test_deep_missing():
    assert safeget({"a": 1}, "a.b.c") is None


def test_list_index():
    data = {"users": [{"name": "Alice"}, {"name": "Bob"}]}
    assert safeget(data, "users.0.name") == "Alice"
    assert safeget(data, "users.1.name") == "Bob"


def test_list_index_out_of_range():
    data = {"items": [1, 2]}
    assert safeget(data, "items.5") is None


def test_has_path_true():
    data = {"a": {"b": 1}}
    assert has_path(data, "a.b") is True


def test_has_path_false():
    data = {"a": {"b": 1}}
    assert has_path(data, "a.c") is False


def test_safeset_creates_intermediates():
    data = {}
    safeset(data, "a.b.c", 42)
    assert data == {"a": {"b": {"c": 42}}}


def test_safeset_overwrites():
    data = {"a": {"b": 1}}
    safeset(data, "a.b", 2)
    assert data["a"]["b"] == 2


def test_safeset_returns_dict():
    data = {}
    result = safeset(data, "x", 1)
    assert result is data


def test_pluck():
    data = {"a": 1, "b": {"c": 2}, "d": 3}
    result = pluck(data, "a", "b.c", "missing")
    assert result == {"a": 1, "b.c": 2, "missing": None}


def test_custom_separator():
    data = {"a": {"b": 1}}
    assert safeget(data, "a/b", separator="/") == 1


def test_none_value_vs_missing():
    data = {"a": None}
    assert safeget(data, "a") is None
    assert has_path(data, "a") is True


def test_flatten_nested_dict():
    from philiprehberger_safeget import flatten

    data = {"a": {"b": 1, "c": {"d": 2}}}
    result = flatten(data)
    assert result == {"a.b": 1, "a.c.d": 2}


def test_flatten_with_list():
    from philiprehberger_safeget import flatten

    data = {"items": [10, 20]}
    result = flatten(data)
    assert result == {"items[0]": 10, "items[1]": 20}


def test_flatten_empty_dict():
    from philiprehberger_safeget import flatten

    assert flatten({}) == {}


def test_flatten_flat_dict():
    from philiprehberger_safeget import flatten

    data = {"a": 1, "b": 2}
    assert flatten(data) == {"a": 1, "b": 2}


def test_flatten_custom_separator():
    from philiprehberger_safeget import flatten

    data = {"a": {"b": 1}}
    assert flatten(data, separator="/") == {"a/b": 1}


def test_delete_path_removes_nested_key():
    from philiprehberger_safeget import delete_path

    data = {"a": {"b": 1, "c": 2}}
    assert delete_path(data, "a.b") is True
    assert data == {"a": {"c": 2}}


def test_delete_path_missing_returns_false():
    from philiprehberger_safeget import delete_path

    data = {"a": {"b": 1}}
    assert delete_path(data, "x.y") is False
    assert data == {"a": {"b": 1}}


def test_delete_path_list_index():
    from philiprehberger_safeget import delete_path

    data = {"users": [{"id": 1}, {"id": 2}]}
    assert delete_path(data, "users.0") is True
    assert len(data["users"]) == 1
    assert data["users"][0] == {"id": 2}


def test_walk_yields_all_nodes():
    from philiprehberger_safeget import walk

    data = {"a": {"b": 1, "c": [10, 20]}}
    result = list(walk(data))
    expected = {
        ("a", (("b", 1), ("c", (10, 20)))),
        ("a.b", 1),
        ("a.c", (10, 20)),
        ("a.c.0", 10),
        ("a.c.1", 20),
    }
    # Compare via normalized forms since dicts/lists aren't hashable.
    def _normalize(value):
        if isinstance(value, dict):
            return tuple((k, _normalize(v)) for k, v in value.items())
        if isinstance(value, list):
            return tuple(_normalize(v) for v in value)
        return value

    normalized = {(p, _normalize(v)) for p, v in result}
    assert normalized == expected


def test_walk_leaves_only():
    from philiprehberger_safeget import walk

    data = {"a": {"b": 1, "c": [10, 20]}}
    result = list(walk(data, leaves_only=True))
    assert sorted(result) == sorted([
        ("a.b", 1),
        ("a.c.0", 10),
        ("a.c.1", 20),
    ])
