"""Independent exact source and spanning-forest oracles."""
import argparse,itertools,json,subprocess,sys
from pathlib import Path
import networkx as nx
import z3


def legal_source(x):
    if not isinstance(x,dict) or not isinstance(x.get('elements'),list) or not isinstance(x.get('triples'),list):return False
    vertices=x['elements'];n=len(vertices)
    return all(type(v) is int for v in vertices) and vertices==list(range(n)) and all(isinstance(t,list) and len(t)==3 and all(type(v) is int and 0<=v<n for v in t) and len(set(t))==3 for t in x['triples'])


def source_witness(x,bits):
    return legal_source(x) and isinstance(bits,list) and len(bits)==len(x['elements']) and all(type(b) is int and b in (0,1) for b in bits) and all(len({bits[v] for v in t})==2 for t in x['triples'])


def source_solutions(x):
    if not legal_source(x):return []
    return [list(b) for b in itertools.product((0,1),repeat=len(x['elements'])) if source_witness(x,list(b))]


def target_graph(x):
    assert isinstance(x,dict) and isinstance(x.get('vertices'),list) and isinstance(x.get('arcs'),list)
    vs=x['vertices'];assert all(type(v) is int for v in vs) and vs==list(range(len(vs)))
    assert len(vs)>=2
    for e in x['arcs']:assert isinstance(e,list) and len(e)==2 and all(type(v) is int and v in vs for v in e) and e[0]!=e[1]
    assert len({tuple(e) for e in x['arcs']})==len(x['arcs'])
    g=nx.DiGraph();g.add_nodes_from(vs);g.add_edges_from(x['arcs'])
    assert nx.is_directed_acyclic_graph(g) and nx.is_weakly_connected(g)
    roots=[v for v in g if g.in_degree(v)==0]
    assert len(roots)==2 and all(g.out_degree(v)==2 for v in roots)
    assert sum(g.out_degree(v)==0 for v in g)>=2
    assert all((g.in_degree(v),g.out_degree(v)) in ((0,2),(1,2),(2,1),(1,0)) for v in g)
    return g,roots


def forest_witness(x,edges):
    g,roots=target_graph(x)
    if not isinstance(edges,list) or any(not isinstance(e,list) or len(e)!=2 or tuple(e) not in g.edges for e in edges):return False
    if len({tuple(e) for e in edges})!=len(edges):return False
    f=nx.DiGraph();f.add_nodes_from(g);f.add_edges_from(edges)
    if any(f.in_degree(v)!=(0 if v in roots else 1) for v in f):return False
    if {v for v in f if f.out_degree(v)==0}!={v for v in g if g.out_degree(v)==0}:return False
    components=list(nx.weakly_connected_components(f))
    if len(components)!=2 or any(len(set(roots)&s)!=1 for s in components):return False
    owner={v:i for i,s in enumerate(components) for v in s}
    return all((u,v) in f.edges or owner[u]!=owner[v] for u,v in g.edges)


def target_solutions(x,limit=3):
    g,roots=target_graph(x);solver=z3.Solver()
    owner={v:z3.Bool(f'c{v}') for v in g};chosen={e:z3.Bool(f'e{e[0]}_{e[1]}') for e in g.edges}
    solver.add(z3.Not(owner[roots[0]]),owner[roots[1]])
    for (u,v),s in chosen.items():solver.add(s==(owner[u]==owner[v]))
    for v in g:
        if v not in roots:solver.add(z3.PbEq([(chosen[u,v],1) for u in g.predecessors(v)],1))
        if g.out_degree(v):solver.add(z3.Or([chosen[v,w] for w in g.successors(v)]))
    solutions=[]
    for _ in range(limit):
        result=solver.check()
        if result==z3.unsat:break
        assert result==z3.sat,result
        model=solver.model();edges=[list(e) for e,s in chosen.items() if z3.is_true(model.eval(s,model_completion=True))]
        assert forest_witness(x,edges)
        solutions.append(edges)
        solver.add(z3.Or([s!=model.eval(s,model_completion=True) for s in chosen.values()]))
    return solutions


def run(path,x,extract=False):
    proc=subprocess.run([sys.executable,str(path)]+(['--extract'] if extract else []),input=json.dumps(x),text=True,capture_output=True,check=True)
    return json.loads(proc.stdout)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--self-test',action='store_true');parser.add_argument('--candidate');args=parser.parse_args()
    cases=json.loads(Path(__file__).with_name('cases.json').read_text())
    if args.self_test:
        for c in cases:assert bool(source_solutions(c['source']))==c['yes']
        yes={'vertices':list(range(6)),'arcs':[[0,2],[0,3],[1,2],[1,4],[2,5]]}
        assert len(target_solutions(yes,10))==2
        assert not forest_witness(yes,yes['arcs'])
        valid_no={'vertices':list(range(10)),'arcs':[[0,2],[0,3],[2,6],[2,4],[3,7],[3,4],[4,5],[1,5],[1,8],[5,9]]}
        assert target_solutions(valid_no)==[]
        no={'vertices':list(range(8)),'arcs':[[0,2],[0,3],[1,4],[1,5],[2,6],[3,6],[4,7],[5,7],[6,4]]}
        # This deliberately malformed graph is rejected before a decision query.
        try:target_graph(no)
        except AssertionError:pass
        else:raise AssertionError('malformed graph accepted')
        assert not source_witness(cases[0]['source'],[2])
        print(json.dumps({'self_test':'pass','source_cases':len(cases),'small_forests':2,'solver':z3.get_version_string()}))
    if args.candidate:
        recovery=0;sizes=[]
        for case in cases:
            source=case['source'];target=run(args.candidate,source);solutions=target_solutions(target)
            assert bool(solutions)==case['yes'],source
            sizes.append([len(target['vertices']),len(target['arcs'])])
            for forest in solutions:
                recovered=run(args.candidate,{'source':source,'target_solution':forest},True)
                assert source_witness(source,recovered),(source,recovered)
                recovery+=1
        print(json.dumps({'candidate':'pass','source_cases':len(cases),'forest_recoveries':recovery,'target_sizes':sizes}))


if __name__=='__main__':main()
