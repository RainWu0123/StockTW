"""CPO 公開資料與入口契約；互動另用真瀏覽器驗收。"""
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class CpoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads((ROOT/'data/cpo.json').read_text())
    def test_navigation_coexists(self):
        for name in ['spa.html','index.html','optical-module.html']:
            self.assertIn('href="cpo.html"', (ROOT/name).read_text())
        self.assertIn('href="optical-module.html"', (ROOT/'cpo.html').read_text())
    def test_components(self):
        self.assertEqual({c['id'] for c in self.d['components']}, {'lid','asic','engine','fiber','els','substrate','foundry','assembly'})
    def test_references(self):
        sources = {s['id'] for s in self.d['sources']}
        firms = {s['id'] for s in self.d['suppliers']}
        self.assertEqual(len(sources),len(self.d['sources']))
        self.assertEqual(len(firms),len(self.d['suppliers']))
        for x in self.d['components']+self.d['suppliers']:
            self.assertTrue(x['source_ids'])
            self.assertLessEqual(set(x['source_ids']),sources)
        for c in self.d['components']:
            self.assertEqual(set(c['supplier_ids']), {s['id'] for s in self.d['suppliers'] if c['id'] in s['component_ids']})
            self.assertTrue(c['chains'])
            for ch in c['chains']:
                for st in ch['stages']:
                    self.assertLessEqual(set(st['supplier_ids']),firms)
                    self.assertLessEqual(set(st['source_ids']),sources)
                    self.assertIn(st['status'],['product_role','adjacent','gap'])
    def test_share_scope(self):
        for s in self.d['suppliers']:
            m=s['market_share']
            if m['value'] is None:
                self.assertEqual(m['status'],'unconfirmed')
            else:
                for f in ['component_ids','denominator','geography','period','source_ids']:
                    self.assertTrue(m[f])
                self.assertTrue(0 <= m['value'] <= 100)
    def test_tracking(self):
        active={s['code'] for s in json.loads((ROOT/'meta/research_universe.json').read_text())['stocks'] if s.get('status')=='active'}
        for s in self.d['suppliers']:
            self.assertEqual(s['research_status']=='tracked',s['country']=='台灣' and s.get('ticker') in active)
if __name__=='__main__': unittest.main()
