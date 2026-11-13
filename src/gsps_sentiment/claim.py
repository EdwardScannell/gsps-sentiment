"""The claim record, and ingest that keeps publishers and drops people.

A `Claim` has no field that could hold a person's name, handle or email, and it rejects
unknown fields, so identity data cannot be stored by accident. `claim_from_article`
checks the allowlist first, drops identity fields, and reports only the *names* of the
fields it dropped, never their values.
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from gsps_sentiment.allowlist import AllowDecision, Allowlist

IDENTITY_FIELDS = frozenset(
    {
        "author",
        "authors",
        "author_email",
        "author_url",
        "byline",
        "contributor",
        "email",
        "handle",
        "profile",
        "profile_url",
        "screen_name",
        "twitter",
        "user",
        "user_name",
        "username",
        "x_handle",
    }
)

CLAIM_INPUTS = ("claim", "published_on", "topic", "stance")


class Stance(StrEnum):
    """How a claim bears on its topic. Never folded into one another."""

    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    COMPLICATES = "complicates"
    NEUTRAL = "neutral"


class Claim(BaseModel):
    """One claim from one organizational publisher. No person is recorded."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    publisher: str
    publisher_kind: str
    url: str
    claim: str = Field(min_length=1)
    published_on: str
    topic: str
    stance: Stance
    allowlist_version: str


class IngestResult(BaseModel):
    """The outcome of ingesting one article record."""

    model_config = ConfigDict(frozen=True)

    decision: AllowDecision
    claim: Claim | None = None
    dropped_identity_fields: tuple[str, ...] = ()
    ignored_fields: tuple[str, ...] = ()

    @property
    def accepted(self) -> bool:
        return self.claim is not None


def is_identity_field(name: str) -> bool:
    return name.strip().lower() in IDENTITY_FIELDS


def claim_from_article(raw: Mapping[str, object], allowlist: Allowlist) -> IngestResult:
    """Turn one article record into a claim, or refuse it.

    The allowlist is checked first; a refused record yields no claim. Identity fields
    are dropped in every case and named in the result, without their values.
    """
    url = str(raw.get("url", "")).strip()
    decision = allowlist.check(url)
    dropped = tuple(sorted(k for k in raw if is_identity_field(k)))
    ignored = tuple(
        sorted(k for k in raw if not is_identity_field(k) and k != "url" and k not in CLAIM_INPUTS)
    )
    if not decision.allowed:
        return IngestResult(
            decision=decision, dropped_identity_fields=dropped, ignored_fields=ignored
        )
    claim = Claim(
        publisher=decision.publisher,
        publisher_kind=decision.kind,
        url=url,
        claim=str(raw.get("claim", "")).strip(),
        published_on=str(raw.get("published_on", "")).strip(),
        topic=str(raw.get("topic", "")).strip(),
        stance=Stance(str(raw.get("stance", "")).strip().lower()),
        allowlist_version=decision.allowlist_version,
    )
    return IngestResult(
        decision=decision, claim=claim, dropped_identity_fields=dropped, ignored_fields=ignored
    )
