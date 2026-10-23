# DI PMO harness repair check

## Finding

GitHub was connected. The prior changes are present on the remote, including `ffb90a0` (SI delivery and Lilian leadership) and the boot-contract observation commit `4a0134e`.

Connection did not establish compliance. In this thread I loaded the skill but did not perform all canonical startup reads before work. I missed `NARROWING.md` and `ACTIVE.md`, left the central recent-work pointer stale, and repeatedly delivered revisions the operator rejected. I installed project instructions after the failures rather than beginning from complete context. Those are agent failures, not evidence of a missing GitHub connection.

## Repair and observed tests

- Mandatory reads now precede task instructions in `AGENTS.md`.
- `scripts/preflight.py` verifies required sources and both template fingerprints.
- Release checks require approved state, exact reviewed bytes, a recorded approval reference and completed artifact-review fields.
- The actual current v3 is marked rejected in the private Project file repository.
- Unit tests: **3 passed**. Missing sources, rejected release and altered artifact bytes all fail.
- Actual entry command: **exit 0** after required inputs were present.
- Actual release command against v3: **exit 1**, blocked because the deck is unapproved and has no completed release evidence.

## Boundaries

This command is a repository workflow control, not a Perplexity runtime hook. An agent or tool can bypass it. Tests verify the coded checks, not deck quality, truthful self-attestation, model comprehension or future compliance. No new deck was generated as part of this repair.

The operator's cost and harm complaint is recorded in the central observation register. No credit amount, refund entitlement, charge reversal or platform-wide fix is asserted.
