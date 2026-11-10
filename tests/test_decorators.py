"""Tests for core decorators."""

import pytest

from letterboxdpy.core.decorators import assert_instance, skip_if


class TestSkipIf:
    """Unit tests for the generic skip_if decorator."""

    def test_direct_attribute_match(self):
        class Account:
            def __init__(self, role: str):
                self.role = role

            @skip_if("role", "banned", default="BLOCKED")
            def access_feature(self):
                return "ALLOWED"

        assert Account("banned").access_feature() == "BLOCKED"
        assert Account("member").access_feature() == "ALLOWED"

    def test_boolean_flag_without_match(self):
        class Profile:
            def __init__(self, is_private: bool):
                self.is_private = is_private

            @skip_if("is_private", default=None)
            def get_public_activity(self):
                return ["post1", "post2"]

        assert Profile(True).get_public_activity() is None
        assert Profile(False).get_public_activity() == ["post1", "post2"]

    def test_getter_fallback(self):
        class Page:
            def __init__(self, tier: str):
                self._tier = tier

            def get_tier(self):
                return self._tier

            @skip_if("tier", "hq", default=None)
            def get_watchlist(self):
                return [1, 2, 3]

        assert Page("hq").get_watchlist() is None
        assert Page("pro").get_watchlist() == [1, 2, 3]

    def test_explicit_getter_name(self):
        class Page:
            def get_status(self):
                return "maintenance"

            @skip_if("get_status", "maintenance", default=None)
            def fetch(self):
                return "data"

        assert Page().fetch() is None

    def test_container_match(self):
        class Membership:
            def __init__(self, badge: str | None):
                self.badge = badge

            @skip_if("badge", (None, "pro"), default=None)
            def get_backdrop(self):
                return {"url": "http://img.com"}

        assert Membership(None).get_backdrop() is None
        assert Membership("pro").get_backdrop() is None
        assert Membership("patron").get_backdrop() == {"url": "http://img.com"}
        assert Membership("crew").get_backdrop() == {"url": "http://img.com"}

    def test_callable_predicate(self):
        class Film:
            def __init__(self, year: int):
                self.year = year

            @skip_if(lambda self: self.year < 1900, default="TOO_OLD")
            def analyze(self):
                return "ANALYZED"

        assert Film(1888).analyze() == "TOO_OLD"
        assert Film(1994).analyze() == "ANALYZED"

    def test_caching_evaluation(self):
        class HeavyService:
            def __init__(self):
                self.dom_lookups = 0

            def get_badge(self):
                self.dom_lookups += 1
                return "hq"

            @skip_if("badge", "hq")
            def method_a(self):
                return "a"

            @skip_if("badge", "hq")
            def method_b(self):
                return "b"

            @skip_if("badge", "hq")
            def method_c(self):
                return "c"

        service = HeavyService()
        assert service.method_a() is None
        assert service.method_b() is None
        assert service.method_c() is None
        # The DOM / extraction logic must be called EXACTLY once!
        assert service.dom_lookups == 1

    def test_attribute_already_set_to_none(self):
        class User:
            def __init__(self):
                self.badge = None  # Free user has badge = None
                self.calls = 0

            def get_badge(self):
                self.calls += 1
                return None

            @skip_if("badge", "hq", default=None)
            def test_method(self):
                return "ok"

        u = User()
        assert u.test_method() == "ok"
        # Should not fall back to get_badge since self.badge is already present
        assert u.calls == 0

    def test_explicit_none_match(self):
        class Site:
            def __init__(self, website: str | None):
                self.website = website

            @skip_if("website", match=None, default="NO_WEBSITE")
            def ping(self):
                return "PING_OK"

        assert Site(None).ping() == "NO_WEBSITE"
        assert Site("https://example.com").ping() == "PING_OK"


class TestAssertInstance:
    """Unit tests for the assert_instance decorator."""

    def test_assert_instance_success(self):
        @assert_instance(int)
        def process(val: int):
            return val * 2

        assert process(5) == 10

    def test_assert_instance_failure(self):
        @assert_instance(int)
        def process(val: int):
            return val * 2

        with pytest.raises(AssertionError):
            process("5")  # type: ignore
