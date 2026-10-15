from pathlib import Path
import json,subprocess,sys
payload=json.load(sys.stdin)
if '--extract' in sys.argv:print(json.dumps([0]*len(payload['source']['elements'])))
else:
    result=subprocess.run([sys.executable,str(Path(__file__).parents[2]/'algorithm.py')],input=json.dumps(payload),text=True,capture_output=True,check=True)
    print(result.stdout,end='')
