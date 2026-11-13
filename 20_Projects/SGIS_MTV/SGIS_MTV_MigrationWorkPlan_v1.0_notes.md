---
type: project
status: draft
created: 2026-11-13
target: SGIS_MTV_MigrationWorkPlan_v1.0.html
---

# 국데처 SGIS VMware → OpenShift 전환 및 MTV 이관 작업계획서 v1.0 릴리스 기록

실제 작업 전에 제출하는 작업계획서의 첫 버전입니다. 반영본은 [SGIS_MTV_MigrationWorkPlan_v1.0.html](SGIS_MTV_MigrationWorkPlan_v1.0.html)입니다. 근거는 `2026-10-10-vmware-to-ocp-migration-work-guide.html`(2026-11-13 갱신본)이고, 디자인·어투·서식은 [작업계획서 v2.9](SGIS_MTV_WorkPlan_v2.9_notes.md)를 따랐습니다.

## 결정

- 원본 가이드의 작업 전 준비 절차를 제거함.
  - 0장(작업 전에 정해져 있어야 하는 것)
  - 1장(반입 파일 만들기: 외부 호스트 준비, 바이너리, RHCOS ISO, 이미지 미러링, 반입물 묶기, 반입 파일 목록)
- 문서는 원본의 「2. 순서 개요」를 바탕으로 한 「01. 작업 개요」부터 시작함.
- 원본 1-7(반입 뒤 Bastion에서 d2m)과 1-8(VDDK 이미지)은 현장 Bastion에서 하는 작업이라 02-7·02-8로 옮김. 0-1 ocp.env는 02-1로 옮김.
- 내부 메모를 정리함: 💡·❓·📖 표식, 오너·작업 담당 발언과 날짜, 구축 실습 기록, 설계 페이지 번호 참조. 남은 미결 사항은 09장 「확인 필요 사항」 표로 모음.
- 어투: v2.9처럼 합니다체. 표 위주로 순서·작업·완료 기준을 정리하고, 정지 조건은 빨간 박스, 완료 기준은 초록 박스로 표시.
- 명령 블록은 원본의 들여쓰기를 그대로 살림(YAML 포함). worker-net.sh의 bond 주석은 결정 내용만 남김.

## 구성

- 01 작업 개요: 숫자 카드, 전체 작업 순서, 작업 기준, 되돌릴 수 없는 단계, 역할 분담
- 02 Bastion 구축: 환경변수, CLI·방화벽, 저장소, HTTP, DNS, Quay, 미러 적재, VDDK, HAProxy
- 03 Master KVM·클러스터 설치: br0·VM, install-config, manifest·chrony, Ignition·스크립트, bootstrap·master, CSR, 미러 리소스
- 04 HV 정리·Worker1 전환: HV 비우기, 전환 전 확인, worker.ign 갱신, bond·RHCOS, 편입·설치 완료, 단독 기간 기준
- 05 대상 클러스터 구성: 기본 소스 차단, Virtualization, MTV, NMState, 브리지 NNCP, NAD, StorageClass, OSUS
- 06 VM 이관: 이관 전 점검, MTV 절차, 이관 후 확인
- 07 Worker2 전환·etcd 백업: 전환 전 확인, 전환, Live Migration, etcd 백업
- 08 내부망 적용
- 09 확인 필요 사항

## 추가·보완

- 05-7에 RWX 테스트 PVC 예시를 추가함(원본에는 YAML이 없었음).
- 02-9에 HAProxy용 방화벽 허용과 setsebool을 명령으로 넣음. 앱 인그레스 worker1 줄은 주석으로 두고 04-5에서 활성화하도록 함.
- 07-2에 Ingress 복제본을 2로 되돌리는 명령을 넣음.

## 검증

- 출력 HTML에 💡·❓·📖·오너·실습·작업 담당 문구가 남지 않음을 스크립트로 확인함.
- 명령 블록 안에 이스케이프되지 않은 `<`가 없음을 확인함.
- Chrome 렌더링으로 머리글·01장, 04장, 05장을 확인함.
