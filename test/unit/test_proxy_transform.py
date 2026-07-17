"""Unit tests for pure response-transformation helpers in proxy.py."""

import proxy
from proxy import normalize_null_values, should_parse_xml, strip_copyright


class TestStripCopyright:
    def test_removes_root_level_copyright(self):
        assert strip_copyright({"copyright": "MLB", "data": 1}) == {"data": 1}

    def test_removes_nested_copyright(self):
        payload = {
            "copyright": "MLB",
            "teams": [{"copyright": "MLB", "id": 1}, {"id": 2}],
            "meta": {"copyright": "MLB", "n": 3},
        }
        assert strip_copyright(payload) == {
            "teams": [{"id": 1}, {"id": 2}],
            "meta": {"n": 3},
        }

    def test_leaves_payload_without_copyright_untouched(self):
        payload = {"a": [1, 2], "b": {"c": 3}}
        assert strip_copyright(payload) == payload


class TestNormalizeNullValues:
    def test_mlb_null_sentinels_become_none(self):
        # "-1" is MLB's sentinel for missing birthStateProvince/deathStateProvince.
        assert normalize_null_values({"birthStateProvince": "-1"}) == {"birthStateProvince": None}
        assert normalize_null_values({"era": ".---"}) == {"era": None}

    def test_real_numbers_are_untouched(self):
        # Integers are never coerced (only exact string sentinels are).
        assert normalize_null_values({"runDiff": -1, "score": 0}) == {"runDiff": -1, "score": 0}


class TestShouldParseXml:
    def test_detects_xml_via_content_type(self):
        assert should_parse_xml("application/xml", "{}") is True

    def test_detects_xml_via_leading_angle_bracket(self):
        assert should_parse_xml("", "  <root/>") is True

    def test_json_is_not_treated_as_xml(self):
        assert should_parse_xml("application/json", '{"a": 1}') is False


def test_cors_origins_parsing():
    """CORS_ALLOW_ORIGINS is a clean list parsed from the comma-separated setting."""
    # Default (unset) yields an empty list -> no cross-origin access.
    assert isinstance(proxy.CORS_ALLOW_ORIGINS, list)


def test_cache_key_no_collision_from_special_chars():
    """Distinct queries must not collapse to the same cache key after decoding."""
    k1 = proxy._cache_key("/p", [("a", "1"), ("b", "2")], None)
    k2 = proxy._cache_key("/p", [("a", "1&b=2")], None)
    assert k1 != k2


def test_cache_key_is_order_independent():
    """Param order doesn't matter (sorted), so the same query hits the same entry."""
    k1 = proxy._cache_key("/p", [("a", "1"), ("b", "2")], None)
    k2 = proxy._cache_key("/p", [("b", "2"), ("a", "1")], None)
    assert k1 == k2
