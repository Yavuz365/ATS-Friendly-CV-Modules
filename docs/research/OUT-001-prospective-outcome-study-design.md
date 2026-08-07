# OUT-001 — Prospective Outcome Study Design (skeleton)

**Status:** Design only. No participant recruitment. No outcome data collected.  
**Date:** 2026-08-07

## Goal

Define *how* hiring / progression outcomes could later be linked to engine
decisions **before** any calibration that uses those outcomes.

## Non-goals (now)

- Collecting real candidate or employer data
- Publishing predictive accuracy claims
- Calibrating scores on outcomes

## Proposed design axes (to be approved by human)

| Axis | Options to decide |
|------|-------------------|
| Unit of analysis | application event / candidate-role pair |
| Primary endpoint | interview invite / offer / hire / 90-day retention |
| Censoring | explicit `outcome_observed=false` + reason (already in ApplicationEvent) |
| Consent | required before any personal linkage |
| Minimum n | TBD — not powered yet |
| Analysis plan | pre-registered before data look |

## Dependency

Requires stable ApplicationEvent store (OPS-001 path) and explicit ethics/
consent review. Until then this document is **not** an active study.

## Measurement status

`NOT_STARTED` — design artifact only.
