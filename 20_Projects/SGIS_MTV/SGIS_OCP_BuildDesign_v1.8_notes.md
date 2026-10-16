---
type: project
status: draft
created: 2026-10-15
target: SGIS_OCP_BuildDesign_v1.7.html → SGIS_OCP_BuildDesign_v1.8.html
---

# 국데처 SGIS OpenShift 구축설계서 v1.8 릴리스 기록

v1.7([릴리스 기록](SGIS_OCP_BuildDesign_v1.7_notes.md))에서 개요 요약 추가, 인터페이스·IP 기입표 통합, VDDK 언급 삭제, 설치 파라미터 삭제를 반영한 버전입니다. 반영본은 [SGIS_OCP_BuildDesign_v1.8.html](SGIS_OCP_BuildDesign_v1.8.html)이며, v1.7은 그대로 둡니다.

## 결정 (2026-10-15)

- Master KVM 호스트는 관리망 IP를 따로 두지 않음. bond0 위 br0 브리지만 구성하고 Master VM·bootstrap을 연결.
- 신규 IP: 망별 7개 → 6개(관리망 5: Bastion 1 · master-0/1/2 3 · bootstrap 1(구성 완료 후 반납), nasbak 1: Bastion).
- 문서에서 VDDK는 언급하지 않음. MTV 이관 방식은 "vCenter·ESXi 443·902 경유 네트워크 복사"로 표기.

## 변경 사항

1. 버전 태그: "VERSION 1.8 / 기입 · 인쇄용 · 망별 구축 인프라 · 인터페이스·IP 기입표 통합".
2. **01 개요**:
   - 숫자 카드 4개를 이관 VM 기준으로 변경: 이관 대상 VM 35대 · 이관 VM vCPU 304(외부 108 / 내부 196) · 이관 VM 메모리 1,124GB(외부 364 / 내부 760GB) · 원본 데이터 74.7TB. 기존 "OpenShift 클러스터 2개"·"구성 서버 4식" 카드는 망별 구축 인프라 표로 대체.
   - 숫자 카드 아래 "망별 구축 인프라" 표 추가(카드·② 이관 대상 VM 표와 중복되지 않도록 인프라 위주).
     - 구축 인프라: 역할별 장비·코어·메모리, 합계(외부 4대 · 168코어 · 3,200GB / 내부 4대 · 180코어 · 3,648GB, Worker 96코어 · 2TB).
     - Worker1 단독 수용(이관 기간): CPU 요청·메모리 사용 예상(43% / 82%). 망별 VM 상세(OS·vCPU·메모리·데이터)는 ② 이관 대상 VM 표에서 표시.
3. **적용 버전**: MTV 비고 "VDDK 방식" → "콜드 이관".
4. **그림 2 망별 장비 재구성**: AS-IS가 신규 장비인 칸은 회색 점선 상자만 남기고 "— (미사용)" 문구 삭제. Master IP 표시 5개 → 4개, 내부 Master "호스트 IP 신규" → "호스트 관리망 IP 없음(br0)".
5. **03 네트워크**:
   - 그림 3 VM 네트워크 매핑 삭제. 구성 기준 "VM NIC 매핑"의 그림 3 참조 삭제, "Master KVM 호스트"에 "호스트 관리망 IP 없음" 추가.
   - "서버별 NIC 인터페이스"와 "장비별 IP 기입표"를 "서버별 인터페이스 · IP 기입표 — 신규 IP 망별 6개 (관리망 5 · nasbak 1)" 하나로 통합.
     - 망별로 ① 망 정보(관리망 대역/GW · nasbak 대역/VLAN · NTP · base domain, 기존 입력값 유지) ② 물리 서버 ③ Master · bootstrap VM 3개 표로 구성.
     - 물리 서버 표: 서버(장비) · 호스트명 · 망 · bond(망별 색상 표시) · 인터페이스 1 · 인터페이스 2 · IP · 비고. 서버에 있는 bond·IPMI만 행으로 두어 bond 포트 2개를 각각 기입. Master KVM 호스트 관리망 IP "IP 없음", Worker bond1·bond2 "IP 없음", bridge·VLAN은 비고에 표시.
     - Master · bootstrap VM 표: VM 1행씩 호스트명 · 인터페이스 · 관리망 IP(NIC 1개, 이중화 없음).
6. **05 클러스터 설치 설계(설치 파라미터)** 삭제, 이후 장 번호 당김: 05 MTV 이관 설계 · 06 설치 체크리스트 · 07 설계 제약 및 요청·협의 사항. 목차 링크도 같이 수정("07 제약·요청·협의").
7. **VDDK 언급 전부 삭제**: MTV 이관 기준의 Provider "VDDK 이미지 지정" · 이관 방식 "VDDK" · "VDDK 이미지" 행 · 전송 속도 "VDDK 복사 속도"(→ 네트워크 복사 속도), 체크리스트 1단계 "VDDK 이미지 빌드 → 미러 레지스트리 push" 행, 체크리스트 "vSphere Provider (VDDK 이미지 지정)".
8. **07 요청 및 협의 사항 8. 추가 IP 할당**: 망별 6개(관리망 5 · nasbak 1), "Master KVM 호스트는 관리망 IP 없음 (bond0 위 br0 브리지만 구성)". "내부 HV#03 기존 IP 재사용 시 1개 감소" 삭제.

## 검증

- 본문에 VDDK · "— (미사용)" · 그림 3 · "7개" · "IP 5개" 문구 없음을 스크립트로 확인.
- 기입칸 data-f 중복 없음 확인.
- 브라우저 렌더링으로 숫자 카드·망별 구축 인프라 표, 그림 2 외부망, 통합 기입표, 목차 번호 확인.

## 남은 사항

- Master KVM 호스트 원격 접속용 IP 필요 여부 추가 검토(필요 시 관리망 IP 1개 추가 → 망별 7개).
- 고객용 PPT v3.0pt도 신규 IP 개수(망별 6개)로 같이 수정함.
