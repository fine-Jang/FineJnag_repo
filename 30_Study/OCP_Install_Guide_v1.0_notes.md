---
type: study
status: release
created: 2026-11-15
target: OCP_Install_Guide_v0.3.html → OCP_Install_Guide_v1.0.html
---

# OCP 폐쇄망 설치 가이드 v1.0 릴리스 기록

aon-kvm 실습(2026-11-14~15) 실제 수행 기록 기반 OCP 4.22.22 설치 · 설치 후 설정 · MTV 이관 가이드. 반영본 [OCP_Install_Guide_v1.0.html](OCP_Install_Guide_v1.0.html). v0.3은 그대로 유지.

## 결정

- 대상 4.22.22(eus-4.22), 도메인 `ocp.jhw.local`, 관리망 10.182.10.0/24(Bastion .10 · bootstrap .11 · master .12–.14 · worker .15–.16 · TrueNAS .20).
- 값 · 명령 · 결과 예시는 Bastion · KVM · TrueNAS 실제 설정과 명령 출력에서 수집. 결과 예시는 초록 박스로 구분.
- CSI 스토리지(TrueNAS 24.10 + democratic-csi iSCSI 동적 할당)는 별첨 A로 분리. 운영 Dell EMC PowerMax FC + Dell CSI와 대응표 포함.
- 노드 설치 스크립트 n.sh는 별첨 B, 실습 중 발생 문제는 부록 C로 정리.
- 문체: 명사형 종결(합니다체 없음).
- 비밀값(Quay 암호 · pull secret · kubeadmin 암호 · TrueNAS API 키 · vCenter 암호)은 자리표시자. KVM · Bastion 접속 암호 미포함.

## v0.3 대비 주요 변경

1. 4.20.16 → 4.22.22, butane `version: 4.22.0`, RHCOS 9.8.20261026-0.
2. 반입 방식: NAS 마운트 → Bastion `/data/4.22.22_Bundle` 번들(disk → mirror).
3. 클러스터 pull secret은 내부 Quay 계정만(jq 추출).
4. 노드 설치: nmcli 수동 → n.sh(bond0 active-backup · 사전 점검 · `--copy-network`).
5. 07장: 미러 리소스 적용 + OLM v1 기본 ClusterCatalog 비활성 + NMState · OpenShift Virtualization · MTV 설치 · 인스턴스 생성.
6. 08장: worker NIC 6개(관리 · SVC · NAS 각 2) 기준 NNCP bond1→br-svc · bond2→br-nas, NAD(default · VLAN 없음), 전후 비교 스크립트.
7. 09장: vCenter FQDN DNS zone, OpenVDDK VDDK 이미지(랩 전용 경고), Provider · Plan · Cold 이관 결과.

## 실습 중 확인된 주의 사항

- TrueNAS 24.10: 마지막 target 삭제 시 initiator group 자동 정리 → 고정용 빈 target(`keep-ig2-do-not-delete`) 필요.
- 셸 전체 `umask 077` 금지 → VDDK 이미지 lib64 700 → VDDKInvalid. umask는 괄호 서브셸 안에서만.
- VDDK 이미지 수정 시 새 태그 사용(노드 캐시 이미지 재사용 방지).
- 관리망 libvirt NAT로 노드 · Bastion 외부 접근 가능 상태(완전 폐쇄망 아님).

## 검증

- 합니다체 · 비밀값 문자열 없음을 검색으로 확인, section · details · pre · table 태그 짝 확인.
- Chrome headless 렌더링으로 머리글 · 00장 확인.
