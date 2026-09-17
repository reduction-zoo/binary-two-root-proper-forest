"""Exact clause and fanout diagrams; boundary supply arcs are explicit stubs."""
from pathlib import Path
from math import hypot
from html import escape
import json
out=Path(__file__).parent

def draw(name,width,height,positions,edges,kinds,labels,notes,stubs=()):
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0,0 L8,4 L0,8 Z" fill="#222"/></marker></defs>',
           '<rect width="100%" height="100%" fill="white"/>']
    for u,v in edges:
        x,y=positions[u];a,b=positions[v];length=hypot(a-x,b-y);dx=(a-x)/length;dy=(b-y)/length
        r1=6 if kinds[u]=='leaf' else 15;r2=6 if kinds[v]=='leaf' else 18
        bold=kinds[u]=='retic' and kinds[v]=='retic'
        parts.append(f'<path d="M{x+dx*r1},{y+dy*r1} L{a-dx*r2},{b-dy*r2}" fill="none" stroke="#222" stroke-width="{3.4 if bold else 2}" marker-end="url(#arrow)"/>')
    for v in stubs:
        x,y=positions[v];parts.append(f'<path d="M{x},{y-43} L{x},{y-18}" stroke="#222" stroke-width="2" stroke-dasharray="5,4" marker-end="url(#arrow)"/>')
    for v,(x,y) in positions.items():
        if kinds[v]=='leaf':parts.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#222"/>')
        elif kinds[v]=='retic':parts.append(f'<path d="M{x},{y-16} L{x+16},{y} L{x},{y+16} L{x-16},{y} Z" fill="#d8e5f1" stroke="#222" stroke-width="2"/>')
        else:parts.append(f'<circle cx="{x}" cy="{y}" r="14" fill="white" stroke="#222" stroke-width="2"/>')
        if v in labels:parts.append(f'<text x="{x}" y="{y+6}" text-anchor="middle" font-family="Libertinus Serif,serif" font-size="19" font-style="italic">{escape(labels[v])}</text>')
    for x,y,text,italic in notes:
        parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" font-family="Libertinus Serif,serif" font-size="19" font-style="{"italic" if italic else "normal"}">{escape(text)}</text>')
    parts.append('</svg>');(out/name).write_text('\n'.join(parts)+'\n')

pos={'A':(350,120),'B':(220,240),'C':(480,240),'D':(220,365),'E':(480,365),
     'pa':(350,55),'p1':(100,180),'p2':(600,180),'pb':(100,320),'pc':(600,320),
     'la':(415,55),'l1':(45,205),'l2':(655,205),'lb':(45,345),'lc':(655,345),'ld':(220,445),'le':(480,445)}
edges=[('pa','A'),('pa','la'),('p1','B'),('p1','l1'),('p2','C'),('p2','l2'),('pb','D'),('pb','lb'),('pc','E'),('pc','lc'),('A','B'),('A','C'),('B','D'),('C','E'),('D','ld'),('E','le')]
kinds={v:('leaf' if v.startswith('l') else 'retic' if v in 'BCDE' else 'tree') for v in pos}
assert all((sum(v==b for a,b in edges),sum(v==a for a,b in edges))==((1,2) if v=='A' else (2,1)) for v in 'ABCDE')
assert len(edges)==16 and len(pos)==17
notes=[(300,55,'¬a',True),(55,174,'a',True),(645,174,'a',True),(58,308,'¬b',True),(642,308,'¬c',True),
       (393,126,'¬a',True),(175,244,'b',True),(525,244,'c',True),(175,370,'b',True),(525,370,'c',True)]
draw('clause.svg',700,470,pos,edges,kinds,{v:v for v in 'ABCDE'},notes,['pa','p1','p2','pb','pc'])
pos={'r':(75,50),'u':(190,125),'v':(330,200),'p':(75,200),'q':(190,275),'lr':(30,275),'lp':(290,280),'lv':(380,280),'t1':(75,350),'t2':(190,350),'t3':(330,350)}
# Three ports are p, q and v. Each has a private leaf and a designated receiver.
edges=[('r','p'),('r','u'),('u','q'),('u','v'),('p','lr'),('p','t1'),('q','lp'),('q','t2'),('v','lv'),('v','t3')]
kinds={v:('leaf' if v in ('lr','lp','lv') else 'retic' if v.startswith('t') else 'tree') for v in pos}
assert all(sum(a==v for a,b in edges)==2 for v in ('r','u','v','p','q'))
notes=[(40,50,'s',True),(130,125,'s',True),(360,200,'s',True),(43,200,'s',True),(155,275,'s',True),(190,400,'Other receiver parents omitted',False)]
draw('fanout.svg',460,425,pos,edges,kinds,{},notes,['r'])
(out/'adjacency-check.json').write_text(json.dumps({'clause_vertices':17,'clause_arcs':16,'clause_internal_degrees':'pass','three_port_fanout_degrees':'pass','boundary_stubs':'incoming fanout/rail arcs; receivers may have other omitted parents'},indent=2)+'\n')

positions={0:(120,40),1:(500,40),2:(230,245),3:(390,245),4:(230,330),5:(390,330),6:(310,430),7:(310,500),8:(75,125),9:(165,125),10:(30,190),11:(210,190),12:(455,125),13:(545,125),14:(410,190),15:(590,190),16:(150,395),17:(470,395)}
edges=[(2,4),(3,5),(6,7),(0,8),(0,9),(8,2),(8,10),(9,3),(9,11),(1,12),(1,13),(12,2),(12,14),(13,3),(13,15),(4,6),(4,16),(5,6),(5,17)]
kinds={v:('leaf' if v in (7,10,11,14,15,16,17) else 'retic' if v in (2,3,6) else 'tree') for v in positions}
import subprocess,sys
actual=json.loads(subprocess.run([sys.executable,str(out.parent/'algorithm.py')],input='{"elements":[0],"triples":[]}',text=True,capture_output=True,check=True).stdout)
assert set(edges)==set(map(tuple,actual['arcs'])) and set(positions)==set(actual['vertices'])
draw('variable.svg',620,530,positions,edges,kinds,{0:'0',1:'1',2:'P',3:'Q',6:'U'},[(186,245,'b',True),(435,245,'¬b',True),(385,435,'either',False)])
(out/'variable-adjacency-check.json').write_text(json.dumps({'vertices':len(positions),'arcs':len(edges),'matches_actual_one_variable_output':True})+'\n')
