# Binary two-root proper forest campaign

Status: ready_for_expert_review.
Allocation recorded at campaign start: 40 rounds; 1 started and completed,
39 unused. Discovery stopped early on a complete reviewed rule; writing and
verification did not consume extra rounds. The user's continuation allowance
was not filled with redundant attempts.
Fixed target: 3-Uniform Set Splitting → binary two-root Proper Forest-Based Recognition.

Result: deterministic linear-graph-size Karp reduction, general YES/NO proof,
and polynomial recovery from every valid target forest. The target is NP-complete.
[Algorithm](work/algorithm.py), [proof](work/proof.md), [six-page paper](work/manuscript.pdf).
No known correctness gap remains; human assessment and broader novelty coverage
remain outstanding. Importance: moderate, a named recognition boundary.

[Verification](work/verification.md): 1,088 exhaustive/seeded cases and 2,160
recoveries; 9 prepared cases and 21 recoveries; a separate verifier's 37 cases
and 112 recoveries. Suite counts are not deduplicated. Latest independent
[review](reviews/initial/review.md): advance, with 73 independently checked
recoveries. Candidate unchanged after review. [Layout inspection](work/evidence/layout/inspection.md)
completed; only editorial artifacts changed after passing checks.

Experience: 1 new entry, 0 updated, 0 pending:
[binary reticulation stacks](../../research/experience/binary-reticulation-stack-nae.md).
Next: expert mathematical and novelty assessment. No publishing or production
integration has occurred.

| Round | Status |
|---|---|
| [1](rounds/001/round.md) | Complete: binary NAE construction, every-forest recovery, tests, independent advance review and inspected paper |
