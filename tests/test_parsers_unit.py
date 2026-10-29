"""Unit tests for letterboxdpy/utils/utils_parser.py functions."""

import pytest
from bs4 import BeautifulSoup

from letterboxdpy.utils.utils_parser import (
    extract_and_convert_shorthand,
    extract_json_ld_script,
    get_body_content,
    get_meta_content,
    parse_iso_date,
    parse_rating,
    parse_review_text,
    parse_written_date,
    try_parse,
)


class TestExtractAndConvertShorthand:
    """Tests for extract_and_convert_shorthand parser."""

    @pytest.mark.parametrize(
        ("input_text", "expected"),
        [
            ("42", 42),
            ("0", 0),
            ("1,234", 1234),
            ("6.3K", 6300),
            ("6.3k", 6300),
            ("1.2M", 1200000),
            ("1.2m", 1200000),
            ("10 K", 10000),
            (" 500 ", 500),
            ("0.5K", 500),
            ("", 0),
            (None, 0),
            ("N/A", 0),
            ("no number here", 0),
        ],
    )
    def test_shorthand_string_values(self, input_text, expected):
        assert extract_and_convert_shorthand(input_text) == expected

    def test_shorthand_with_soup_tag(self):
        soup = BeautifulSoup("<span>12.5K</span>", "html.parser")
        tag = soup.find("span")
        assert extract_and_convert_shorthand(tag) == 12500


class TestParseRating:
    """Tests for parse_rating supporting SVG glyphs and legacy CSS classes."""

    def test_svg_rating_with_aria_label(self):
        html = '<span class="rating"><svg class="glyph -rating" aria-label="★★★★½"></svg></span>'
        soup = BeautifulSoup(html, "html.parser")
        assert parse_rating(soup.find("span")) == 4.5

    def test_svg_rating_full_stars(self):
        html = '<svg class="glyph -rating" aria-label="★★★"></svg>'
        soup = BeautifulSoup(html, "html.parser")
        assert parse_rating(soup.find("svg")) == 3.0

    def test_svg_rating_half_star(self):
        html = '<svg class="glyph -rating" aria-label="½"></svg>'
        soup = BeautifulSoup(html, "html.parser")
        assert parse_rating(soup.find("svg")) == 0.5

    def test_svg_rating_with_title_tag(self):
        html = '<svg class="glyph -rating"><title>★★★★</title></svg>'
        soup = BeautifulSoup(html, "html.parser")
        assert parse_rating(soup.find("svg")) == 4.0

    @pytest.mark.parametrize(
        ("css_class", "expected"),
        [
            ("rated-1", 0.5),
            ("rated-2", 1.0),
            ("rated-7", 3.5),
            ("rated-10", 5.0),
        ],
    )
    def test_legacy_class_ratings(self, css_class, expected):
        html = f'<span class="{css_class}">Rated</span>'
        soup = BeautifulSoup(html, "html.parser")
        assert parse_rating(soup.find("span")) == expected

    def test_unrated_or_empty(self):
        html = '<span class="no-rating">Unrated</span>'
        soup = BeautifulSoup(html, "html.parser")
        assert parse_rating(soup.find("span")) is None
        assert parse_rating(None) is None


class TestTryParse:
    """Tests for try_parse conversion helper."""

    def test_successful_conversions(self):
        assert try_parse("123", int) == 123
        assert try_parse("12.34", float) == 12.34
        assert try_parse(123, int) == 123
        assert try_parse(123, str) == "123"

    def test_failed_conversions(self):
        assert try_parse("abc", int) is False
        assert try_parse(None, int) is False
        assert try_parse([1, 2], int) is False


class TestDateParsers:
    """Tests for parse_iso_date and parse_written_date."""

    def test_parse_iso_date_standard(self):
        result = parse_iso_date("2025-01-01T00:00:00Z")
        assert "2025-01-01" in result

    def test_parse_written_date_standard(self):
        result = parse_written_date("01 Jan 2025")
        assert "2025-01-01" in result

    def test_parse_written_date_invalid(self):
        with pytest.raises(ValueError, match="Error parsing written date format"):
            parse_written_date("invalid date format")


class TestReviewTextParser:
    """Tests for parse_review_text handling spoilers and paragraphs."""

    def test_clean_review(self):
        html = """
        <div class="review">
            <div class="body-text js-review-body">
                <p>First paragraph.</p>
                <p>Second paragraph.</p>
            </div>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        text, spoiler = parse_review_text(soup.find("div", class_="review"))
        assert text == "First paragraph.\nSecond paragraph."
        assert spoiler is False

    def test_spoiler_review_with_inline_warning(self):
        html = """
        <div class="review">
            <div class="body-text js-review-body">
                <p class="contains-spoilers">This review contains spoilers.</p>
                <p>The main plot twist revealed.</p>
            </div>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        text, spoiler = parse_review_text(soup.find("div", class_="review"))
        assert text == "The main plot twist revealed."
        assert spoiler is True

    def test_empty_review_element(self):
        text, spoiler = parse_review_text(None)
        assert text == ""
        assert spoiler is False


class TestMetaAndJsonLdParsers:
    """Tests for get_meta_content, get_body_content, and extract_json_ld_script."""

    def test_get_meta_content_property_and_name(self):
        html = """
        <html>
            <head>
                <meta property="og:title" content="Inception" />
                <meta name="description" content="A mind-bending thriller" />
            </head>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert get_meta_content(soup, property="og:title") == "Inception"
        assert get_meta_content(soup, name="description") == "A mind-bending thriller"
        assert get_meta_content(soup, property="nonexistent") is None

    def test_get_body_content(self):
        html = '<body data-owner="nmcassa" class="logged-in"></body>'
        soup = BeautifulSoup(html, "html.parser")
        assert get_body_content(soup, "data-owner") == "nmcassa"
        assert get_body_content(soup, "class") == ["logged-in"]

    def test_extract_json_ld_script(self):
        html = """
        <script type="application/ld+json">
        /* <![CDATA[ */
        {"@type": "Movie", "name": "Parasite", "director": "Bong Joon-ho"}
        /* ]]> */
        </script>
        """
        soup = BeautifulSoup(html, "html.parser")
        data = extract_json_ld_script(soup)
        assert data is not None
        assert data.get("name") == "Parasite"
        assert data.get("director") == "Bong Joon-ho"

    def test_extract_json_ld_missing_or_corrupt(self):
        html = "<script>var x = 1;</script>"
        soup = BeautifulSoup(html, "html.parser")
        assert extract_json_ld_script(soup) is None


class TestExtractAuthor:
    """Tests for extract_author in user_list page parser."""

    def test_extract_author_with_badge(self):
        from letterboxdpy.pages.user_list import extract_author

        html = """
        <div class="person-summary -inline">
          <h1 class="title-4">
            <small class="context">List by</small>
            <a class="name" href="/bugracoskun/">
              <span>bugra</span>
              <span class="badge -patron -small">Patron</span>
            </a>
          </h1>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert extract_author(soup) == "bugra"

    def test_extract_author_without_badge(self):
        from letterboxdpy.pages.user_list import extract_author

        html = """
        <div class="person-summary -inline">
          <h1 class="title-4">
            <small class="context">List by</small>
            <a class="name" href="/johndoe/">
              <span>John Doe</span>
            </a>
          </h1>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        assert extract_author(soup) == "John Doe"

    def test_extract_author_legacy_itemprop(self):
        from letterboxdpy.pages.user_list import extract_author

        html = """<div><span itemprop="name">Jane Doe</span></div>"""
        soup = BeautifulSoup(html, "html.parser")
        assert extract_author(soup) == "Jane Doe"
