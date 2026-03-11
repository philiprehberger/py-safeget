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
