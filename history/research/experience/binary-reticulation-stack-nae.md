# Binary reticulation stacks realize not-all-equal constraints

Tags: phylogenetic-network, proper-forest-based, binary, two-roots, reticulation-stack, NAE, protected-port.

## Claim and applicability

Under the two-color characterization of a proper base forest, every nonroot
has exactly one same-color parent and every nonleaf has a same-color child.
For a binary reticulation, the parent condition forces its two parents to have
opposite colors. If its only child is another reticulation, the child condition
forces those two reticulations to have the same color. Supplying the latter
reticulation's other parent with the complement of b therefore forces both
reticulations to have color b.

Apply two such stacks below a tree vertex of color not-a. Give their upper
reticulations second parents of color a and their lower reticulations second
parents of colors not-b and not-c. The tree's child condition is exactly
(not-a=b) or (not-a=c), the NAE relation. Binary color-copy trees can supply
these inputs, but each supplying port needs a private leaf to satisfy its own
child condition independently of the recipient. A port serves exactly one use.

These statements require two colors, proper forest witness semantics, and
reticulation stacks. They do not prove hardness for tree-child or tree-sibling
networks, nor for an arbitrary number of forest components. The published
coloring characterization is an ingredient, not a new result claimed here.

## Evidence and status

General construction lemma and composed Karp rule; independent agent review
advances, human expert assessment pending. See the originating
[round](../../campaigns/binary-two-root-proper-forest/rounds/001/round.md),
[proof](../../campaigns/binary-two-root-proper-forest/work/proof.md),
[review](../../campaigns/binary-two-root-proper-forest/reviews/initial/review.md),
and [paper](../../campaigns/binary-two-root-proper-forest/work/manuscript.pdf).
The review checked the source/target equivalence, every-forest recovery, degree
restrictions, composition and bit bounds. Finite tests support the implementation;
the lemma's universal claim rests on the proof, not the number of tests.

## Consequence for search

When a binary-network gadget seems unable to enforce a three-variable relation,
check whether the sole-child condition across a permitted reticulation stack
transmits a color constraint. Separate color distribution from recipient
constraints using private-leaf ports. Verify the target permits stacks before
using this mechanism; omitting that premise can cross a known tractability boundary.

## Use history

Derived in the linked campaign's first round; no subsequent campaign use yet.
No quantitative improvement in search efficiency has been established.
