# Verification evidence

The current rule consists of algorithm.py's forward construction and --extract
forest recovery. No oracle imports it. The prepared checker uses selected forest
arcs; verify.py independently uses the published two-color characterization,
then checks the resulting actual spanning forest before extraction. Both execute
the candidate through fresh subprocesses. No independent-author claim is made
for these two programs; native review is a separate step.

| Check | Coverage and outcome | Evidence |
|---|---|---|
| Prepared current suite | 9 source cases, 21 forest recoveries; pass | [output](../rounds/001/prepared-check-current.json) |
| Exhaustive/seeded suite | all 1,024 five-element triple families plus 64 seeded seven-element instances; 1,080 YES, 8 NO; 2,160 recoveries; pass | [raw progress/output](../rounds/001/exhaustive-check.jsonl) |
| Separate verifier | 37 cases, 25 YES, 12 NO; 112 recoveries; 15 cases exhaust all forests, including NO cases; largest output 644 vertices; pass | [output](../rounds/001/verify.json) |
| Fault and boundary checks | wrong forward decision and extraction rejected; 3 malformed serializations map to legal NO; malformed cyclic witness rejected | [output](evidence/preparation/fault-check.json) |

Commands from the repository root:
`python3 campaigns/binary-two-root-proper-forest/work/check.py --candidate campaigns/binary-two-root-proper-forest/work/algorithm.py`;
`python3 campaigns/binary-two-root-proper-forest/rounds/001/exhaustive-check.py`;
`python3 campaigns/binary-two-root-proper-forest/work/verify.py --candidate campaigns/binary-two-root-proper-forest/work/algorithm.py`.

The exhaustive suite ran before adding explicit malformed-JSON handling and
removing Python's integer digit cap. Its [candidate snapshot](../rounds/001/algorithm-before-json-boundary.py)
is preserved. Those changes do not alter any valid source construction or valid
witness recovery. The current prepared suite, separate verifier and boundary
checks ran after that repair. No other candidate changes remain untested.

The separate verifier includes renamed Fano NO instances, all permutations of
a repeated triple, isolated elements and reversed forest-arc lists. It enumerates
all target forests for sources with at most two elements, up to a limit of 20
(which the observed counts exhaust). Larger cases sample up to four forests.
All numeric computations are exact; no timeout or unknown result is treated as NO.
Finite checks support, but do not prove, the general theorem in proof.md.
