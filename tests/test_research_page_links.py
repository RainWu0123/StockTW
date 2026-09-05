"""個股研究頁 ↔ CPO／可插拔 deep link。oracle 來自資料契約與已知代碼，不重跑被測函式。"""
import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CPO_REQUIRED = ['lid', 'asic', 'engine', 'fiber', 'els', 'substrate', 'foundry', 'assembly']
OM_REQUIRED = ['housing', 'connector', 'optics', 'laser', 'receiver', 'dsp', 'substrate', 'assembly']


def node_json(source: str):
    result = subprocess.run(
        ['node', '--input-type=module', '-e', source],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
    )
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)
    return json.loads(result.stdout)


def eval_expr(expr: str, setup: str = '') -> Any:
    return node_json(
        "import { linksForTicker, tickerFromFilename, resolveCodeParam, "
        "resolveComponentParam, fileForCode, localResearchHref, parseResearchFilenames, "
        "parseResearchFilenamesFromIndex, parseResearchFilenamesFromUniverse, "
        "loadResearchFilenames } from './research-links.js';\n"
        + setup
        + "\nconst __out = await (async () => (" + expr + "))();\n"
        + "console.log(JSON.stringify(__out));\n"
    )


class ResearchPageLinksTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cpo = json.loads((ROOT / 'data/cpo.json').read_text())
        cls.om = json.loads((ROOT / 'data/optical-module.json').read_text())
        cls.scope = json.loads((ROOT / 'data/research-scope.json').read_text())

    def test_ticker_from_research_filename(self):
        self.assertEqual(eval_expr("tickerFromFilename('2330_台積電.md')"), '2330')
        self.assertEqual(eval_expr("tickerFromFilename('research/4971_IET-KY.md')"), '4971')
        self.assertEqual(eval_expr("tickerFromFilename('')"), '')

    def test_code_query_is_sanitized(self):
        self.assertEqual(eval_expr("resolveCodeParam('?code=2330')"), '2330')
        self.assertEqual(eval_expr("resolveCodeParam('code=3081&x=1')"), '3081')
        self.assertEqual(eval_expr("resolveCodeParam('?code=../etc/passwd')"), '')
        self.assertEqual(eval_expr("resolveCodeParam('?code=<script>')"), '')

    def test_file_for_code_uses_filename_prefix(self):
        setup = "const files=['1101_台泥.md','2330_台積電.md','3081_聯亞.md'];"
        self.assertEqual(eval_expr("fileForCode('2330', files)", setup), '2330_台積電.md')
        self.assertEqual(eval_expr("fileForCode('9999', files)", setup), '')

    def test_links_for_tsmc_use_cpo_supplier_components_only(self):
        setup = (
            "import { readFileSync } from 'fs';"
            "const cpo=JSON.parse(readFileSync('data/cpo.json','utf8'));"
            "const om=JSON.parse(readFileSync('data/optical-module.json','utf8'));"
            "const datasets=["
            "{page:'cpo',href:'cpo.html',label:'CPO 拆解',suppliers:cpo.suppliers,components:cpo.components},"
            "{page:'optical-module',href:'optical-module.html',label:'可插拔光通',"
            "suppliers:om.suppliers,components:om.components}];"
        )
        links = eval_expr("linksForTicker('2330', datasets)", setup)
        self.assertEqual([p['page'] for p in links], ['cpo'])
        self.assertEqual([c['id'] for c in links[0]['components']], ['foundry', 'substrate'])
        self.assertEqual(links[0]['components'][0]['href'], 'cpo.html?component=foundry')
        self.assertEqual(links[0]['href'], 'cpo.html')

    def test_links_for_union_and_unrelated(self):
        setup = (
            "import { readFileSync } from 'fs';"
            "const cpo=JSON.parse(readFileSync('data/cpo.json','utf8'));"
            "const om=JSON.parse(readFileSync('data/optical-module.json','utf8'));"
            "const datasets=["
            "{page:'cpo',href:'cpo.html',label:'CPO 拆解',suppliers:cpo.suppliers,components:cpo.components},"
            "{page:'optical-module',href:'optical-module.html',label:'可插拔光通',"
            "suppliers:om.suppliers,components:om.components}];"
        )
        union = eval_expr("linksForTicker('3081', datasets)", setup)
        self.assertEqual(
            [(p['page'], [c['id'] for c in p['components']]) for p in union],
            [('cpo', ['els']), ('optical-module', ['laser'])],
        )
        self.assertEqual(eval_expr("linksForTicker('1101', datasets)", setup), [])
        self.assertEqual(eval_expr("linksForTicker('', datasets)", setup), [])

    def test_component_param_valid_and_invalid(self):
        self.assertEqual(
            eval_expr("resolveComponentParam('?component=lid', ['lid','assembly'], 'assembly')"),
            'lid',
        )
        self.assertEqual(
            eval_expr("resolveComponentParam('?component=housing', ['lid','assembly'], 'assembly')"),
            'assembly',
        )
        self.assertEqual(
            eval_expr("resolveComponentParam('', ['lid','assembly'], 'assembly')"),
            'assembly',
        )
        self.assertEqual(
            eval_expr("resolveComponentParam('?component=laser%2f..', " + json.dumps(CPO_REQUIRED) + ", 'assembly')"),
            'assembly',
        )
        self.assertEqual(
            eval_expr("resolveComponentParam('?component=laser', " + json.dumps(OM_REQUIRED) + ", 'assembly')"),
            'laser',
        )

    def test_local_research_href_requires_indexed_file(self):
        self.assertEqual(eval_expr("localResearchHref({ticker:'3363'}, [])"), '')
        self.assertEqual(eval_expr("localResearchHref({ticker:'AVGO'}, [])"), '')
        self.assertEqual(eval_expr("localResearchHref({ticker:'3234'}, ['3234_光環.md'])"), 'research.html?code=3234')
        self.assertEqual(
            eval_expr("localResearchHref({ticker:'2330', research_url:'https://github.com/x'}, [])"),
            '',
        )
        self.assertEqual(eval_expr("localResearchHref({ticker:''}, ['2330_台積電.md'])"), '')

    def test_parse_research_filenames_from_listing(self):
        html = '<a href="2330_%E5%8F%B0%E7%A9%8D%E9%9B%BB.md">x</a><a href="../secret.md">n</a>'
        self.assertEqual(
            eval_expr('parseResearchFilenames(' + json.dumps(html) + ')'),
            ['2330_台積電.md'],
        )

    def test_index_and_universe_filenames_without_guessing(self):
        setup = (
            "import { readFileSync } from 'fs';"
            "const md=readFileSync('INDEX.md','utf8');"
            "const universe=JSON.parse(readFileSync('meta/research_universe.json','utf8'));"
        )
        from_index = list(eval_expr('parseResearchFilenamesFromIndex(md)', setup))
        from_universe = list(eval_expr('parseResearchFilenamesFromUniverse(universe)', setup))
        for name in ('3081_聯亞.md', '3163_波若威.md', '3234_光環.md', '2330_台積電.md',
                     '3363_上詮.md', '6213_聯茂.md', '8996_高力.md', '2421_建準.md', '8358_金居.md'):
            self.assertIn(name, from_index)
        for name in ('3081_聯亞.md', '3363_上詮.md', '6213_聯茂.md', '8996_高力.md',
                     '2421_建準.md', '8358_金居.md'):
            self.assertIn(name, from_universe)
        self.assertNotIn('3234_光環.md', from_universe)

    def test_load_filenames_when_research_dir_404(self):
        setup = (
            "import { readFileSync } from 'fs';"
            "const md=readFileSync('INDEX.md','utf8');"
            "const universe=JSON.parse(readFileSync('meta/research_universe.json','utf8'));"
            "const fetchImpl=async (url)=>{"
            "  const u=String(url);"
            "  if(u.includes('INDEX.md')) return {ok:true,text:async()=>md,json:async()=>({})};"
            "  if(u.includes('research_universe')) return {ok:true,text:async()=>'',json:async()=>universe};"
            "  return {ok:false,status:404,text:async()=>'Not Found',json:async()=>({})};"
            "};"
        )
        files = eval_expr('loadResearchFilenames(fetchImpl)', setup)
        self.assertIn('3081_聯亞.md', files)
        self.assertIn('3163_波若威.md', files)
        self.assertIn('3234_光環.md', files)
        self.assertIn('3363_上詮.md', files)
        self.assertIn('6213_聯茂.md', files)

    def test_origin_main_index_has_real_research_paths(self):
        shown = subprocess.run(
            ['git', 'show', 'origin/main:INDEX.md'],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
        )
        if shown.returncode != 0:
            self.skipTest('origin/main INDEX.md unavailable')
        files = eval_expr(
            'parseResearchFilenamesFromIndex(md)',
            'const md=' + json.dumps(shown.stdout) + ';',
        )
        for name in ('3081_聯亞.md', '3163_波若威.md', '2330_台積電.md'):
            self.assertIn(name, files)

    def test_research_html_fetches_maps_not_static_company_list(self):
        html = (ROOT / 'research.html').read_text()
        links = (ROOT / 'research-links.js').read_text()
        self.assertIn('data/cpo.json', html)
        self.assertIn('data/optical-module.json', html)
        self.assertIn('research-links.js', html)
        self.assertIn('loadResearchFilenames', html)
        self.assertIn('./INDEX.md', links)
        self.assertIn('./meta/research_universe.json', links)
        self.assertNotIn('2330: cpo', html)
        self.assertNotIn("pages: [{page: 'cpo'", html)

    def test_public_scope_has_four_rules_and_no_removal_candidates(self):
        self.assertEqual(
            self.scope['policy'],
            ['0050持股', '00981A可核對持股', '熱門族群股票', '製作人過去常談或明確指定'],
        )
        items = self.scope['items']
        codes = [item['code'] for item in items]
        self.assertEqual(len(codes), len(set(codes)))
        self.assertNotIn('2312', codes)
        self.assertNotIn('2348', codes)
        self.assertNotIn('6269', codes)
        for code in ('4953', '4939', '6226', '3490', '1303', '2345', '2881', '2882',
                     '2449', '1301', '1326', '6505', '2603', '3363', '6213', '8996', '2421', '8358'):
            self.assertIn(code, codes)

    def test_public_scope_report_status_matches_filesystem(self):
        for item in self.scope['items']:
            if item['status'] == 'available':
                self.assertTrue(item['report_file'])
                self.assertTrue((ROOT / 'research' / item['report_file']).is_file())
            else:
                self.assertEqual(item['status'], 'pending_research')
                self.assertIsNone(item['report_file'])
        self.assertFalse(self.scope['etf_evidence']['00981A']['complete'])
        self.assertEqual(sum('0050' in item['categories'] for item in self.scope['items']), 50)
        self.assertEqual(sum('00981A' in item['categories'] for item in self.scope['items']), 36)

    def test_research_html_uses_reviewed_scope_and_no_stale_fallback(self):
        html = (ROOT / 'research.html').read_text()
        self.assertIn('./data/research-scope.json', html)
        self.assertIn('pending_research', (ROOT / 'data/research-scope.json').read_text())
        self.assertNotIn('FALLBACK_FILES', html)
        self.assertNotIn('1303_台塑化.md', html)
        self.assertNotIn('2345_鴻準.md', html)

    def test_interactive_js_uses_shared_resolver_and_keeps_research_url(self):
        for name in ('cpo.js', 'optical-module.js'):
            text = (ROOT / name).read_text()
            self.assertIn("from './research-links.js'", text)
            self.assertIn('resolveComponentParam', text)
            self.assertIn('localResearchHref', text)
            self.assertIn('loadResearchFilenames', text)
            self.assertIn('s.research_url&&safeUrl(s.research_url)', text)


if __name__ == '__main__':
    unittest.main()
