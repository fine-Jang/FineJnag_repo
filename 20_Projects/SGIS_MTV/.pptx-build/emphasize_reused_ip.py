from pathlib import Path
import re

p=next((Path.cwd()/'20_Projects/SGIS_MTV').glob('*초안_v2.1.html'))
s=p.read_text(encoding='utf-8')

# Make reused TNS equipment and IP action visually distinct in the diagrams.
s=s.replace('.new-server{fill:#eaf3ff;stroke:#2f66b3;stroke-width:2.2;stroke-dasharray:7 4}', '.new-server{fill:#dceaff;stroke:#174e91;stroke-width:3;stroke-dasharray:7 4}')
s=s.replace('.badge-new{display:inline-block;font-size:12px;padding:1px 8px;border:1.5px dashed #2f66b3;background:#eaf3ff;color:#244f8c;white-space:nowrap}', '.badge-new{display:inline-block;font-size:12px;padding:2px 9px;border:2px solid #174e91;background:#dceaff;color:#173f73;font-weight:700;white-space:nowrap}.ip-required{display:inline-block;margin:2px 4px;padding:2px 8px;border:1px solid #9b351c;border-radius:4px;background:#a94325;color:#fff;font-size:12px;font-weight:700;white-space:nowrap}.ip-required-bg{fill:#a94325;stroke:#762b19;stroke-width:1.5}.ip-required-text{fill:#fff;font-weight:700}')
s=s.replace('<text x="625" y="187" text-anchor="middle" class="small">KVM 호스트 · 신규 IP</text>', '<text x="625" y="164" text-anchor="middle" class="small">KVM 호스트</text><rect x="570" y="171" width="110" height="23" rx="5" class="ip-required-bg"/><text x="625" y="187" text-anchor="middle" class="small ip-required-text">IP 할당 필요</text>')
s=s.replace('<text x="790" y="187" text-anchor="middle" class="small">신규 IP</text>', '<rect x="735" y="171" width="110" height="23" rx="5" class="ip-required-bg"/><text x="790" y="187" text-anchor="middle" class="small ip-required-text">IP 할당 필요</text>')

# Highlight the matching role rows, including the new addresses for Master VMs on the reused internal HV#03.
s=s.replace('<td>호스트·VM 3식 신규 할당</td>', '<td><span class="ip-required">IP 할당 필요</span><br>호스트·VM 3식</td>')
s=s.replace('<td>신규 할당</td><td>2차 재구성 · 최초 구축</td>', '<td><span class="ip-required">IP 할당 필요</span></td><td>2차 재구성 · 최초 구축</td>')
s=s.replace('<td>호스트 기존 IP 재사용 · VM 3식 신규 할당</td>', '<td>호스트 기존 IP 재사용<br><span class="ip-required">Master VM 3식 IP 할당 필요</span></td>')

# Give the IP inventory row an explicit highlighted action for reused TNS servers.
s=s.replace('외부: Master KVM 호스트, Master VM 3, Bootstrap(임시), Bastion 내부: Master VM 3, Bootstrap(임시), Bastion (KVM 호스트는 HV#03 기존 IP 재사용)', '외부: 재활용 TNS Master 호스트·Master VM 3식·임시 Bootstrap·재활용 TNS Bastion·API/Ingress VIP. 내부: Master VM 3식·임시 Bootstrap·재활용 TNS Bastion·API/Ingress VIP (HV#03 Master 호스트는 기존 IP 재사용). <span class="ip-required">재활용 TNS 장비 IP 할당 필요</span>')

# Add a clear legend explaining the red callout without changing the diagram's network meaning.
s=s.replace('청회색 영역: VM 풀 · 주황색 강조: MTV 이후 전환하는 Worker2', '청회색 영역: VM 풀 · 주황색 강조: MTV 이후 Worker2 · <span class="ip-required">적색 표식: IP 할당 필요</span>')

# Ensure each reused TNS role has the same prominent callout in the allocation table.
ra=s.index('<section id="roles"'); rb=s.index('</section>',ra)
role_sec=s[ra:rb]
def mark_reused_row(m):
    row=m.group(0)
    if 'TNS-2100' not in row:
        return row
    cells=list(re.finditer(r'<td>([\s\S]*?)</td>',row))
    if len(cells)<4 or 'ip-required' in cells[3].group(1):
        return row
    cell=cells[3]
    marked='<span class="ip-required">IP 할당 필요</span><br>'+cell.group(1)
    return row[:cell.start(1)]+marked+row[cell.end(1):]
role_sec=re.sub(r'<tr>[\s\S]*?</tr>',mark_reused_row,role_sec)
def mark_internal_master(m):
    row=m.group(0)
    if 'HV#03' not in row or 'ip-required' in row:
        return row
    cells=list(re.finditer(r'<td>([\s\S]*?)</td>',row))
    if len(cells)<4: return row
    cell=cells[3]
    marked=cell.group(1)+'<br><span class="ip-required">Master VM 3식 IP 할당 필요</span>'
    return row[:cell.start(1)]+marked+row[cell.end(1):]
role_sec=re.sub(r'<tr>[\s\S]*?</tr>',mark_internal_master,role_sec)
s=s[:ra]+role_sec+s[rb:]

# Add a callout in the network/IP plan itself, so readers see the action beside the address scope.
na=s.index('<section id="network"'); nb=s.index('</section>',na)
net_sec=s[na:nb]
def mark_ip_scope(m):
    row=m.group(0)
    if '신규 IP' not in row or 'ip-required' in row:
        return row
    cells=list(re.finditer(r'<td>([\s\S]*?)</td>',row))
    if len(cells)<3: return row
    cell=cells[-1]
    marked=cell.group(1)+'<br><span class="ip-required">재활용 TNS 및 Master VM IP 할당 필요</span>'
    return row[:cell.start(1)]+marked+row[cell.end(1):]
net_sec=re.sub(r'<tr>[\s\S]*?</tr>',mark_ip_scope,net_sec)
s=s[:na]+net_sec+s[nb:]
p.write_text(s,encoding='utf-8')
print('Updated reused-equipment and IP allocation emphasis')
