---
type: project
status: draft
created: 2026-10-20
target: SGIS_OCP_WorkPlan_v0.1.html
---

# 국데처 SGIS OpenShift 전환 작업계획서 v0.1 릴리스 기록

내부 작업자용 작업계획서의 첫 버전입니다. 반영본은 [SGIS_OCP_WorkPlan_v0.1.html](SGIS_OCP_WorkPlan_v0.1.html)이며, 근거는 [구축설계서 v1.9t](SGIS_OCP_BuildDesign_v1.9t_notes.md)와 [고객용 계획 v3.0pt](SGIS_MTV_WorkPlan_v3.0pt_notes.md)입니다. 고객 제출용 작업계획서(SGIS_MTV_WorkPlan v2.9)와는 별도 문서입니다.

## 결정

- 독자: 내부 구축팀. 출력해서 보면서 작업하는 문서.
- 단계별로 할 일 순서 · 명령 예시 · 확인 기준을 적음. 체크리스트는 넣지 않음(설계서 04장 체크리스트와 별도).
- 명령은 예시. 테스트 환경에서 실행하며 확정하고, 확정 전 명령은 "예시", 미확정 값은 TBD로 표시.
- IP · 호스트명은 `<Bastion IP>` 같은 자리표시자로만 표기(실제 값은 구축설계서 IP 기입표).
- 외부망 · 내부망은 순서가 같아 한 번만 쓰고, 망별 장비만 표로 구분. 외부망 먼저 진행.
- 방침: 콜드 이관, VMware Tools 미설치 · 이관 후 IP 직접 설정, Master KVM 관리망 4회선(bond0 호스트 IP · bond1 → br0), 신규 IP 망별 7개, master-1·2·3, bootstrap은 master 구성 후 반납.

## 구성

- 00 작업 전 확인 — 전체 8단계 흐름, 망별 대상 장비, 시작 전에 받아 둘 것(IP · 망 정보 · 방화벽 · 설치 미디어 · IPMI · vCenter 계정)
- 01 장비 설치 · 결선 — 장비별 관리망 · 서비스망 · nasbak · IPMI · FC 회선
- 02 Bastion 구축 — OS · bond, chrony, DNS(bind), HAProxy, Ignition HTTP, 미러 레지스트리 · oc-mirror
- 03 HV 정리 — vMotion, ESXi 설정 백업, 호스트 제거, MTV 계정(VMware 엔지니어)
- 04 Master 구성 · 클러스터 설치 — KVM 호스트 네트워크, install-config · ignition, VM 생성(virt-install), RHCOS 설치, wait-for, bootstrap 정리, etcd 백업
- 05 Worker1 편입 — RHCOS 설치(bond0), CSR 승인, NNCP(br-svc · br-bk) · NAD, FC LUN 인식
- 06 Operator · MTV 준비 — 미러 카탈로그, NMState · OpenShift Virtualization · MTV, vSphere Provider · NetworkMap · StorageMap
- 07 VM 이관 — 시험 이관, Plan 실행 · 확인, 이관 후 IP 설정(RHEL nmcli · Windows netsh)
- 08 Worker2 전환 — MTV 완료 후 vCenter · DNS VM 정리, LUN 매핑, 편입, Live Migration 시험
- 09 원복 · 장애 대응
- 부록 — 자주 쓰는 명령

## 남은 사항

- 테스트하며 명령 확정: nasbak VLAN 태깅 방식, Ignition HTTP 포트, imageset 범위, StorageClass 구성 방식, etcd 백업 주기 · 보관 기간.
- 내부 HV#03 관리망 4회선 결선 변경 여부 확인.

## 검증

- Chrome 렌더링으로 머리글 · 00~02장 확인.
- 실제 IP 값 없음(자리표시자만 사용).
