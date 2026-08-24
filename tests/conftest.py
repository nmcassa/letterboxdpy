import base64
import gzip
import hashlib
import json
import re
from enum import Enum
from functools import cache
from http.client import responses as http_reasons
from pathlib import Path
from urllib.parse import urlparse

import pytest
from bs4 import BeautifulSoup
from curl_cffi.requests import Response
from curl_cffi.requests.headers import Headers

from letterboxdpy.core.scraper import Scraper

CASSETTES_DIR = Path(__file__).parent / "cassettes"


class VcrMode(str, Enum):
    ONCE = "once"
    RERECORD = "rerecord"
    DISABLE = "disable"


def pytest_addoption(parser):
    parser.addoption(
        "--vcr-record",
        default=VcrMode.ONCE,
        choices=[mode.value for mode in VcrMode],
        help=(
            f"{VcrMode.ONCE.value + ':':10}record if no cassette exists, replay if exists (default)\n"
            f"{VcrMode.RERECORD.value + ':':10}record cassettes even if they already exist\n"
            f"{VcrMode.DISABLE.value + ':':10}disable replays, always make real requests"
        ),
    )


def _strip_redundant_tags(content: bytes, content_type: str) -> bytes:
    if "html" not in content_type.lower():
        return content
    try:
        soup = BeautifulSoup(content, "html.parser")
    except Exception:
        return content

    for tag in soup.find_all("script"):
        if tag.get("type") not in ("application/json", "application/ld+json"):
            tag.decompose()

    for tag in soup.find_all(["noscript", "link", "path"]):
        tag.decompose()

    for tag in soup.select(
        "span.flag, footer, section#film-hq-mentions,"
        "div#poster-picker-modal, div#backdrop-picker-modal, div#remove-ads-modal"
    ):
        tag.decompose()

    return soup.encode(formatter="minimal")


def _url_to_cassette_path(method: str, url: str) -> Path:
    parsed = urlparse(url)

    # Build readable part: host + path
    readable = parsed.netloc + parsed.path
    readable = re.sub(r"[^a-zA-Z0-9\-_]", "_", readable)
    readable = re.sub(r"_+", "_", readable).strip("_")
    readable = readable[:120]

    # Short hash for uniqueness (includes method, full URL with query)
    url_hash = hashlib.sha256(f"{method}:{url}".encode()).hexdigest()[:12]

    return CASSETTES_DIR / f"{readable}_{url_hash}.json.gz"


def _save_cassette(path: Path, method: str, request_url: str, resp) -> None:
    content_type = resp.headers.get("content-type", "")
    content = _strip_redundant_tags(resp.content, content_type)
    entry = {
        "method": method,
        "request_url": request_url,
        "response_url": str(getattr(resp, "url", request_url)),
        "status_code": resp.status_code,
        "reason": getattr(resp, "reason", ""),
        "content_b64": base64.b64encode(content).decode("ascii"),
        "headers": dict(resp.headers),
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    raw_json = json.dumps(entry, indent=2, ensure_ascii=False).encode("utf-8")
    path.write_bytes(gzip.compress(raw_json, compresslevel=9))

    # for debugging the raw html is stored on disc (but ignored via .gitignore)
    path.with_suffix(".stripped.html").write_bytes(content)
    path.with_suffix(".full.html").write_bytes(resp.content)


def _load_cassette(path: Path) -> Response:
    entry = json.loads(gzip.decompress(path.read_bytes()))
    status_code = entry["status_code"]
    resp = Response()
    resp.status_code = status_code
    resp.content = base64.b64decode(entry["content_b64"])
    resp.headers = Headers(entry["headers"])
    resp.url = entry.get("response_url", entry.get("url", ""))
    resp.reason = entry.get("reason", "") or http_reasons.get(status_code, "Unknown")
    resp.ok = 200 <= status_code < 400
    return resp


@pytest.fixture(autouse=True, scope="session")
def curl_vcr(request):
    mode = VcrMode(request.config.getoption("--vcr-record"))

    original_descriptor = Scraper.__dict__["_fetch"]
    original_fetch = Scraper._fetch

    # Use a small in-memory cache, so that even the "rerecord" mode only needs to call every request once per test run.
    @cache
    def caching_fetch(url: str) -> Response:
        cassette = _url_to_cassette_path("GET", url)

        if mode is VcrMode.ONCE and cassette.exists():
            return _load_cassette(cassette)
        else:
            real_resp = original_fetch(url)
            _save_cassette(cassette, "GET", url, real_resp)
            return real_resp

    if mode is not VcrMode.DISABLE:
        Scraper._fetch = caching_fetch

    yield

    Scraper._fetch = original_descriptor
