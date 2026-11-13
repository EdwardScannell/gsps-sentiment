# Roadmap

gsps-sentiment is built in seven phases. Each lands as its own pull request with tests,
and CI stays green on every commit.

1. [ ] **Claim record, allowlist, identity drop.** A claim keeps publisher, URL, text,
   date, topic and stance; a dated allowlist decides which publishers are read; author,
   byline and handle fields are dropped at ingest and cannot be stored.
2. [ ] **PII filter for claim text.** Remove person names and @handles from claim text
   (quotes, embedded posts), driven by pattern lists kept as data files.
3. [ ] **Sentiment scorer interface and baseline.** A typed scorer interface and a simple,
   reproducible baseline scorer.
4. [ ] **GSPS grading on every score.** Each score carries its source's grade and
   confidence: the publisher's own release counts more than a vendor's commentary.
5. [ ] **Source policy from gsps-fetch, with a blocklist guard.** Adopt gsps-fetch's dated
   allow and block lists; platforms such as Reddit and X are refused even if allowlisted.
6. [ ] **PII filter maintenance and audit.** Versioned pattern lists, a regression test for
   every miss, and an audit report of what was removed (counts and field names, never
   values).
7. [ ] **Command line and reports.** Per-topic summaries with thin, contrary and
   vendor-heavy flags.

## Never

- Social platforms, forums, comment sections or personal blogs as sources.
- Storing author names, handles, emails or profile links.
- Scraping, crawling, login or paywall handling.
