"""gsps-sentiment: stance and sentiment from organizational publishers, graded with GSPS.

Allowlist only: a source that is not on the allowlist is never read. No identities are
stored: author, byline and handle fields are dropped at ingest.
"""

from gsps_sentiment.allowlist import AllowDecision, Allowlist, Publisher, normalize_host
from gsps_sentiment.claim import Claim, IngestResult, Stance, claim_from_article

__version__ = "0.1.0"

__all__ = [
    "AllowDecision",
    "Allowlist",
    "Claim",
    "IngestResult",
    "Publisher",
    "Stance",
    "__version__",
    "claim_from_article",
    "normalize_host",
]
