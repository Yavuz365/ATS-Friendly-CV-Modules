# OPS-002 / OPS-003 / OPS-004 — Integration Stubs

**Status:** Documentation stubs only. No live connections.  
**Date:** 2026-08-07

| ID | Target | Blocker |
|----|--------|--------|
| OPS-002 | GitHub + Notion + Drive + one work tracker | OAuth / API tokens + workspace choice |
| OPS-003 | MySQL + Metabase outcome dashboards | DB credentials + hosting |
| OPS-004 | OpenClaw / n8n / agent orchestration | Runtime + secrets + policy |

## Policy

- Do not commit secrets.
- Do not claim integration “done” without a successful authenticated read/write probe recorded in provenance.
- Prefer read-only first for Notion/Drive.

## Next human actions

1. Choose tracker of record (Linear / GitHub Issues / other).
2. Grant least-privilege tokens to a dedicated bot account.
3. Record first successful probe under EVAL-002 provenance log.
