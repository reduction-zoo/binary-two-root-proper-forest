# Independent review

**Decision: advance.** Date: 2026-09-16. The complete construction and recovery rule supports the fixed question. No blocking correctness gap or prior resolution was identified. This is an agent review permitting manuscript preparation and expert review, not a publication or universal novelty certificate.

Reviewed: fixed `question.md`; `work/algorithm.py`, `proof.md`, `contract.md`, `preparation.md`, and `verification.md`. The candidate was unchanged during this review. I did not import either the candidate or either original checker. I wrote only in this review directory and did not spawn agents.

## Correctness

The coloring/forest equivalence is valid with exactly the stated witness semantics. Both original roots must be roots in any spanning subforest. Exactly two tree components therefore give one original root per component. The condition on omitted arcs forces every same-component network arc to be selected. Conversely, selecting same-colored arcs gives indegree one at each nonroot; acyclicity forces every parent chain to end at a root, and the child condition preserves the leaf set. Distinct root colors then give exactly two components. Thus the proof is about every valid forest, including noncanonical choices of comparison-reticulation parent.

At `algorithm.py:20–26`, each fanout use has a private leaf, preventing the receiving gadget from imposing an unintended child requirement on the supply vertex. Its continuations and ports have indegree one and copy the supply color. Every fanout list is nonempty: root supplies have 2 max(1,n) entries and every rail supplies a comparison reticulation. A k-use fanout including its initial vertex contains 3k−1 vertices. No port supplies two uses.

The variable construction at lines 29–34 gives independently selectable rail colors from the distinct root colors; the comparison reticulation forces the rails to differ. The clause at lines 35–40 is sound: A=¬a; B's sole child forces D=B, while D's two-parent condition forces B=b. Similarly C=E=c. The only remaining local condition is that A matches B or C, equivalent to NAE(a,b,c). Conversely every satisfying assignment extends, with either comparison color. Reticulation stacks are essential here and allowed by the fixed target.

Composition does not introduce cycles: root fanouts precede variable reticulations, then rail fanouts, then clause vertices A, B/C, D/E. Comparison reticulations and leaves are terminal relative to these dependencies. The allocation order need not itself be a topological order. Every vertex has an allowed degree; all ports and clause vertices are fresh; roots are joined through each variable reticulation, establishing weak connectivity even for NO instances and the dummy-variable empty instance. There are many private leaves.

The backward map at lines 47–57 reconstructs the deterministic metadata and traverses the supplied forest from roots 0 and 1. For a valid witness each vertex is reached once and receives its component label. Reading the positive rail reticulations consequently yields a valid source split by the necessity argument. Reversed forest-arc order has no effect. Full rejection of all invalid witnesses is not a premise of this recovery theorem.

The constant malformed-source output at line 15 is a legal binary two-root network. Root 0 forces the colors of both its tree children; their shared reticulation cannot have exactly one same-colored parent. Hence it is NO. JSON syntax errors are handled in forward mode. No counterexample to the source/target equivalence was found.

### Exact resources

