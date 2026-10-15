# Independent testing foundation

The source oracle exhaustively checks every bit assignment on the stated small
source domain. This textbook cross-check makes the nine stored answers independent
of the candidate; the largest source has seven vertices. The Fano triples are NO,
and deleting the final triple is YES. These statements were verified exhaustively.

Z3 5.1.0 models selected forest arcs and two component labels. An arc is selected
exactly when its endpoints share a component; each nonroot has exactly one selected
incoming arc and each internal vertex at least one selected outgoing arc. The two
roots have different labels. Since the input is a DAG, these constraints give two
rooted spanning trees with exactly the required leaves and crossing omitted arcs.
Returned forests are independently validated by explicit weak components, degrees,
and the omitted-arc condition. Only sat/unsat are accepted; unknown fails.

The self-test checks nine source cases, all two forests of a six-vertex YES
network, a ten-vertex valid NO network whose reticulation has necessarily equally
colored parents, invalid source witnesses and malformed target degree patterns.
[Latest output](evidence/preparation/self-test.json); the earlier baseline output
is preserved next to it. Command: `python3 check.py --self-test` from work/.
Deliberately incorrect subprocess fixtures will exercise the complete harness
before the candidate is submitted for review. No wall-clock timeout is used.

The complete subprocess harness rejects both an always-NO forward fixture and an
all-zero recovery fixture: [fault-check output](evidence/preparation/fault-check.json).
Their stderr logs and scripts are preserved alongside it. Three malformed serialized
inputs, including a 5,001-digit illegal label, map to the legal constant NO target.
A reachable cycle in a purported forest is rejected. These boundary checks are
separate from the mathematical source/target comparisons.
