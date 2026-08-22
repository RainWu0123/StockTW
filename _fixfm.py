"""修復 frontmatter target_base 損壞（"target"字面值）與 confidence 損壞。"""
import re, glob
from pathlib import Path

RES=Path('/home/ubuntu/investment/research')
# 正確目標價（來自本 session 估值）
fixes={
 '2368_金像電.md':('1500','中高'),
 '2383_台光電.md':('5500','高'),
 '2449_京元電子.md':('350','中高'),
 '3017_奇鋐.md':('3600','高'),
 '2303_聯電.md':('135','中'),
 '2327_國巨.md':('700','中'),
 '2337_旺宏.md':('220','中'),
 '3008_大立光.md':('3200','中'),
 '3443_創意.md':('2900','中'),
 '3529_力旺.md':('3300','高'),
 '6415_矽力.md':('3500','中'),
 '6505_台塑化.md':('105','中'),
}
for fname,(t,c) in fixes.items():
    p=RES/fname
    if not p.exists(): print(fname,'MISSING'); continue
    t_text=p.read_text(encoding='utf-8')
    t_text=t_text.replace('target_base: "target"',f'target_base: "{t}"')
    t_text=t_text.replace('confidence: "confidence"',f'confidence: "{c}"')
    # 若無 target_base 則加
    if 'target_base:' not in t_text:
        parts=t_text.split('---',2)
        head=parts[1].rstrip('\n')+f'\ntarget_base: "{t}"\ntarget_date: "2026-08-22"\n'
        t_text='---'+head+'---'+parts[2]
    p.write_text(t_text,encoding='utf-8')
    print(fname,'fixed ->',t)

# 全庫掃描其他損壞
for f in glob.glob(str(RES/'*_*.md')):
    name=Path(f).name
    if name.startswith(('摘要_','追蹤_')) or name.endswith('.html'): continue
    text=open(f,encoding='utf-8').read()
    if 'target_base: "target"' in text or 'confidence: "confidence"' in text:
        print('STILL BROKEN:',name)
