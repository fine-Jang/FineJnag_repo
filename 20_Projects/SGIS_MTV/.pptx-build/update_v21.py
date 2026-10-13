from pathlib import Path
import re, html

root=Path.cwd()
target=next((root/'20_Projects/SGIS_MTV').glob('*초안_v2.1.html'))
s=target.read_text(encoding='utf-8')

def rows_table(section_id, table_no, rows):
    global s
    a=s.index(f'<section id="{section_id}"')
    b=s.index('</section>',a)+len('</section>')
    sec=s[a:b]
    tables=list(re.finditer(r'<table>[\s\S]*?</table>',sec))
    old=tables[table_no].group()
    header=rows[0]
    body=rows[1:]
    new='<table><thead><tr>'+''.join(f'<th>{html.escape(x)}</th>' for x in header)+'</tr></thead><tbody>'
    for row in body:
        new+='<tr>'+''.join(f'<td>{html.escape(x)}</td>' for x in row)+'</tr>'
    new+='</tbody></table>'
    sec=sec.replace(old,new,1)
    s=s[:a]+sec+s[b:]

rows_table('roles',0,[
 ['망','TO-BE 역할','장비 출처','IP 계획','전환 시점·확인 사항'],
 ['외부망','Master (KVM, VM 3식)','재활용 TNS-2100','신규 할당','초기 구축'],
 ['외부망','Bastion + 미러 레지스트리','재활용 TNS-2100','기존 IP 및 필요 주소 확인','초기 구축 · 상시 운영·백업'],
 ['외부망','Worker1','외부 HV#02','기존 IP 재사용','초기 구축 · MTV 이전'],
 ['외부망','Worker2','기존 HV#01','기존 IP 재사용','MTV 원본 유지 → 이관 후 전환'],
 ['내부망','Master (KVM, VM 3식)','기존 HV#03 재구성','HV#03 기존 IP 재사용','초기 구축'],
 ['내부망','Bastion + 미러 레지스트리','재활용 TNS-2100','신규 할당','초기 구축 · 상시 운영·백업'],
 ['내부망','Worker1','내부 HV#02 재구성','기존 IP 재사용','초기 구축 · MTV 이전'],
 ['내부망','Worker2','기존 HV#01','기존 IP 재사용','MTV 원본 유지 → 이관 후 전환'],
])
a=s.index('<section id="roles"'); b=s.index('</section>',a)+10
sec=s[a:b]
sec=re.sub(r'<p class="note">[\s\S]*?</p>', '<p class="note">기존 VMware 하이퍼바이저는 외부망 2대·내부망 3대입니다. 각 망 HV#01은 MTV 원본으로 유지하고, 외부 HV#02와 내부 HV#02를 Worker1으로 전환합니다. 내부 HV#03은 Master KVM 호스트로 재구성합니다. TNS-2100 5대 중 3대를 투입하고 2대는 예비로 둡니다. 전체 기존 HV 5대는 최종적으로 OpenShift 노드 또는 Master 호스트로 재구성합니다.</p>',sec,count=1)
s=s[:a]+sec+s[b:]

