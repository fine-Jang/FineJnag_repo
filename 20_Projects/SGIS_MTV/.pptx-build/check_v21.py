from pathlib import Path
from html.parser import HTMLParser
import re
p=next((Path.cwd()/'20_Projects/SGIS_MTV').glob('*초안_v2.1.html'))
s=p.read_text(encoding='utf-8')
class Checker(HTMLParser):
    pass
Checker().feed(s)
print('chars',len(s),'sections',s.count('<section'),'tables',s.count('<table>'))
for t in ['IP 할당 필요','Master VM 3식 IP 할당 필요','재활용 TNS 장비 IP 할당 필요','TNS-2100','신규 IP']:
    print(repr(t),s.count(t))
print('svg ip badges',len(re.findall(r'class="small ip-required-text"',s)))
print('red flag css',s.count('.ip-required-bg'))
print('stale mapping',s.count('기존 장비 재구성 · 출처 확인 필요'),s.count('HV#02·HV#03 중 선정 필요'))
