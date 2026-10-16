---
type: project
status: draft
created: 2026-10-14
target: SGIS_OCP_BuildDesign_v1.1.html
---

# 국데처 SGIS OpenShift 구축설계서 v1.1 릴리스 기록

v1.0 이후 02장 구성도를 개편하고 장 순서를 조정한 버전입니다. 반영본은 [SGIS_OCP_BuildDesign_v1.1.html](SGIS_OCP_BuildDesign_v1.1.html)이며, v1.0([릴리스 기록](SGIS_OCP_BuildDesign_v1.0_notes.md))은 그대로 둡니다.

## 변경 사항

1. **02장 구성도 개편**: SVG 곡선 화살표 구성도를 장비 1대당 1행(번호 · AS-IS · 전환 표시 · TO-BE) 방식으로 교체.
   - 전환 표시: `+ 신규`(재활용 TNS-2100), `→ 재구성`, `→ 안정화 후 전환`.
   - 재활용 TNS-2100은 AS-IS 칸을 "— (미사용)"으로 비움.
   - MTV 이관은 화살표 대신 Worker1 칸의 초록 칩(④ MTV 이관 수신)과 원본 HV 칸의 메모로 표시.
   - 행 번호는 망별 작업 카드 ①~⑤와 일치. 작업 카드 ①에 "2차(11월) 최초 구축" 추가.
2. **장비별 역할 배정 표 삭제**: 02장 행 구성으로 대체. 재활용 장비 여유분·vCLS·vCenter 설명 문단은 유지.
3. **장 순서 조정**: 03 네트워크 ↔ 04 하드웨어·용량. 목차, 06장 표의 장 참조(03장 클러스터 네트워크 파라미터, 04장 사양 합계)를 새 번호로 수정.

## 검토 후 보완 (2026-10-14)

- 03장 본문의 옛 참조 "02장 장비 재구성 구성도"를 "02장 망별 장비 재구성(행별 AS-IS → TO-BE)"으로 수정.
- Master 칸에 KVM 하이퍼바이저 영역(점선)과 master-0·1·2 VM 마크, Bootstrap 임시 VM 표기 복원.
- 내부망 Master(기존 HV#03 재구성)를 신규 장비 스타일(파란 점선)에서 기존 HV 재구성 스타일로 변경하고 전환 조건(Bastion DNS 전환·DNS VM 종료 → 호스트 제거·LUN 매핑 해제 후 재구성) 추가.
- 역할 배정 표 삭제로 빠진 정보 복원: Worker1·Worker2 "기존 IP 재사용", Worker1 편입 조건(호스트 제거·LUN 매핑 해제 후), Worker2 전환 조건(MTV 이관·안정화 완료 후).
- 작성일 2026.10.14로 갱신.

## 02장 구성도 추가 수정 (2026-10-14)

1. 망별 재구성 행 위에 AS-IS(현재 VMware) / TO-BE(OpenShift) 열 머리 추가.
2. TO-BE 재활용 장비(Bastion, 외부망 Master)에 AS-IS와 같은 형식으로 사양 표기: TNS-2100 · 36코어 · 576GB.
3. Master 칸의 KVM 영역을 "KVM 하이퍼바이저 (RHEL 9.8) 위 Master 노드 VM × 3"으로 바꾸고, master-0·1·2를 VM 마크·이름·역할(Control Plane · etcd)이 있는 큰 칸 3개로 표시.
4. 전환 표기 "안정화 후 전환"을 "MTV 완료 후 전환"으로 변경(범례·설명·화살표 라벨·Worker2 칸).

## etcd 백업 경로 변경 — Bastion NAS/BK 신규 포설 (2026-10-14)

- etcd 백업을 Master KVM 호스트가 아닌 **Bastion**이 수행: Master VM에서 `cluster-backup.sh` 실행 → Bastion 수집(SSH 22, 관리망) → Bastion NAS/BK 2포트(nasbak망) → 통합 백업스토리지.
- 양 망 Bastion(재활용 TNS-2100)에 NAS/BK 2포트 신규 포설·bond2 구성, nasbak망 호스트 IP 필요(IP·VLAN TBD).
- 외부망 Master의 NAS/BK 2포트 추가 포설은 삭제. Master KVM 호스트는 양 망 모두 관리망만 사용.
- 장 배정은 변경 없음(내부망 HV#03 Master 유지). 내부망 etcd 백업 보관 위치 TBD 해소.
- 반영 위치: 01 설치 방식, 02 작업 카드 ①, 03 전체 구성도·설명·포트 표·Bastion 서비스(etcd 백업 수집)·방화벽(Bastion → 통합 백업스토리지), 06 Master KVM 호스트 구성, 08 백업 표(외부·내부 통합), 09 확정 항목(etcd 백업 주기·보관 기간, Bastion NAS/BK 포설·nasbak IP·VLAN).

## 검증

- 브라우저 렌더링으로 02장 행 배치, KVM·VM 마크, 작업 카드 확인.
