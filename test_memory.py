import tempfile,unittest
from pathlib import Path
from memory_engine import AssociativeMemory
class TestMemory(unittest.TestCase):
 def test_association_activates_neighbor(self):
  m=AssociativeMemory();m.add('a','supplier onboarding insurance documents');m.add('b','renewal deadline risk');m.connect('a','b',1)
  direct={x['id']:x for x in m.activate('supplier onboarding insurance',spreading=0,top_k=2,feedback=False)}
  assoc={x['id']:x for x in m.activate('supplier onboarding insurance',spreading=1,top_k=2,feedback=False)}
  self.assertGreater(assoc['b']['score'],direct['b']['score'])
 def test_persistence(self):
  m=AssociativeMemory();m.add('a','alpha');m.add('b','beta');m.connect('a','b',.6)
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'m.json';m.save(p);r=AssociativeMemory.load(p)
   self.assertEqual(r.nodes['a'].links['b'],.6)
 def test_reinforce_and_weaken(self):
  m=AssociativeMemory();m.add('a','alpha');m.add('b','beta');m.connect('a','b',.5)
  m.reinforce('a','b',.2);self.assertAlmostEqual(m.nodes['a'].links['b'],.7)
  m.weaken('a','b',.1);self.assertAlmostEqual(m.nodes['b'].links['a'],.6)
 def test_no_unintended_feedback(self):
  m=AssociativeMemory();m.add('a','alpha');m.activate('alpha',feedback=False)
  self.assertEqual(m.nodes['a'].use_count,0)
if __name__=='__main__':unittest.main()