rows_table('procedure',0,[
 ['단계','작업 내용','진행 전 확인 / 완료 기준'],
 ['1. 현황·백업 확보','HV·VM·네트워크·FC LUN·VMFS 데이터스토어 현황과 설정을 기록하고 복구 가능한 백업을 확보합니다.','VM별 OS·NIC·디스크·부팅 설정, 콘솔 접근, HV#01 수용 자원을 확인합니다.'],
 ['2. VMware VM 집약','외부 VM 13식·내부 VM 26식을 각 망 HV#01로 집약하고 VMware 원본을 유지합니다.','VM 이동 방식과 서비스 정상 여부, 다른 HV의 VM 잔존 여부를 확인합니다.'],
 ['3. 비운 HV 초기화 준비','외부 HV#02와 내부 HV#02·HV#03에서 VMFS LUN 매핑을 해제하고 설정을 백업합니다.','대상 데이터 보존과 EMC Host Group 매핑 해제를 확인합니다.'],
 ['4. Bastion 구축','망별 Bastion에 RHEL 9.8, 미러 레지스트리, DNS·로드밸런서 기능을 구성하고 Ignition을 생성합니다.','외부·내부 각 1대의 미러 레지스트리 이미지 반입과 지속 운영·백업을 확인합니다.'],
 ['5. Master KVM 호스트 구성','외부 TNS-2100 및 내부 HV#03에 RHEL 9.8·KVM·네트워크 브리지를 구성합니다.','Master VM 3식과 Bootstrap 임시 VM 수용 자원, 지원·구독 조건을 확인합니다.'],
 ['6. Bootstrap·Master 설치','Master KVM 호스트의 임시 VM으로 Bootstrap을 구동하고 Master VM 3식을 설치합니다. 완료 후 Bootstrap VM을 제거하고 LB 대상에서 제외합니다.','UPI 설치 완료, etcd 디스크·지연, API 접근과 Master 상태를 확인합니다.'],
 ['7. Worker1 설치·편입','외부 HV#02와 내부 HV#02에 RHCOS를 설치하고 Worker1으로 편입합니다.','설치 디스크 by-id 지정, VMFS LUN 미매핑, CSR 승인 및 노드 정상 상태를 확인합니다.'],
 ['8. 클러스터 기반 구성','OpenShift Virtualization, NMState 네트워크, EMC CSI 드라이버와 StorageClass를 구성합니다.','Worker1 단독 운영 조건, CSI 볼륨 생성·접근, 원본·대상 동시 용량과 I/O를 검증합니다.'],
 ['9. MTV 설치·시험','Provider·VDDK·NetworkMap·StorageMap을 구성하고 주요 OS·NIC·디스크 유형별 시험 이관을 수행합니다.','버전 호환성, 연결·인증서·권한·통신과 시험 결과를 기록합니다.'],
 ['10. 회차별 본 이관','HV#01의 VM을 Worker1로 회차별 이관하고 기동·NIC·디스크·업무를 검증합니다.','외부 13식·내부 26식 전체 대상과 회차별 성공·실패·재작업을 기록합니다.'],
 ['11. Worker2 전환 판단','이관 완료, 최소 1주 안정화, 백업 복구 시험 및 업무 담당 확인 후 원본 보관 조건을 판단합니다.','원복 요청 없음, 데이터 정합성 및 원본 VM 종료·보관 상태를 확인합니다.'],
 ['12. Worker2 편입','HV#01의 LUN 매핑을 해제하고 RHCOS를 설치하여 Worker2로 편입합니다.','노드·네트워크·CSI 정상 상태와 합의된 VM 배치·이동 검증을 확인합니다.'],
 ['13. 최종 검증·결과서','최종 구성·IP·VM 이관 결과와 잔여 작업을 정리합니다.','OS·디스크·네트워크·업무·백업 및 합의된 검수 항목을 확인하고 결과서를 갱신합니다.'],
])

