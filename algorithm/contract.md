# Input and witness contract

Source: {"elements": [0,...,n-1], "triples": [[a,b,c],...]}. Elements are explicitly
listed; each triple has three distinct listed integer vertices. Empty universes,
empty triple families, repeated triples and isolated elements are allowed.
Malformed source encodings are NO. Source witnesses are lists of n bits making
every triple nonmonochromatic. No nonemptiness condition is placed on the two
parts when there are no triples.

Target: {"vertices": [0,...,N-1], "arcs": [[u,v],...]}, a simple weakly connected
DAG with exactly two (0,2) roots, at least two leaves, and remaining degrees in
{(1,2),(2,1),(1,0)}. Target witnesses list the forest arcs. They must span every
vertex, have exactly the two original roots and original leaf set, and consist
of two directed trees. Every omitted network arc must cross components.

algorithm.py reads one source JSON value and emits a legal target. --extract
reads {"source": source, "target_solution": forest arc list} and emits source
bits. Both invocations are separate processes. Any valid forest is accepted;
no canonical color labeling or optimality is part of the witness premise.
