# Round 1 — Compose binary NAE clauses with opposite-color rails

## Plan

Build the complete Set Splitting reduction using two freely colored reticulations
per source element, an opposite-color enforcer, binary color-copy trees with
private-leaf ports, and the screened clause interface. Each clause uses one tree
vertex and four reticulations; reticulation stacks intentionally violate the
known polynomial tree-child restriction. The output must remain a weakly connected
binary two-root DAG on every well-formed source, regardless of its answer.

Implement extraction from every valid spanning forest by finding which of the
two distinguished roots owns each positive rail. Treat malformed source inputs
with one constant legal NO network. The empty universe uses one dummy element
whose color is discarded in recovery. Prove general correctness and exact size
bounds; compare the actual outputs with independent source/forest oracles.

Finite scope: the nine prepared cases; all 1,024 triple families on five elements;
64 seeded seven-element hypergraphs; multiple solver-generated target forests;
separate verification and a native review if all obligations pass. No hidden
expansion is authorized within this round. Routine repairs do not start a round.
The screened local interface is the supporting evidence. No relevant previous
experience entry about this construction was found; other network reductions
have different witness semantics and are not reused.

## Evidence and diagnosis

Full composition and recovery passed the [verification suites](../../work/verification.md).
The candidate has N=20 max(1,n)+22m-2 vertices and E=23 max(1,n)+26m-4 arcs;
the exhaustive suite checks these identities on its actual outputs. The general
proof gives both directions, legal outputs, and arbitrary-forest recovery.
The only implementation repairs added bounded rejection of malformed recovery
cycles and explicit malformed-JSON mapping; neither changed the graph mechanism.
A pre-JSON-boundary snapshot and all test outputs are retained.

No mathematical counterexample has been found. Finite tests are not a general
proof or novelty assessment. Experience extraction: one general construction finding is ready for post-campaign
storage as `research/experience/binary-reticulation-stack-nae.md`: a binary
reticulation stack transmits an externally constrained bit, while private-leaf
ports prevent unintended constraints on supplies. Independent review supports
the exact premises; no measured cross-campaign search benefit is claimed.
One construction family; 1,088 exhaustive/seeded source instances, 9 prepared and
37 separate verification cases. Counts are suite counts, not deduplicated totals.
Time/token totals unavailable.

## Closure

Completed one construction family in one round. The independent
[review](../../reviews/initial/review.md) advances correctness, novelty within
inspected literature, and significance. Its own checks recover 73 witnesses.
The six-page [manuscript](../../work/manuscript.pdf) contains the full rule,
proof, three checked vector figures, and reproduction appendix; all pages were
inspected. Writing introduced no new mathematical mechanism or additional round.

Decision: ready for expert review; stop discovery early on this fixed target.
The construction uses private leaves to separate supply feasibility from the
clause's child constraints. This is the reusable lesson; finite verification is
not its all-input proof. One [experience entry](../../../../research/experience/binary-reticulation-stack-nae.md)
was saved at closeout, with zero pending findings. Human correctness and novelty assessment remain
outstanding. No production integration or publication was performed.