# Replace UPI instructions table (the table immediately following the UPI heading).
a=s.index('<h3>폐쇄망 UPI 설치 절차</h3>')
tb=s.index('<table>',a); te=s.index('</table>',tb)+8
upi=[
 ['단계','작업 내용'],
 ['1. 사전 준비','망별 Bastion에 설치 도구와 CLI를 준비하고 DNS·NTP·API·Ingress 로드밸런서 및 네트워크를 구성합니다.'],
 ['2. 폐쇄망 미러 구성','OCP·가상화·MTV·CSI 이미지를 망별 Bastion의 내부 미러 레지스트리에 반입하고 인증서·인증·미러 설정을 준비합니다.'],
 ['3. 설치 설정 생성','클러스터 구성과 미러 정보를 반영하여 install-config 및 Bootstrap·Master·Worker용 Ignition 파일을 생성합니다.'],
 ['4. 임시 Bootstrap·Master 설치','Master KVM 호스트의 임시 VM에서 Bootstrap을 구동하고 Master VM 3식을 설치합니다. Bootstrap 완료 후 임시 VM을 종료·삭제하고 로드밸런서 대상에서 제거합니다.'],
 ['5. Worker 노드 설치','외부 HV#02·내부 HV#02에 RHCOS와 Worker Ignition을 적용하고 CSR을 승인합니다. HV#01은 MTV 원본으로 유지합니다.'],
 ['6. 클러스터 완료 검증','노드·CSR·ClusterOperator 상태, API·콘솔·미러 접근을 확인하고 Virtualization·EMC CSI·MTV를 구성합니다.'],
 ['7. MTV 이후 Worker2 편입','원본 보관·원복 조건 충족 후 HV#01을 재구성하여 Worker2로 편입합니다.'],
]
new='<table><thead><tr>'+''.join(f'<th>{html.escape(x)}</th>' for x in upi[0])+'</tr></thead><tbody>'
for row in upi[1:]: new+='<tr>'+''.join(f'<td>{html.escape(x)}</td>' for x in row)+'</tr>'
new+='</tbody></table>'
s=s[:tb]+new+s[te:]
s=s.replace('설치 방식은 UPI로 확정합니다. Master 실제 노드 수·HA 구성, 초기 Worker1 단독 운영의 지원 조건 및 Bootstrap 자원 배치는 구축 전 확인합니다.', '설치 방식은 폐쇄망 UPI로 진행합니다. Master VM 3식은 외부 TNS-2100 및 내부 HV#03의 KVM 호스트에서 운영합니다. Master 호스트 장애 시 API가 중단되는 물리 단일 장애점과 초기 Worker1 단독 운영의 지원 조건을 확인합니다. etcd는 SSD/NVMe를 사용하고 fsync 지연 10ms 이하를 확인하며, etcd 백업은 KVM 호스트 외부에 보관하고 복구 절차를 마련합니다. Worker1 단독 운영 기간에는 Live Migration이 불가하므로 노드 재부팅·OCP 업데이트·MachineConfig 변경을 통제합니다.')

rows_table('schedule',0,[
 ['차수','시기','작업'],
 ['1차 사전작업','2026년 10월','행정작업·장비 재배치·전기 포설·현황 조사·백업·이미지 반입 준비'],
 ['2차 재구성','2026년 11월','VM 집약 → HV 초기화 → Bastion → Master KVM·VM → Worker1 → Virtualization·CSI·MTV 구성 및 시험 이관'],
 ['3차 MTV','2026년 12월','본 이관 → 안정화 → Worker2 편입 → 최종 검증 (12월 말 종료 목표)'],
])
a=s.index('<section id="schedule"'); b=s.index('</section>',a)+10
sec=s[a:b]
sec=sec.replace('<h3>실행 전 확정 항목</h3>', '''<h3>12월 상세 일정 (안 A · 작업일 확정 시 조정)</h3><div class="tablewrap"><table><thead><tr><th>기간</th><th>작업</th><th>다음 단계 진행 조건</th></tr></thead><tbody><tr><td>12/1 ~ 12/11</td><td>회차별 본 이관 (외부 13식·내부 26식)</td><td>회차별 이관 완료 점검표 통과</td></tr><tr><td>12/14 ~ 12/23</td><td>업무 안정화·백업 확인·원본 VM 전원 종료 보관</td><td>최소 1주 무장애 및 원복 불필요 판단</td></tr><tr><td>12/24 ~ 12/30</td><td>각 망 HV#01을 Worker2로 편입</td><td>노드·네트워크·CSI 정상 확인</td></tr><tr><td>12/31</td><td>최종 검증·결과서</td><td>완료</td></tr></tbody></table></div><ul><li>Worker2 전환은 최소 1주 안정화, 원복 요청 없음, 백업 복구 시험 통과 및 업무 담당 확인을 조건으로 합니다.</li><li>12/11까지 이관이 끝나지 않으면 안정화 기간을 줄이지 않고 Worker2 전환을 1월로 이연합니다.</li><li>원본 LUN·데이터스토어 회수는 Worker2 전환과 별도로 판단합니다. 12/25 휴일과 연말 작업 가능일을 고려합니다.</li></ul><h3>실행 전 확정 항목</h3>''')
sec=sec.replace('외부 Bastion 장비 출처, 내부 HV#02·HV#03의 Worker1 배정·잔여 장비 용도 및 실제 장비 식별정보','내부 HV#03 Master KVM 호스트 사양 및 지원 여부, 외부·내부 장비별 식별정보와 TNS-2100 3대 배정')
sec=sec.replace('Master 물리·가상 구성과 노드 수·HA 설계, UPI용 Bootstrap 및 로드밸런서 배치','Master VM 3식 구성의 지원 여부, 물리 단일 장애점·HA 조건, 임시 Bootstrap 자원 및 로드밸런서 배치')
sec=sec.replace('MTV 예상 2개월','MTV 수행 기간 1개월')
sec=sec.replace('적용 범위·회차별 일정·완료일 미확정','2026년 12월 말 종료 목표 · 회차별 실제 작업일은 확정 필요')
sec=sec.replace('</ul>\n<p class="muted">', '''<li>vCenter 유무와 대상 39식 포함 여부, VM 집약·Warm 이관·Provider 구성 영향 및 VDDK 이미지 반입 여부</li><li>OCP 4.22 기준 MTV 2.12 호환 조합, EMC 모델·펌웨어·CSI 지원 여부와 Copy Offload 가능성</li><li>KVM 호스트·Bastion RHEL 및 OpenShift Virtualization 구독 범위</li></ul>
<p class="muted">''')
s=s[:a]+sec+s[b:]

