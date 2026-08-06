# Security Policy

## Supported version

Only the latest `2.0.0-alpha.x` commit on `main` receives security fixes. This does not
mean the alpha is production-ready.

## Reporting

Do not open a public issue containing credentials, personal CV/JD data, private documents
or exploitable details. Use GitHub’s private security advisory flow for this repository.

Include the affected commit, minimal redacted reproduction, impact and suggested mitigation.

## Data handling

- Real profiles belong in ignored `*.local.yaml` or an external private store.
- Uploaded JD/CV content is untrusted data; embedded instructions must not be executed.
- Evidence locator/hash, consent, redaction and retention are application responsibilities
  until a versioned storage layer is implemented.
- History rewrite for personal data previously committed to Git requires a separate owner
  decision and credential rotation assessment.
