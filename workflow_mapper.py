"""Illustrative workflow discovery from synthetic structured events (not live integrations)."""
from collections import defaultdict
import json
from pathlib import Path
EVENTS=[
 {'case':'A','step':'receive_request','actor':'sales','system':'inbox'},
 {'case':'A','step':'check_documents','actor':'ops','system':'spreadsheet'},
 {'case':'A','step':'request_missing_document','actor':'ops','system':'email'},
 {'case':'A','step':'check_documents','actor':'ops','system':'spreadsheet'},
 {'case':'A','step':'approve','actor':'manager','system':'email'},
 {'case':'B','step':'receive_request','actor':'sales','system':'inbox'},
 {'case':'B','step':'check_documents','actor':'ops','system':'spreadsheet'},
 {'case':'B','step':'approve','actor':'manager','system':'email'},
]
def analyze(events):
 by_case=defaultdict(list)
 for e in events: by_case[e['case']].append(e)
 transitions=defaultdict(int); handoffs=defaultdict(int)
 for trace in by_case.values():
  for a,b in zip(trace,trace[1:]):
   transitions[(a['step'],b['step'])]+=1
   if a['actor']!=b['actor']: handoffs[(a['actor'],b['actor'])]+=1
 candidates=[]
 for step in sorted({e['step'] for e in events}):
  sample=[e for e in events if e['step']==step]
  if step=='check_documents':
   candidates.append({'task':'document completeness check','observed_events':len(sample),
    'candidate_agent':'DocumentCheckAssistant','proposal':'check required fields, flag missing documents',
    'validation':'compare with human-reviewed cases; human approves final decisions',
    'status':'PROPOSED - not generated or deployed'})
 return {'cases':len(by_case),'transitions':[{'from':a,'to':b,'count':n} for (a,b),n in sorted(transitions.items())],
  'handoffs':[{'from':a,'to':b,'count':n} for (a,b),n in sorted(handoffs.items())],
  'candidate_agents':candidates}
if __name__=='__main__':
 result=analyze(EVENTS)
 print(json.dumps(result,indent=2))
 (Path(__file__).parent/'workflow_results.json').write_text(json.dumps(result,indent=2))
