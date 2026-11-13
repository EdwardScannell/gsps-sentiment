# gsps-sentiment

**Stance and sentiment from organizational publishers, graded by source quality with
[GSPS](https://github.com/EdwardScannell/gsps).**

Most sentiment tools count every voice the same. gsps-sentiment asks two questions about
each claim: *what does it say about the topic*, and *how much should it count*. A
statistical agency's release and a vendor's blog post can point the same way and deserve
very different weight.

[![CI](https://github.com/EdwardScannell/gsps-sentiment/actions/workflows/ci.yml/badge.svg)](https://github.com/EdwardScannell/gsps-sentiment/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-Apache--2.0-green)

## Safe by design

| Rule | What it means |
|---|---|
| **Allowlist only** | Only organizational publishers on a dated allowlist (news outlets, statistical agencies, research institutes, company newsrooms) are read. Anything else is refused. |
| **No identities stored** | Author, byline and handle fields are dropped at ingest. A claim keeps its publisher, never a person. See [`PRIVACY.md`](PRIVACY.md). |
| **No routing around a refusal** | A refused source is never fetched through a mirror, cache or scraper. |
| **No network in the core** | Fetching is plugged in from outside (see [gsps-fetch](https://github.com/EdwardScannell/gsps-fetch)). |

## Who it's for

Researchers, analysts and editors who track how organizations are talking about a topic
and need to show which sources the picture rests on: market research, policy briefs,
investor memos, media monitoring.

## Built with

- **Python 3.11+**, fully typed (`mypy --strict`)
- **pydantic** for records; plain CSV for the allowlist
- **pytest** with coverage, **ruff**, **GitHub Actions** CI on 3.11 to 3.13

## Install

```bash
pip install -e ".[dev]"     # from a clone
make check                  # lint, strict types, tests with coverage
```

## Status

Early. Built in seven phases; see [`ROADMAP.md`](ROADMAP.md) and the issues.

## License

Apache License 2.0. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
