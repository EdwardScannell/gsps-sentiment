"""Phase 1: only listed organizational publishers are read."""

from __future__ import annotations

from pathlib import Path

import pytest

from gsps_sentiment import Allowlist, normalize_host
from tests.conftest import ALLOWLIST


@pytest.fixture
def allowlist() -> Allowlist:
    return Allowlist.load(ALLOWLIST)


def test_listed_publisher_is_allowed_with_its_version(allowlist: Allowlist) -> None:
    d = allowlist.check("https://stats.example.gov/release/2026-10")
    assert d.allowed
    assert d.publisher == "Example Statistics Office"
    assert d.kind == "agency"
    assert d.allowlist_version == "20261112"


def test_unlisted_domain_is_refused(allowlist: Allowlist) -> None:
    d = allowlist.check("https://forum.example.net/thread/1")
    assert not d.allowed
    assert "not on the allowlist" in d.reason
    assert d.allowlist_version == "20261112"


@pytest.mark.parametrize(
    "url",
    [
        "https://www.newsroom.example.com/a",
        "https://NEWSROOM.example.com/a",
        "https://newsroom.example.com:8443/a",
        "https://business.newsroom.example.com/a",
    ],
)
def test_www_case_port_and_subdomains_resolve_to_the_listed_domain(
    allowlist: Allowlist, url: str
) -> None:
    assert allowlist.check(url).publisher == "Example Daily News"


def test_lookalike_domain_is_not_a_subdomain(allowlist: Allowlist) -> None:
    assert not allowlist.check("https://evilnewsroom.example.com/a").allowed
    assert not allowlist.check("https://newsroom.example.com.evil.example/a").allowed


@pytest.mark.parametrize("url", ["ftp://stats.example.gov/x", "stats.example.gov/x", ""])
def test_only_http_and_https_are_read(allowlist: Allowlist, url: str) -> None:
    d = allowlist.check(url)
    assert not d.allowed
    assert "http and https" in d.reason


def test_normalize_host() -> None:
    assert normalize_host("https://WWW.Example.org:443/x") == "example.org"
    assert normalize_host("mailto:someone@example.org") is None


def test_allowlist_file_must_be_dated(tmp_path: Path) -> None:
    bad = tmp_path / "allowlist.csv"
    bad.write_text("domain,publisher,kind\n", encoding="utf-8")
    with pytest.raises(ValueError, match="ALLOWLIST_YYYYMMDD"):
        Allowlist.load(bad)


def test_allowlist_rejects_duplicates_and_blank_rows(tmp_path: Path) -> None:
    path = tmp_path / "ALLOWLIST_20261112.csv"
    path.write_text(
        "domain,publisher,kind\na.example,A,news\nwww.a.example,A again,news\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="listed twice"):
        Allowlist.load(path)
    path.write_text("domain,publisher,kind\nb.example,,news\n", encoding="utf-8")
    with pytest.raises(ValueError, match="needs a domain, publisher and kind"):
        Allowlist.load(path)
