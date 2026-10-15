"""Set Splitting to binary two-root proper forest recognition."""
import json
import sys


def legal_source(x):
    if not isinstance(x,dict) or not isinstance(x.get('elements'),list) or not isinstance(x.get('triples'),list):return False
    vertices=x['elements'];n=len(vertices)
    return all(type(v) is int for v in vertices) and vertices==list(range(n)) and all(isinstance(t,list) and len(t)==3 and all(type(v) is int and 0<=v<n for v in t) and len(set(t))==3 for t in x['triples'])


def construct(source):
    if not legal_source(source):
        return {'vertices':list(range(10)),'arcs':[[0,2],[0,3],[2,6],[2,4],[3,7],[3,4],[4,5],[1,5],[1,8],[5,9]]},[]
    vertices=[0,1];arcs=[]
    def vertex():
        v=len(vertices);vertices.append(v);return v
    def leaf(parent):arcs.append([parent,vertex()])
    def fanout(root,targets):
        current=root
        for target in targets[:-1]:
            port=vertex();continuation=vertex()
            arcs.extend([[current,port],[current,continuation],[port,target]])
            leaf(port);current=continuation
        arcs.append([current,targets[-1]]);leaf(current)
    count=max(1,len(source['elements']));positive=[];negative=[];positive_roots=[];negative_roots=[]
    positive_targets=[[] for _ in range(count)];negative_targets=[[] for _ in range(count)]
    for i in range(count):
        p=vertex();q=vertex();pr=vertex();qr=vertex()
        positive.append(p);negative.append(q);positive_roots.append(pr);negative_roots.append(qr)
        arcs.extend([[p,pr],[q,qr]])
        unequal=vertex();leaf(unequal)
        positive_targets[i].append(unequal);negative_targets[i].append(unequal)
    for a,b,c in source['triples']:
        x=vertex();y=vertex();z=vertex();d=vertex();e=vertex()
        arcs.extend([[x,y],[x,z],[y,d],[z,e]]);leaf(d);leaf(e)
        negative_targets[a].append(x)
        positive_targets[a].extend([y,z])
        negative_targets[b].append(d);negative_targets[c].append(e)
    for root in (0,1):fanout(root,positive+negative)
    for i in range(count):
        fanout(positive_roots[i],positive_targets[i]);fanout(negative_roots[i],negative_targets[i])
    return {'vertices':vertices,'arcs':arcs},positive


def extract(source,forest):
    if not legal_source(source):raise ValueError('Malformed source has no valid target witness')
    target,positive=construct(source);children=[[] for _ in target['vertices']]
    for u,v in forest:children[u].append(v)
    owner={0:0,1:1};queue=[0,1]
    for u in queue:
        for v in children[u]:
            if v in owner:raise ValueError("Forest contains a repeated reachable vertex")
            owner[v]=owner[u];queue.append(v)
    if len(owner)!=len(children):raise ValueError("Forest does not span both rooted components")
    return [owner[v] for v in positive[:len(source['elements'])]]


if __name__=='__main__':
    payload=json.load(sys.stdin)
    if sys.argv[1:]==['--extract']:result=extract(payload['source'],payload['target_solution'])
    elif not sys.argv[1:]:result=construct(payload)[0]
    else:raise ValueError('Only --extract is supported')
    json.dump(result,sys.stdout);sys.stdout.write('\n')
