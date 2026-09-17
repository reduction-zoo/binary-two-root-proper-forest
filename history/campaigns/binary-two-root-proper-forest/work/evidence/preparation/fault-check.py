from pathlib import Path
import json,subprocess,sys
work=Path(__file__).parents[2];sys.path.insert(0,str(work))
from check import run,target_solutions
results=[]
for name in ('wrong-decision','wrong-recovery'):
    p=subprocess.run([sys.executable,str(work/'check.py'),'--candidate',str(Path(__file__).with_name(name+'.py'))],text=True,capture_output=True)
    assert p.returncode!=0 and 'AssertionError' in p.stderr
    Path(__file__).with_name(name+'.stderr').write_text(p.stderr)
    results.append({'fixture':name,'rejected':True,'exit_code':p.returncode})
for raw in ('{','null','{"elements":['+'9'*5001+'],"triples":[]}'):
    p=subprocess.run([sys.executable,str(work/'algorithm.py')],input=raw,text=True,capture_output=True,check=True)
    assert target_solutions(json.loads(p.stdout))==[]
results.append({'malformed_serializations_mapped_to_legal_no':3})
source={'elements':[0],'triples':[]}
p=subprocess.run([sys.executable,str(work/'algorithm.py'),'--extract'],input=json.dumps({'source':source,'target_solution':[[0,2],[2,2]]}),text=True,capture_output=True)
assert p.returncode!=0 and 'repeated reachable vertex' in p.stderr
results.append({'cyclic_recovery_input_rejected':True})
print(json.dumps(results,indent=2))
