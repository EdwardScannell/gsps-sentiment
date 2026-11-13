# Changelog

All notable changes are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Phase 1 of 7: `Claim` record (publisher, URL, text, date, topic, stance, allowlist
  version) that rejects unknown fields, so no person can be stored; `Allowlist` from a
  dated `ALLOWLIST_YYYYMMDD.csv` with www, case, port and subdomain handling and
  lookalike-domain protection; `claim_from_article`, which refuses unlisted sources and
  drops identity fields, reporting their names but never their values.
- A test that fails if any core module imports a network library.
- Project scaffold: packaging, strict typing, lint, tests and CI on Python 3.11 to 3.13.
