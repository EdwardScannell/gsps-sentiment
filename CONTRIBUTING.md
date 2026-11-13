# Contributing

## Setup

```bash
python -m venv .venv && . .venv/bin/activate
make install
make check           # lint, strict types, tests with coverage (must stay >= 90%)
```

## The rules for changes

1. **Allowlist only.** Never add a code path that reads a source not on the allowlist.
2. **No identities.** Never add a field that stores a person's name, handle, email or
   profile link. If a new input format carries one, drop it at ingest and add a test.
3. **No network in the core.** Fetching belongs to
   [gsps-fetch](https://github.com/EdwardScannell/gsps-fetch) or another plug-in.
4. **Never fold stances.** Supports, contradicts and complicates stay separate.
5. **Every bug gets a regression test first**, named after the failure it guards against.
6. **Keep the public API typed.** `mypy --strict` must pass.

## Allowlist changes

An allowlist change is a new dated file, never an edit to an existing one. Only
organizational publishers qualify; see the open issue on inclusion criteria.

## Fixtures and data

Fixtures are synthetic and use reserved `.example` domains. Do not add real articles,
personal data or anything you do not have the right to publish.
