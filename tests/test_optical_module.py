"""光通圖譜資料與網站入口契約。python3 -m unittest discover -s tests -p test_optical_module.py"""
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class OpticalModuleTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=json.loads((ROOT/'data/optical-module.json').read_text())
 def test_component_contract(self):
  self.assertEqual({x['id'] for x in self.data['components']},{'housing','connector','optics','laser','receiver','dsp','substrate','assembly'})
 def test_unique_and_resolved_sources(self):
  sources={x['id'] for x in self.data['sources']};self.assertEqual(len(sources),len(self.data['sources']))
  ids={x['id'] for x in self.data['suppliers']};self.assertEqual(len(ids),len(self.data['suppliers']))
  for item in self.data['suppliers']+self.data['components']:
   self.assertTrue(item['source_ids']);self.assertTrue(set(item['source_ids'])<=sources)
 def test_bidirectional_component_mapping(self):
  for c in self.data['components']:
   self.assertEqual(set(c['supplier_ids']),{s['id'] for s in self.data['suppliers'] if c['id'] in s['component_ids']})
 def test_no_share_without_scope(self):
  for s in self.data['suppliers']:
   m=s['market_share']
   if m['value'] is not None:
    self.assertIn(m['status'],['verified','historical_estimate'])
    for f in ['denominator','period','geography','source_ids','component_ids']:self.assertTrue(m[f])
    self.assertGreaterEqual(m['value'],0);self.assertLessEqual(m['value'],100)
   else:self.assertEqual(m['status'],'unconfirmed')
 def test_no_integrator_role_inference(self):
  suppliers={s['id']:s for s in self.data['suppliers']}
  for i in ['innolight','eoptolink','lumentum']:self.assertEqual(suppliers[i]['component_ids'],['assembly'])
  for i in ['broadcom','marvell','macom']:self.assertEqual(suppliers[i]['component_ids'],['dsp'])
 def test_tracking_matches_universe(self):
  u={s['code'] for s in json.loads((ROOT/'meta/research_universe.json').read_text())['stocks'] if s.get('status')=='active'}
  for s in self.data['suppliers']:
   self.assertEqual(s['research_status']=='tracked',s['country']=='台灣' and s.get('ticker') in u)
 def test_coexistence_and_assets(self):
  for f in ['spa.html','index.html']:
   t=(ROOT/f).read_text();self.assertIn('href="optical-module.html"',t);self.assertIn('id="stock-results"',t)
  for f in ['optical-module.html','optical-module.css','optical-module.js']:self.assertTrue((ROOT/f).is_file())
 def test_chains_cover_components(self):
  ids={s['id'] for s in self.data['suppliers']}; srcs={s['id'] for s in self.data['sources']}
  for c in self.data['components']:
   self.assertTrue(c.get('chains'))
   for ch in c['chains']:
    for st in ch['stages']:
     self.assertTrue(set(st.get('supplier_ids') or [])<=ids)
     self.assertTrue(set(st.get('source_ids') or [])<=srcs)
     self.assertIn(st['status'], {'product_role','gap','adjacent'})
if __name__=='__main__':unittest.main()
