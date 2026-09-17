"""Separate color-based oracle and direct forest/recovery verification."""
import argparse,itertools,json,random,subprocess,sys
import z3


def invoke(path,data,extract=False):
    result=subprocess.run([sys.executable,path]+(['--extract'] if extract else []),input=json.dumps(data),text=True,capture_output=True,check=True)
    return json.loads(result.stdout)


def decision(source):
    n=len(source['elements'])
    for mask in range(1<<n):
        if all(0<sum(mask>>v&1 for v in t)<3 for t in source['triples']):return True
    return False


def solve(target,limit):
    vs=target['vertices'];arcs=target['arcs'];n=len(vs)
    assert vs==list(range(n)) and len({tuple(e) for e in arcs})==len(arcs)
    incoming=[[] for _ in vs];outgoing=[[] for _ in vs]
    for u,v in arcs:
        assert type(u) is int and type(v) is int and 0<=u<n and 0<=v<n and u!=v
        incoming[v].append(u);outgoing[u].append(v)
    roots=[v for v in vs if not incoming[v]]
    assert len(roots)==2 and sum(not outgoing[v] for v in vs)>=2
    assert all((len(incoming[v]),len(outgoing[v])) in ((0,2),(1,2),(2,1),(1,0)) for v in vs)
    degree=[len(p) for p in incoming];queue=roots[:]
    for u in queue:
        for v in outgoing[u]:
            degree[v]-=1
            if degree[v]==0:queue.append(v)
    assert len(queue)==n
    seen={roots[0]};stack=list(seen)
    for u in stack:
        for v in incoming[u]+outgoing[u]:
            if v not in seen:seen.add(v);stack.append(v)
    assert len(seen)==n
    colors=[z3.Bool(f'v{i}') for i in vs];s=z3.Solver();s.add(colors[roots[0]]!=colors[roots[1]])
    for v in vs:
        if incoming[v]:s.add(z3.Sum([z3.If(colors[u]==colors[v],1,0) for u in incoming[v]])==1)
        if outgoing[v]:s.add(z3.Or([colors[u]==colors[v] for u in outgoing[v]]))
    forests=[];exhausted=False
    for _ in range(limit):
        status=s.check()
        if status==z3.unsat:exhausted=True;break
        assert status==z3.sat,status
        model=s.model();bits=[z3.is_true(model.eval(c,model_completion=True)) for c in colors]
        edges=[[u,v] for u,v in arcs if bits[u]==bits[v]]
        children=[[] for _ in vs];indegree=[0]*n
        for u,v in edges:children[u].append(v);indegree[v]+=1
        assert all(indegree[v]==(0 if v in roots else 1) for v in vs)
        assert all(bool(children[v])==bool(outgoing[v]) for v in vs)
        owner={roots[0]:0,roots[1]:1};order=roots[:]
        for u in order:
            for v in children[u]:assert v not in owner;owner[v]=owner[u];order.append(v)
        assert len(owner)==n
        assert all([u,v] in edges or owner[u]!=owner[v] for u,v in arcs)
        forests.append(edges)
        # Block both global color orientations of this same forest.
        s.add(z3.Or([colors[v]!=bits[v] for v in vs]))
        s.add(z3.Or([colors[v]==bits[v] for v in vs]))
    return forests,exhausted


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--candidate',required=True);args=parser.parse_args()
    fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]]
    cases=[{'elements':list(range(n)),'triples':[]} for n in (0,1,2,8)]
    cases.append({'elements':list(range(3)),'triples':list(map(list,itertools.permutations(range(3))))})
    cases.append({'elements':list(range(5)),'triples':list(map(list,itertools.combinations(range(5),3)))})
    for shift in range(7):cases.append({'elements':list(range(7)),'triples':[[((v+shift)%7) for v in reversed(t)] for t in fano]})
    rng=random.Random(73019)
    for _ in range(24):cases.append({'elements':list(range(7)),'triples':[list(t) for t in itertools.combinations(range(7),3) if rng.random()<0.45]})
    recoveries=0;yes=0;no=0;exhausted=0;max_n=0
    for source in cases:
        actual=invoke(args.candidate,source);truth=decision(source)
        forests,all_done=solve(actual,20 if len(source['elements'])<=2 else 4)
        assert bool(forests)==truth,source
        yes+=truth;no+=not truth;exhausted+=all_done;max_n=max(max_n,len(actual['vertices']))
        for forest in forests:
            bits=invoke(args.candidate,{'source':source,'target_solution':list(reversed(forest))},True)
            assert isinstance(bits,list) and len(bits)==len(source['elements']) and all(type(b) is int and b in (0,1) for b in bits)
            assert all(0<sum(bits[v] for v in t)<3 for t in source['triples'])
            recoveries+=1
    print(json.dumps({'result':'pass','source_cases':len(cases),'yes':yes,'no':no,'forest_recoveries':recoveries,'all_forests_exhausted_cases':exhausted,'maximum_target_vertices':max_n,'seed':73019,'solver':z3.get_version_string()}))


if __name__=='__main__':main()
