---
type: project
status: draft
created: 2026-10-12
target: SGIS_MTV_WorkPlan_v2.3.html → SGIS_MTV_WorkPlan_v2.5.html
---

# 국데처 MTV 작업계획서 v2.5 수정안

V2.3 작업계획서를 기준으로 구성 명칭, DNS 전환, 일정 및 외부 Master 백업망 계획을 정합성 있게 반영한 릴리스 기록입니다. 반영본은 [SGIS_MTV_WorkPlan_v2.5.html](SGIS_MTV_WorkPlan_v2.5.html)입니다.

## v2.5 반영 사항

1. **작업 일정표와 상세 절차 통일**
   - Bastion 및 DNS·미러 레지스트리·로드밸런서 준비 → 기존 DNS 설정·레코드 이관과 질의 검증 → 원본 DNS VM 종료·보관 → 대상 HV 정리·재구성 → Master 및 Worker1 구축 → MTV 시험·본 이관 순서로 통일했습니다.
   - MTV 본 이관 후 업무 검증과 안정화를 완료하고 원복 조건을 확인한 뒤 Worker2로 전환합니다. 일정 지연 시 안정화 기간을 줄이지 않고 Worker2 전환을 이연합니다.

2. **망별 Bastion DNS 구축**
   - DNS VM은 MTV 대상에서 제외합니다. 외부·내부 각 망의 Bastion에 DNS 서비스를 구축하고 기존 DNS 설정 및 HV·vCenter 레코드를 이관합니다.
   - 질의, vCenter 및 ESXi 관리 연결을 검증한 뒤 기존 DNS VM을 종료·보관합니다. 외부 HV#02와 내부 HV#03은 DNS 전환 및 검증 후 재구성합니다.
   - DNS VM은 Windows·로컬 디스크 기반이며 HV와 vCenter의 이름 해석 용도로 확인된 실사 내용을 기준으로 합니다. 업무 서비스가 기존 DNS VM을 추가로 사용하는지 작업 전 확인합니다.

3. **Worker2 전환 표현 통일**
   - 구성도·장비 역할표·일정·절차에서 `이관·업무 검증·안정화 완료 후 Worker2 전환`으로 의미를 통일했습니다.
   - 외부 Worker2는 HV#01, 내부 Worker2는 HV#02이며 해당 호스트는 MTV 원본을 유지하다가 전환 조건 충족 후 재구성합니다.

4. **외부 Master의 NAS/BK 포설 및 etcd 백업**
   - 외부 Master KVM 호스트(TNS-2100)에 관리망 2포트와 별도로 NAS/BK망 2포트를 추가 포설하고 Bond를 구성하도록 명시했습니다.
   - 외부 클러스터의 etcd 백업을 NAS/BK망을 통해 통합 백업스토리지에 주기적으로 보관하고 복구 절차를 시험하도록 반영했습니다.
   - 이 추가 포설은 외부 Master에만 적용하며, 내부 Master HV#03에는 NAS/BK 추가 포설을 표시하지 않았습니다. 포트·스위치 포설과 백업 저장소 경로는 현장 확인 후 확정합니다.

5. **장비 출처와 IP 할당 표시 분리**
   - 신규 구매로 오해될 수 있는 `신규 투입 장비` 표현을 장비 출처를 뜻하는 `재활용 TNS-2100`으로 통일했습니다.
   - 장비표의 출처 열과 IP 계획 열을 분리하고, 신규 IP 필요 여부는 별도 배지로 표기했습니다. 외부 Master·외부 Bastion·내부 Bastion 및 내부 Master의 신규 IP 계획을 표에 명시했습니다. Worker IP는 기존 IP 재사용으로 구분했습니다.

## 유지한 현장 실사 기준

- 기존 VMware HV는 외부망 2대, 내부망 3대입니다.
- 업무 VM 원본은 외부 HV#01(12대)과 내부 HV#02(25대)입니다. 해당 호스트는 MTV 원본으로 유지하고, 검증·안정화 후 Worker2로 전환합니다.
- 외부 HV#02는 Worker1, 내부 HV#01은 Worker1, 내부 HV#03은 DNS 전환 후 Master KVM 호스트로 재구성합니다.
- 외부 Master와 외부·내부 Bastion은 재활용 TNS-2100을 사용합니다. 재활용 장비 출처와 IP 할당 여부는 별도 항목으로 관리합니다.
- vCenter, DNS VM, vCLS는 업무 VM MTV 이관 대상에서 제외합니다.

## 검토·검증

- 표·절차·구성도의 역할, 호스트 번호, DNS 전환 순서 및 Worker2 조건을 상호 대조합니다.
- HTML 태그 구조, 표 행·열, 버전 표기 및 변경 이력의 일관성을 확인한 뒤 릴리스합니다.
- 실제 DNS 설정·레코드, 신규 IP, NAS/BK 포트의 스위치 측 연결, 백업 대상·주기·복구 시험은 착수 전에 담당자와 확정합니다.