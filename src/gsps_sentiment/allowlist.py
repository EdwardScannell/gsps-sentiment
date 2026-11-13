"""The allowlist: which organizational publishers may be read.

An allowlist is a dated CSV file, `ALLOWLIST_YYYYMMDD.csv`, with columns `domain`,
`publisher` and `kind`. The date in the file name is its version, and every decision
records it. A listed domain covers its subdomains. Anything not listed is refused.
A change to the allowlist is a new dated file, never an edit.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict

FILE_NAME = re.compile(r"^ALLOWLIST_(\d{8})\.csv$")
SCHEMES = {"http", "https"}


def normalize_host(url: str) -> str | None:
    """Lowercased host without `www.` or port; None unless the URL is http or https."""
    parts = urlsplit(url.strip())
    if parts.scheme.lower() not in SCHEMES or not parts.hostname:
        return None
    host = parts.hostname.lower().rstrip(".")
    return host.removeprefix("www.")


class Publisher(BaseModel):
    model_config = ConfigDict(frozen=True)

    domain: str
    publisher: str
    kind: str


class AllowDecision(BaseModel):
    """Whether a URL may be read, why, and under which allowlist version."""

    model_config = ConfigDict(frozen=True)

    url: str
    allowed: bool
    reason: str
    allowlist_version: str
    publisher: str = ""
    kind: str = ""


class Allowlist:
    """A dated set of organizational publishers. Refuses everything not listed."""

    def __init__(self, version: str, publishers: list[Publisher]) -> None:
        self.version = version
        self.publishers: dict[str, Publisher] = {}
        for p in publishers:
            domain = p.domain.strip().lower().removeprefix("www.")
            if not domain or not p.publisher.strip() or not p.kind.strip():
                raise ValueError("every allowlist row needs a domain, publisher and kind")
            if domain in self.publishers:
                raise ValueError(f"{domain} is listed twice")
            self.publishers[domain] = p.model_copy(update={"domain": domain})

    @classmethod
    def load(cls, path: Path) -> Allowlist:
        match = FILE_NAME.match(path.name)
        if not match:
            raise ValueError(f"{path.name}: an allowlist file is named ALLOWLIST_YYYYMMDD.csv")
        with path.open(newline="", encoding="utf-8") as fh:
            rows = [
                Publisher(
                    domain=(r.get("domain") or ""),
                    publisher=(r.get("publisher") or ""),
                    kind=(r.get("kind") or ""),
                )
                for r in csv.DictReader(fh)
            ]
        return cls(match.group(1), rows)

    def check(self, url: str) -> AllowDecision:
        host = normalize_host(url)
        if host is None:
            return AllowDecision(
                url=url,
                allowed=False,
                reason="only http and https URLs are read",
                allowlist_version=self.version,
            )
        # Most specific listed domain wins: the host itself, then each parent domain.
        labels = host.split(".")
        for i in range(len(labels) - 1):
            candidate = ".".join(labels[i:])
            listed = self.publishers.get(candidate)
            if listed is not None:
                return AllowDecision(
                    url=url,
                    allowed=True,
                    reason=f"listed: {candidate}",
                    allowlist_version=self.version,
                    publisher=listed.publisher,
                    kind=listed.kind,
                )
        return AllowDecision(
            url=url,
            allowed=False,
            reason=f"not on the allowlist: {host}",
            allowlist_version=self.version,
        )
