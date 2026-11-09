"""Run: python demo.py. Writes deterministic sample output."""
from pathlib import Path
from memory_engine import AssociativeMemory
import json

m=AssociativeMemory()
m.add('m1','Client onboarding requires verifying supplier insurance documents.', ['onboarding'],.8)
m.add('m2','Insurance certificates frequently expire before vendor renewal.', ['risk'],.9)
m.add('m3','Procurement approval is delayed when supplier records are incomplete.', ['onboarding'],.8)
m.add('m4','The marketing team prepares monthly social media reports.', ['marketing'],.5)
m.add('m5','An operations manager manually checks renewal dates in spreadsheets.', ['risk'],.7)
m.connect('m1','m2',.95,reason='document-dependency')
m.connect('m2','m5',.85,reason='renewal-risk')
query='supplier onboarding documents'
base=m.activate(query,goal='onboarding',spreading=0,feedback=False)
associative=m.activate(query,goal='onboarding',spreading=.95,feedback=False)
print('QUERY:',query)
print('BASELINE (direct relevance):',[(x['id'],x['score']) for x in base])
print('ASSOCIATIVE:',[(x['id'],x['score']) for x in associative])
print('ASSOCIATIVE GAIN:',[(x['id'],x['association_gain']) for x in associative])
m.reinforce('m1','m2',.05)
m.save(Path(__file__).parent/'sample_memory.json')
reloaded=AssociativeMemory.load(Path(__file__).parent/'sample_memory.json')
assert len(reloaded.nodes)==5
report={'query':query,'baseline':base,'associative':associative,'note':'Illustrative synthetic scenario; not a benchmark or evidence of superiority.'}
(Path(__file__).parent/'demo_results.json').write_text(json.dumps(report,indent=2))
