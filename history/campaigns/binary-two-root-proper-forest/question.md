---
status: active
openness: supported-within-search
difficulty: moderate
importance: moderate
tags: [phylogenetic-network, proper-forest-based, two-roots, binary, set-splitting]
last-literature-check: 2026-09-16
---

# Binary two-root proper forest recognition

## Fixed question

Construct a deterministic polynomial-time Karp reduction from 3-Uniform Set
Splitting to Proper Forest-Based Recognition on binary two-root networks.
Source: an explicitly listed finite universe and triples of distinct elements;
a witness assigns each element a bit and makes every triple nonmonochromatic.
Allow an empty triple family and isolated elements. Malformed strings are NO.

Target: a weakly connected simple DAG with exactly two roots of degree (0,2),
all other vertices of type (1,2), (2,1) or (1,0), and at least two leaves.
A witness is a spanning subforest consisting of exactly two directed rooted
trees, with the network's leaf set, such that every excluded arc connects the
two different components. Unary subdivision vertices may occur in the forest,
not in the network. Every output, including source NO instances, must obey the
network restrictions. A supplied valid forest must recover a source split in
polynomial time. The intended size and bit bounds are O(n+m) vertices/arcs and
O((n+m) log(n+m+2)) bits. Prove actual construction and recovery bounds.

Success requires this complete rule, general proof, independent tests/review
and novelty assessment. A generic SAT encoding or a nonbinary construction does
not qualify. A failed gadget is a partial result, not a resolution.

## Primary evidence

Huber, van Iersel, Moulton and Scholz, *Is this network proper forest-based?*,
[Information Processing Letters 187 (2025), 106500](https://doi.org/10.1016/j.ipl.2024.106500),
[full journal PDF](https://pure.tudelft.nl/ws/portalfiles/portal/203216660/1-s2.0-S0020019024000309-main.pdf),
Lemma 3.1: proper forest-basedness is equivalent to an m-coloring in which each
nonroot has exactly one same-color parent and each internal vertex has at least
one same-color child. Theorem 4.1 gives hardness for quasi-binary tree-child
2-networks, using indegree-three reticulations. Theorem 6.2 gives a polynomial
algorithm for binary tree-child 2-networks. Section 8 explicitly asks about
general binary 2-networks and tree-sibling extensions.

The source is exactly the size-three Set Splitting problem used in Theorem 4.1;
we do not infer hardness from unrestricted hyperedge sizes.

*Path partitions of phylogenetic networks*, [TCS 1024 (2025), 114907](https://doi.org/10.1016/j.tcs.2024.114907),
[full PDF](https://ueaeprints.uea.ac.uk/97012/7/1_s2.0_S0304397524005243_main.pdf),
proves hardness of ordinary forest-based recognition, even with one root and
three leaves. Its number of forest components is not fixed to the number of
network roots. Its polynomial two-induced-path result is also not a result
about two branching tree components. These theorems do not immediately settle
the target. Both full PDFs were downloaded and inspected.

Queries on 2026-09-16: `"proper forest-based" "two" NP-complete binary`,
`"proper forest-based" "2-network" NP-complete`,
`"proper forest-based" "binary" "NP-complete" "two"`,
`"proper forest-based" "2-networks" complexity`, and
`"proper forest-based" "2026" -forest-based-value -random -classification`.
The arXiv record [2308.11176](https://arxiv.org/abs/2308.11176) and subsequent TCS
paper were checked. No resolution of the exact target was identified. Unindexed
and unpublished work remains outside coverage.

## Proposed mechanism and bounded evidence

For each source bit make two freely chosen opposite-colored reticulations,
supplied by the two root colors. Binary tree fanout copies those colors. A
reticulation with opposite-colored parents permits either output color; a
reticulation stack can force an output to equal a remotely supplied bit.

For a clause (a,b,c), a tree vertex A has color not-a and two reticulation
children B,C, both also parented by separate a-colored ports. B's only child D
has a second parent colored not-b; C's only child E has second parent not-c.
The local parent and child conditions force B=D=b and C=E=c. A has a same-color
child precisely when not-a equals b or c, equivalent to NAE(a,b,c). D and E
receive leaf children. Supply ports use private leaves to satisfy their own
child condition independently. Reticulation stacks intentionally leave the
polynomial tree-child subclass.

The [interface probe](../evidence/binary-two-root-forest-clause-probe.py) checks
all eight boundary assignments and all sixteen internal assignments for each.
[Output](../evidence/binary-two-root-forest-clause-probe.json): exactly the six
NAE assignments extend, each uniquely. Remaining obligations are legal binary
fanout composition, root/component consistency, every-forest recovery and a full
independent source/target check. This bounded result is not the global theorem.
Existing experience searches for forest-based networks and reconciliation found
no applicable construction; previous network-contraction results concern a
different witness relation and are not reused.

## Assessment and gates

Difficulty: moderate, provisionally. The logical clause is verified and the
remaining composition uses bounded-degree color copying; forest witness semantics
and unintended constraints still need independent checks. Importance: moderate.
The target settles the general binary two-root boundary left open in the primary
paper, contrasting with its tree-child algorithm. No broader classification is
claimed.

| Gate | Decision | Evidence |
|---|---|---|
| Exact endpoints | pass | Explicit Set Splitting and binary two-root forest witnesses |
| Known results | pass | Indegree-three hardness and tree-child algorithm differ |
| Supported openness | pass | Explicit Section 8 question; follow-up theorem checks |
| Significance | pass | A named recognition boundary, not an implementation port |
| Proof route | pass | Binary clause and opposite-color fanout/stack mechanism |
| Bounded investigation | pass | Complete local interface relation on 128 assignments |

Campaign: campaigns/binary-two-root-proper-forest. Allocation: 40 rounds under
the standing authorization. Stop early on a reviewed result or no supported
next mechanism. Keep the statement fixed; binary tree-sibling is not silently
added as a target restriction.
