"""Phase 1: claims keep the publisher and never a person."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest
from pydantic import ValidationError

from gsps_sentiment import Allowlist, Claim, Stance, claim_from_article
from tests.conftest import ALLOWLIST, ROOT

PERSON = "Jordan Example-Writer"
HANDLE = "@jordan_example"


def article(**kw: object) -> dict[str, object]:
    base: dict[str, object] = {
        "url": "https://institute.example.org/briefs/ai-screening",
        "claim": "AI resume screens now check claims against evidence.",
        "published_on": "2026-11-06",
        "topic": "hiring",
        "stance": "Supports",
        "author": PERSON,
        "Byline": f"By {PERSON}",
        "handle": HANDLE,
        "email": "jordan@example.org",
    }
    base.update(kw)
    return base


@pytest.fixture
def allowlist() -> Allowlist:
    return Allowlist.load(ALLOWLIST)


def test_allowed_article_becomes_a_claim_with_its_publisher(allowlist: Allowlist) -> None:
    result = claim_from_article(article(), allowlist)
    assert result.accepted and result.claim is not None
    assert result.claim.publisher == "Example Policy Institute"
    assert result.claim.publisher_kind == "research"
    assert result.claim.stance is Stance.SUPPORTS
    assert result.claim.allowlist_version == "20261112"


def test_identity_fields_are_dropped_and_their_values_stored_nowhere(
    allowlist: Allowlist,
) -> None:
    result = claim_from_article(article(), allowlist)
    assert result.dropped_identity_fields == ("Byline", "author", "email", "handle")
    stored = result.model_dump_json()
    for value in (PERSON, HANDLE, "jordan@example.org"):
        assert value not in stored


def test_a_claim_cannot_hold_an_author_field() -> None:
    with pytest.raises(ValidationError):
        Claim.model_validate(
            {
                "publisher": "P",
                "publisher_kind": "news",
                "url": "https://newsroom.example.com/a",
                "claim": "x",
                "published_on": "2026-11-12",
                "topic": "t",
                "stance": "neutral",
                "allowlist_version": "20261112",
                "author": PERSON,
            }
        )


def test_unlisted_source_yields_no_claim_and_still_drops_identities(
    allowlist: Allowlist,
) -> None:
    result = claim_from_article(article(url="https://blog.example.net/post"), allowlist)
    assert not result.accepted and result.claim is None
    assert "not on the allowlist" in result.decision.reason
    assert PERSON not in result.model_dump_json()


def test_unknown_non_identity_fields_are_reported_and_ignored(allowlist: Allowlist) -> None:
    result = claim_from_article(article(title="A headline", section="Jobs"), allowlist)
    assert result.ignored_fields == ("section", "title")
    assert result.claim is not None


def test_empty_claim_text_is_rejected(allowlist: Allowlist) -> None:
    with pytest.raises(ValidationError):
        claim_from_article(article(claim="   "), allowlist)


def test_unknown_stance_is_rejected(allowlist: Allowlist) -> None:
    with pytest.raises(ValueError):
        claim_from_article(article(stance="bullish"), allowlist)


def test_claims_are_frozen(allowlist: Allowlist) -> None:
    claim = claim_from_article(article(), allowlist).claim
    assert claim is not None
    with pytest.raises(ValidationError):
        claim.publisher = "edited"  # type: ignore[misc]


NETWORK_MODULES = {
    "socket",
    "ssl",
    "http.client",
    "urllib.request",
    "urllib3",
    "requests",
    "httpx",
    "aiohttp",
}


def _imports(path: Path) -> set[str]:
    found: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            found.add(node.module)
            found.update(f"{node.module}.{alias.name}" for alias in node.names)
    return found


def test_the_core_imports_no_network_library() -> None:
    offenders = {
        f"{path.relative_to(ROOT)}: {name}"
        for path in (ROOT / "src" / "gsps_sentiment").rglob("*.py")
        for name in _imports(path)
        if any(name == m or name.startswith(m + ".") for m in NETWORK_MODULES)
    }
    assert not offenders, sorted(offenders)
