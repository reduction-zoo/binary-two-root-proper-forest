from pathlib import Path
import sys,itertools,json,random
root=Path(__file__).parents[2];sys.path.insert(0,str(root/'work'))
from check import run,source_solutions,target_solutions,source_witness
algorithm=root/'work/algorithm.py';triples=list(itertools.combinations(range(5),3))
count=0;yes=0;no=0;recovery=0;max_vertices=0
cases=[{'elements':list(range(5)),'triples':[list(t) for i,t in enumerate(triples) if mask>>i&1]} for mask in range(1<<len(triples))]
rng=random.Random(20260916)
for _ in range(64):cases.append({'elements':list(range(7)),'triples':[list(t) for t in itertools.combinations(range(7),3) if rng.random()<0.4]})
for source in cases:
    truth=bool(source_solutions(source));target=run(algorithm,source);forests=target_solutions(target,2)
    assert bool(forests)==truth,source
    n=len(source['elements']);m=len(source['triples'])
    assert len(target['vertices'])==20*n+22*m-2
    assert len(target['arcs'])==23*n+26*m-4
    for forest in forests:
        bits=run(algorithm,{'source':source,'target_solution':forest},True)
        assert source_witness(source,bits),(source,forest,bits);recovery+=1
    count+=1;yes+=truth;no+=not truth;max_vertices=max(max_vertices,len(target['vertices']))
    if count%128==0:print(json.dumps({'progress':count,'recoveries':recovery}),flush=True)
print(json.dumps({'result':'pass','source_instances':count,'yes':yes,'no':no,'forest_recoveries':recovery,'max_vertices':max_vertices,'seed':20260916}),flush=True)
