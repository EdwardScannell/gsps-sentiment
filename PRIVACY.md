# Privacy

gsps-sentiment is built to work with what organizations publish, not with people.

- **Allowlist only.** Sources are limited to organizational publishers on a dated
  allowlist. Social platforms, forums, comment sections and personal blogs are never on it.
- **No identities stored.** Author, byline, handle, username, email and profile fields are
  dropped when a record is ingested. The stored claim has no field that could hold them.
  The ingest report lists only the *names* of the fields dropped, never their values.
- **Claim text.** Removing names and handles that appear inside quoted text is planned
  (roadmap phase 2) with a maintenance and audit process (phase 6).
- **Fixtures** are synthetic and use reserved `.example` domains.