I independently recomputed the counts. Root fanouts contribute 12n'−2 vertices, the variable and comparison vertices 4n', rail fanouts 4n'+15m, and clauses 7m, where n'=max(1,n). Thus N=20n'+22m−2. There are 3n'+4m reticulations, so E=(N−2)+(3n'+4m)=23n'+26m−4. The stated O((n+m+1) log(n+m+2)) output-bit bound follows. Both directions use O(n+m+1) graph operations on valid instances/witnesses, and the proof's conservative polynomial bit-time bound is sufficient. Parsing and rejecting an arbitrary malformed serialization must additionally be charged to its actual input length; n and m alone do not measure such an input. This is consistent with the proof's complete-input-length claim.

### Independent executable evidence

Command from the repository root:

```sh
python3 campaigns/binary-two-root-proper-forest/reviews/initial/independent_check.py
```

[`check-output.json`](check-output.json) records a pass. The check independently validates simplicity, weak connectivity, DAG order, all degrees, roots, leaves, and exact counts. It enumerates choices of incoming forest arcs and validates actual component/leaf/omitted-arc conditions, rather than importing the candidate's coloring argument. It exhausts all forests for n=0,1,2 with no clauses, and n=3 with one triple: respectively 4,4,16,48 valid forests. All 72 recovered witnesses are valid, and every possible source split is recovered. A separately written Z3 model checks Fano NO, one-line-deleted Fano YES (one additional recovered witness), and duplicated Fano with an isolated element NO. The constant NO target is checked by complete incoming-edge enumeration. These checks are finite evidence; the general argument above supplies the all-input justification.

## Novelty

Search date: 2026-09-16. I checked the theorem actually claimed, not simply the title or abstract of the baseline. Primary sources:

1. Huber, van Iersel, Moulton and Scholz, [*Is this network proper forest-based?*](https://doi.org/10.1016/j.ipl.2024.106500), IPL 187 (2025), 106500. The [journal PDF](https://pure.tudelft.nl/ws/portalfiles/portal/203216660/1-s2.0-S0020019024000309-main.pdf) is retained as `proper-forest.pdf`, with searchable `proper-forest.txt`. Lemma 3.1 is the known coloring characterization. Theorem 4.1 uses quasi-binary tree-child networks and the same size-three Set Splitting source. Theorem 6.1 treats binary tree-child networks with at least three roots; its binarization is explicitly not valid for arbitrary networks. Theorem 6.2 handles binary tree-child two-root networks. Section 8, journal page 6, explicitly leaves general binary two-root recognition open. Neither hardness theorem directly gives the candidate result. The candidate uses binary stacks to realize the clause condition instead of the baseline's indegree-three mechanism.

2. Huber, Moulton and Scholz, [*Forest-Based Networks*](https://link.springer.com/article/10.1007/s11538-022-01081-9), Bulletin of Mathematical Biology (2022), Section 7, Theorems 7–8. Theorem 8 characterizes the semi-binary two-root case by existence of a bipartite omni-extension. This is not merely a bipartiteness test on a fixed graph: choices of extension edges must satisfy the omnian requirements. The candidate's clause realizes precisely such a nontrivial choice. The characterization neither proves this restricted realization NP-hard nor provides a polynomial recognition algorithm for it. It therefore does not make the present construction an immediate already-proved consequence.

3. Lafond and Moulton, [*Path partitions of phylogenetic networks*](https://doi.org/10.1016/j.tcs.2024.114907), TCS 1024 (2025), 114907. Theorem 1 relates ordinary forest-basedness to leaf induced path partitions. Theorem 3 and Corollary 3 give hardness, including binary one-root networks with three leaves; Section 5 gives the two-path tractable boundary. Converting a branching forest to paths increases its component count. Thus none of these statements preserves the fixed requirement of exactly two components rooted at the two network roots. The known hardness cannot be transferred by simply relabeling the problem, and two induced paths are not two branching trees.

4. M.A. van Gruijthuijsen, [*Forest-Based Binary Phylogenetic Networks*](https://repository.tudelft.nl/file/File_12ae3435-6a43-4e2d-9675-dff3cd9ac922), TU Delft bachelor's thesis (2023), Sections 1.3 and 4. This primary thesis provides an ILP recognition/minimization formulation, including proper forest-basedness. It does not establish the claimed restricted NP-hardness.

Queries included `"proper forest-based" "binary" "2" NP`, `"proper forest-based" "binary" "2026"`, `"proper forest-based" "two roots" complexity`, `"proper forest-based" "reticulation" "stack"`, `"bipartite omni-extension" complexity`, and broader exact-phrase NP-completeness searches. Searches located the above baselines and related arboreal and semi-directed work, but no resolution of the fixed target. Coverage does not include unpublished or unindexed work, exhaustive citation-database traversal, or every equivalent terminology in graph constraint literature. Absence of a search hit is not proof of novelty. Within the inspected primary literature, the concrete restricted reduction is distinct and supported as a contribution suitable for expert assessment.

## Significance and scope

The result supplies a linear-size deterministic reduction and every-witness recovery for the exact general binary two-root recognition boundary explicitly raised by the closest primary paper. Target membership in NP follows by checking a spanning forest certificate and its omitted arcs in polynomial time, so the reduction establishes NP-completeness for the fixed target. This is a meaningful, moderate-scope classification result, rather than merely an encoding or an optimization of a known implementation. The fixed question's significance criterion is met. No claim about acceptance, a complete classification of other network subclasses, or novelty beyond the stated literature coverage is warranted.
