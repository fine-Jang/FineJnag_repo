---
type: project
status: draft
created: 2026-10-14
target: SGIS_OCP_BuildDesign_v1.2.html
---

# 국데처 SGIS OpenShift 구축설계서 v1.2 릴리스 기록

v1.1([릴리스 기록](SGIS_OCP_BuildDesign_v1.1_notes.md))에 IP 할당 상세, 포트 속도, 이관 대상 VM 약식 정보를 반영한 버전입니다. 반영본은 [SGIS_OCP_BuildDesign_v1.2.html](SGIS_OCP_BuildDesign_v1.2.html)이며, v1.1은 그대로 둡니다.

## 변경 사항

1. **IP 할당 상세 표기 (02장)**: "● IP 할당 필요" 배지를 망별·장비별 필요 IP 내역과 개수로 바꿈.
   - Bastion(외부·내부): 2개 — 관리망 Bastion 호스트 1, nasbak 1(etcd 백업).
   - 외부망 Master(TNS-2100 #B): 5개 — 관리망 KVM 호스트 1, master-0·1·2 각 1, Bootstrap 1(임시).
   - 내부망 Master(HV#03): 5개 — 관리망 KVM 호스트 1, master-0·1·2 각 1, Bootstrap 1(임시).
   - IPMI IP는 BIOS에서 설정하므로 할당 요청 대상에서 제외(02·03·09장 IPMI 할당 항목 삭제, 망 정의 IPMI망은 "BIOS에서 설정 · 할당 요청 없음").
2. **03장 IP 표**
   - 전체 구성도 Master 배지를 "● IP 5: 호스트 1 · VM 3 · 임시 1"로 변경.
   - 호스트명·IP 할당표에 nasbak IP 열 추가(Bastion만 해당).
   - "망별 신규 IP 소요" 표 신규: 외부망 7(관리망 6 · nasbak 1), 내부망 7(관리망 6 · nasbak 1). Worker는 기존 IP 재사용, API·Ingress는 Bastion LB 사용으로 별도 VIP 없음, Bootstrap IP는 설치 후 반납 가능.
3. **포트 속도 (v1.1 이후 보류분)**: IPMI 1G, 그 외(관리망·서비스망·nasbak망, Bastion NAS/BK 포함) 10G로 확정.
   - 03장 포트 설명과 전체 구성도 주석의 "미확정" 문구 교체.
   - 09장 네트워크 담당 항목에서 "포트 속도"·"IPMI 대역"을 빼고 "망별 신규 IP 할당(외부 7 · 내부 7)", "TNS-2100 NIC 10G 지원 여부" 추가.
4. **이관 대상 VM 약식 (07장 신규)**: 망별 서비스 VM 수·OS·자원 표.
   - 외부망 11식(RHEL 8.9 8 · Windows Server 2022 3), vCPU 108 · 메모리 364GB · 데이터스토어 12.4TB.
   - 내부망 24식(RHEL 8.9 22 · Windows Server 2022 2), vCPU 196 · 메모리 760GB · 데이터스토어 62.3TB.
   - 제외: 망별 DNS VM 1식(Windows Server 2022, 별도 HV), vCenter, vCLS.
   - 문서 전체 VM 수 정정: 업무 VM 12 → 11(외부), 25 → 24(내부). 02장 행·작업 카드, 04장 수용 용량 표, 05장 스토리지 표 반영. 메모리 예상치(약 440GB·840GB)는 VM당 오버헤드 차이가 작아 유지.
5. 버전 태그: "VERSION 1.2 / 내부 구축팀용 초안 · IP 할당 상세 · 포트 속도 · 이관 VM 약식".

## 검증

- 구성도 SVG 글자 넘침 검사 결과 넘침 없음.
- 브라우저 렌더링으로 02장 IP 상세 박스, 03장 호스트명·IP 할당표·망별 신규 IP 소요 표 확인.