# Correct role/IP narrative and add an explicit technical validation register.
s=s.replace('외부 Master, 내부 Master·Bastion','외부 Master KVM 호스트·Master VM 3식·임시 Bootstrap·Bastion 및 API/Ingress VIP, 내부 Master VM 3식·임시 Bootstrap·Bastion 및 API/Ingress VIP')
s=s.replace('기존 VMware 하이퍼바이저는 외부망 2대·내부망 3대입니다.', '기존 VMware 하이퍼바이저는 외부망 2대·내부망 3대입니다.')
a=s.index('<section id="verify"'); b=s.index('</section>',a)+10
sec=s[a:b]
insert='''<h3>추가 기술 확인 항목</h3><div class="tablewrap"><table><thead><tr><th>항목</th><th>확인 내용</th></tr></thead><tbody><tr><td>내부 HV#03</td><td>Master VM 3식과 Bootstrap 수용 가능 여부를 확인합니다. 초기 산정 참고치는 약 28~32 vCPU·112~128GB 메모리·SSD이며 실제 요구량과 지원 구성을 검증합니다.</td></tr><tr><td>MTV 버전</td><td>OCP 4.22와 정합되는 MTV 2.12 지원 조합을 기준으로 확인하고 구축 시점의 제품 지원 문서를 대조합니다.</td></tr><tr><td>EMC CSI</td><td>스토리지 모델·펌웨어, CSI 드라이버의 OCP 지원 범위 및 실제 연결 프로토콜을 확인합니다. 미지원 시 대체 구성을 검토합니다.</td></tr><tr><td>Copy Offload</td><td>동일 EMC의 원본·대상에서 복사 오프로드 지원 여부를 시험 이관으로 확인하고, 이관 시간 산정에 반영합니다.</td></tr><tr><td>vCenter·VDDK</td><td>vCenter 유무와 39식 대상 포함 여부를 확인하고, VM 집약·Warm 이관·Provider 설정 및 VDDK 이미지 반입 필요성을 확인합니다.</td></tr><tr><td>구독</td><td>KVM 호스트·Bastion RHEL 구독 및 OpenShift Virtualization 구독 범위를 확인합니다.</td></tr></tbody></table></div><p class="note">HV#01을 Worker2로 재설치하기 전 EMC Host Group에서 해당 호스트의 VMFS LUN 매핑을 해제합니다. 설치 디스크는 /dev/disk/by-id로 명시하고, 필요한 RHCOS 멀티패스 설정을 적용합니다.</p>'''
sec=sec.replace('<h3>단계별 원복 방향</h3>',insert+'<h3>단계별 원복 방향</h3>')
s=s[:a]+sec+s[b:]

# Version the delivered document and clarify the schedule duration in visible content.
s=s.replace('작업계획서 · 초안 v0.2','작업계획서 · 초안 v2.1')
s=s.replace('작업계획서 V4','작업계획서 v2.1')
s=s.replace('기존 HV 5대 외부망 2 / 내부망 3','기존 HV 5대 외부망 2 / 내부망 3')
target.write_text(s,encoding='utf-8')
print(f'Updated {target} ({len(s)} chars)')
