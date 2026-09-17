"""Independent review: incoming-edge enumeration and explicit component checking."""
import itertools
import json
from pathlib import Path
import subprocess
import sys
import z3

CANDIDATE = Path(__file__).resolve().parents[2] / 'work/algorithm.py'

def call(payload, extract=False):
    p = subprocess.run([sys.executable, str(CANDIDATE)] + (['--extract'] if extract else []),
                       input=json.dumps(payload), text=True, capture_output=True, check=True)
    return json.loads(p.stdout)

def graph(g):
    n = len(g['vertices'])
    assert g['vertices'] == list(range(n))
    arcs = [tuple(e) for e in g['arcs']]
    assert len(set(arcs)) == len(arcs)
    parents, children = [[] for _ in range(n)], [[] for _ in range(n)]
    for u, v in arcs:
        assert 0 <= u < n and 0 <= v < n and u != v
        parents[v].append(u); children[u].append(v)
    roots = [v for v in range(n) if not parents[v]]
    assert roots == [0, 1]
    assert all((len(parents[v]), len(children[v])) in {(0, 2), (1, 2), (2, 1), (1, 0)} for v in range(n))
    assert sum(not c for c in children) >= 2
    pending = list(map(len, parents)); order = roots.copy()
    for u in order:
        for v in children[u]:
            pending[v] -= 1
            if pending[v] == 0: order.append(v)
    assert len(order) == n
    reached = {0}; queue = [0]
    for u in queue:
        for v in parents[u] + children[u]:
            if v not in reached: reached.add(v); queue.append(v)
    assert len(reached) == n
    return parents, children, order

def valid_forest(g, edges, order):
    n = len(order); edges = set(edges); arcs = set(map(tuple, g['arcs']))
    if not edges <= arcs: return False
    owner = {0: 0, 1: 1}; p = {}; children = set()
    for u, v in edges:
        if v in p: return False
        p[v] = u; children.add(u)
    for v in order:
        if v not in (0, 1):
            if v not in p: return False
            owner[v] = owner[p[v]]
    return children == {u for u, v in arcs} and all(owner[u] != owner[v] for u, v in arcs - edges)

def source_bits(source):
    return {b for b in itertools.product((0, 1), repeat=len(source['elements']))
            if all(len({b[v] for v in t}) == 2 for t in source['triples'])}

def check(source, exhaustive):
    g = call(source); parents, children, order = graph(g)
    n, m = len(source['elements']), len(source['triples'])
    assert len(parents) == 20 * max(1, n) + 22*m - 2
    assert len(g['arcs']) == 23 * max(1, n) + 26*m - 4
    expected = source_bits(source); found = set(); count = 0
    if exhaustive:
        vertices = [v for v in order if parents[v]]
        forests = (list(zip(selection, vertices)) for selection in itertools.product(*(parents[v] for v in vertices)))
    else:
        solver = z3.Solver(); colors = [z3.Bool(f'v{v}') for v in order]
        solver.add(z3.Not(colors[0]), colors[1])
        for v in order:
            if parents[v]: solver.add(z3.PbEq([(colors[v] == colors[u], 1) for u in parents[v]], 1))
            if children[v]: solver.add(z3.Or([colors[v] == colors[u] for u in children[v]]))
        answer = solver.check(); assert answer in (z3.sat, z3.unsat)
        if answer == z3.unsat: forests = []
        else:
            model = solver.model()
            forests = [[tuple(e) for e in g['arcs'] if z3.is_true(model.eval(colors[e[0]] == colors[e[1]]))]]
    for forest in forests:
        if not valid_forest(g, forest, order):
            assert exhaustive
            continue
        witness = call({'source': source, 'target_solution': list(reversed(forest))}, True)
        assert tuple(witness) in expected
        found.add(tuple(witness)); count += 1
    assert bool(found) == bool(expected)
    if exhaustive: assert found == expected
    return {'n': n, 'm': m, 'forests_checked': count, 'all_forests': exhaustive,
            'recovered_splits': len(found), 'source_splits': len(expected)}

if __name__ == '__main__':
    cases = [(n, [], True) for n in (0, 1, 2)] + [(3, [[0,1,2]], True)]
    fano = [[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]]
    cases += [(7, fano, False), (7, fano[:-1], False), (8, fano + fano, False)]
    results = [check({'elements': list(range(n)), 'triples': ts}, exhaustive) for n, ts, exhaustive in cases]
    malformed = call({'elements': [0], 'triples': [[0,0,0]]})
    parents, children, order = graph(malformed)
    vertices = [v for v in order if parents[v]]
    assert not any(valid_forest(malformed, zip(selection, vertices), order)
                   for selection in itertools.product(*(parents[v] for v in vertices)))
    print(json.dumps({'status': 'pass', 'cases': results, 'constant_no_checked_exhaustively': True}, indent=2))
