# Set Splitting to binary two-root proper forest recognition

## Statement and conventions

Let H=(X,C) be an explicitly represented 3-uniform hypergraph, allowing isolated
vertices and repeated triples. We construct a weakly connected binary DAG N with
two roots such that H has a nonmonochromatic bit assignment if and only if N is
proper forest-based. Every valid spanning forest of N yields such an assignment
in polynomial time. Empty instances are included by adding one dummy variable
only inside the construction and discarding its value during recovery.

A binary network has roots of degree (0,2), tree vertices (1,2), reticulations
(2,1), and leaves (1,0). A proper base forest is spanning, has exactly two rooted
tree components and the network's leaves, and has every omitted network arc
cross between components. Unary vertices are permitted in this subdivision forest.

We use the coloring characterization in Huber et al., IPL 187 (2025), 106500,
Lemma 3.1. For completeness, a coloring with two colors represents such a forest
precisely when the roots have distinct colors and:
(C1) each nonroot has exactly one same-color parent;
(C2) each nonleaf has at least one same-color child.
Selecting every monochromatic arc yields the forest. Its parent chains end at
the roots because the network is acyclic. Conversely, labeling components of a
valid forest gives (C1), (C2); every same-component network arc must be selected,
as an omitted one would violate the crossing condition. This argument covers
every valid target forest, not only a forest built in the forward proof.

## Color-copy trees and ports

A rail starts at a reticulation followed by a tree vertex. Any descendant reached
only through indegree-one tree vertices has the rail's color by (C1). To supply
k>=1 uses, build a binary caterpillar from that tree vertex. It has k ports;
each port has one private leaf and one arc to its designated receiving vertex.
Intermediate branches have two tree children. The private leaf always inherits
the port's color, so every supplying vertex satisfies (C2) independently of the
receiving gadget's color. Including its starting vertex and private leaves, a
k-port fanout has 3k-1 vertices. All designated receiving vertices are distinct
for a given port; repeated hyperedges use distinct clause gadgets.

## Variable gadget

For each element i create positive and negative reticulations P_i,Q_i, both
with one parent port from each root's fanout. Their parents have opposite colors,
so (C1) permits either color at each reticulation. Each reticulation has its own
color-copy fanout as its only child, satisfying (C2).

A comparison reticulation U_i has one parent port from each of the two rails,
and has one leaf child. With two available colors, (C1) is possible at U_i
exactly when P_i and Q_i differ. When they differ either color is allowed for
U_i, and its leaf satisfies (C2). Thus P_i is a free bit and Q_i its complement.
Each rail has at least this comparison use, so no zero-port fanout is needed.
Each root supplies all 2n' variable reticulations, where n'=max(1,|X|); hence
its fanout has at least two ports and its outdegree is two.

## Clause gadget

For a listed triple (a,b,c), introduce a tree vertex A, four reticulations B,C,D,E,
and leaf children of D,E. Their arcs are A→B,A→C,B→D,C→E. A receives its single
parent from the negative rail of a. B and C each have a separate second parent
from the positive rail of a. D receives its second parent from the negative
rail of b; E receives its second parent from the negative rail of c.

Write the source rail bits as a,b,c. Then A has color not-a. Its children B,C
have parents of opposite colors and initially may have either color. Because B
has only child D, (C2) forces D=B. The two parents of D must have opposite colors
by (C1), so B=b. Similarly C=E=c. All conditions now hold except possibly (C2)
at A. That condition says (not-a=b) or (not-a=c), which is exactly that a,b,c
are not all equal. This establishes both necessity and sufficiency of the local
relation. The reticulation-to-reticulation arcs B→D and C→E intentionally make
the output non-tree-child when there is a clause.

## Composition and network restrictions

Allocate all variable gadgets, clause gadgets and private leaves. Supply their
inputs using the root and rail fanouts just described. A topological ordering
places root fanouts first, then variable reticulations, their fanouts, comparison
reticulations and clause vertices in the order A, then B,C, then D,E; leaves come
after their parents. There is no backward gadget arc, so the output is acyclic.
All supplied ports are distinct, and each requested edge uses a fresh port,
so the graph is simple. Every listed vertex has one of the required degree types.
There are exactly two roots and at least two private leaves. Each variable
reticulation joins the two root descendant systems in the underlying undirected
graph; all remaining vertices descend from these systems. Thus the graph is
weakly connected, regardless of whether the source is YES or NO.

Given a source split, color root 0 by zero and root 1 by one. Color P_i by the
source bit, Q_i oppositely, and propagate through fanouts. Give each U_i any color.
For each clause use the forced colors above; the split guarantees (C2) at A.
Color all private and terminal leaves by their parents. Conditions (C1),(C2)
hold everywhere, hence monochromatic arcs form a valid proper base forest.

Conversely, take any proper base forest. Label its components by their roots,
with root 0 assigned zero. Its coloring satisfies (C1),(C2). The variable gadget
forces opposite rails, and the clause argument forces every source triple to
be nonmonochromatic. Read P_i's component for each actual element, ignoring any
dummy variable. This proves soundness and the every-witness recovery implication.
Global color reversal changes no NAE constraint; the root labels only make the
extractor deterministic.

## Determinism, totality and size

All allocation and traversal orders follow the explicitly listed source order.
For n'=max(1,n) and m triples, the root fanouts use 12n'-2 vertices. Variable
reticulations and comparison reticulation/leaf pairs use 4n' vertices. The two
rail fanouts for each variable have total uses 2n'+5m, hence 4n'+15m vertices.
Clauses contribute 7m vertices. Therefore

N = 20n' + 22m - 2,     E = 23n' + 26m - 4.

The arc count follows also from indegrees: there are 3n'+4m reticulations and
every nonroot otherwise has indegree one. Output length is O((n+m+1)
log(n+m+2)) bits. Graph construction and forest traversal use O(n+m+1) graph
operations; a conservative bound including implementation dictionary operations
and bit handling is O((n+m+1)^2 log(n+m+2)) time. Recovery reconstructs the same
metadata, traverses the supplied forest from its two roots, and outputs n bits.
On valid witnesses its output and work are polynomial in the complete encoded
input length. Traversal rejects repeated reachable vertices and nonspanning
forests, so malformed cyclic witnesses cannot cause unbounded traversal.

Malformed source values map to the fixed ten-vertex binary network listed in
algorithm.py. Its two tree children of root 0 share that root's color, but both
parent a reticulation, violating (C1). It is therefore a legal target NO instance.
Malformed JSON syntax also maps to this fixed NO network in forward mode.
Noncanonical decimal integers are parsed without an implementation digit cap;
illegal source labels are then rejected by the source predicate.

## Novelty and significance boundary

The known source hardness, coloring characterization and color-copy observation
are not claimed as new. The intended contribution is the binary clause realized
through reticulation stacks, settling general binary two-root recognition. The
published quasi-binary two-root construction uses indegree-three reticulations;
the polynomial binary result assumes tree-child. Ordinary forest-based recognition
permits a different number of components. The literature record in question.md
checks these distinctions. The independent review in ../reviews/initial/review.md advances correctness,
novelty within its inspected literature, and significance. Human expert
assessment remains outstanding.
