---
type: project
status: draft
created: 2026-10-12
target: 국데처MTV_작업계획서_초안_v0.2.html → v2.1
---

# 국데처MTV 작업계획서 v2.1 수정안

`국데처MTV_작업계획서_초안_v0.2.html` 검토 결과와 2026-10-12 사용자 확정 사항을 정리한 수정안이다. 사용자가 전체 반영을 요청하면 이 목록 기준으로 `국데처MTV_작업계획서_초안_v2.1.html`을 작성한다.

## 1. 사용자 확정 사항 (2026-10-12)

| 항목 | 확정 내용 |
|---|---|
| Master 구성 | 망별 KVM 호스트에 **Master VM 3식**. Red Hat 지원 가능 확인 |
| 내부망 Master 호스트 | **기존 내부 HV#03 재구성** |
| 외부망 Bastion | **재활용 TNS-2100** (v0.2의 "기존 장비 재구성·출처 확인 필요"를 대체) |
| 미러 레지스트리 | **망별 Bastion에 설치** (외부·내부 각 1) |
| MTV 기간 | **1개월로 정정**, 전체 **2026년 12월 말 종료** |
| 원본 보관 방식 | **안 A** — 12월 중순까지 이관 완료, 1~2주 안정화 후 12월 말 Worker2 전환 |
| DB 레거시 | **별도 DB 풀**에 있음. 이관 대상 39식에 포함되지 않음 |

## 2. 장비별 배정표 (확정)

■ 기존 서버 재구성 · □ 재활용 TNS-2100

| 망 | 역할 | 구분 | 장비 | 시점 |
|---|---|---|---|---|
| 외부 | Master (KVM, VM 3식) | □ | TNS-2100 | 초기 구축 |
| 외부 | Bastion (+미러 레지스트리) | □ | TNS-2100 | 초기 구축 |
| 외부 | Worker1 | ■ | HV#02 | 초기 구축 |
| 외부 | Worker2 | ■ | HV#01 | MTV 이후 |
| 내부 | Master (KVM, VM 3식) | ■ | HV#03 | 초기 구축 |
| 내부 | Bastion (+미러 레지스트리) | □ | TNS-2100 | 초기 구축 |
| 내부 | Worker1 | ■ | HV#02 | 초기 구축 |
| 내부 | Worker2 | ■ | HV#01 | MTV 이후 |

수량: 기존 HV 5대 전량 재구성 / TNS-2100 5대 중 3대 투입, 2대 여유분.

## 3. 설치 순서 정정 (v0.2 05장)

v0.2는 3단계 Worker1 구성 → 4단계 Master·Bastion 구축 순서로, UPI 설치 의존관계(Bastion → Master → Worker)와 충돌한다. 망별 아래 순서로 정정한다.

| 단계 | 작업 | 장비 |
|---|---|---|
| 1 | 현황·백업: HV·VM·네트워크·FC LUN 현황 기록, VM 백업 | 기존 HV 전체 |
| 2 | VM을 HV#01로 집약, VMware 원본 유지 | HV#01 |
| 3 | 비운 HV 초기화 준비: EMC에서 VMFS LUN 매핑 해제, 설정 백업 | 외부 HV#02 / 내부 HV#02·#03 |
| 4 | Bastion 구축: RHEL 9.8, 미러 레지스트리(이미지 반입), DNS, LB, Ignition 생성 | Bastion (TNS-2100) |
| 5 | Master KVM 호스트 구성: RHEL 9.8 + KVM, 네트워크 브리지 | 외부 TNS-2100 / 내부 HV#03 |
| 6 | Bootstrap VM + Master VM 3식 설치 → Bootstrap 완료 후 Bootstrap VM 삭제·LB 제외 | Master KVM 호스트 |
| 7 | Worker1 설치·편입 (RHCOS, 설치 디스크 by-id 지정, CSR 승인) | HV#02 |
| 8 | 클러스터 기반 구성: OpenShift Virtualization, NMState 네트워크, EMC CSI·StorageClass | 클러스터 |
| 9 | MTV 설치·준비: Provider·VDDK·NetworkMap·StorageMap → 시험 이관 | 클러스터 |
| 10 | 회차별 본 이관·검증 | HV#01 → Worker1 |
| 11 | 전환 판단: 원본 보관·원복 기준 충족 확인 | – |
| 12 | HV#01 → Worker2 편입 (LUN 매핑 해제 → RHCOS → CSR 승인) | HV#01 |
| 13 | 최종 검증·결과서 | – |

UPI 절차 표도 동일하게 수정: Bootstrap 위치는 "Master KVM 호스트의 임시 VM, 설치 완료 후 삭제".

## 4. 일정 (07장)

| 차수 | 시기 | 작업 |
|---|---|---|
| 1차 사전작업 | 10월 | 행정작업, 장비 재배치, 전기 포설, 현황 조사·백업, 이미지 반입 준비 |
| 2차 재구성 | 11월 | VM 집약 → HV 초기화 → Bastion → Master KVM·VM → Worker1 → Virtualization·CSI·MTV 구성, 시험 이관 |
| 3차 MTV | 12월 | 본 이관 → 안정화 → Worker2 편입 → 최종 검증 (**12월 말 종료**) |

12월 상세 (안 A, 작업일은 확정 시 조정):

| 기간 | 작업 | 다음 단계 진행 조건 |
|---|---|---|
| 12/1 ~ 12/11 | 회차별 본 이관 (외부 13식, 내부 26식) | 회차별 이관 완료 점검표 통과 |
| 12/14 ~ 12/23 | 안정화: 업무 모니터링, 백업 정상 확인. 원본 VM 전원 종료 보관 | 이관 완료 후 최소 1주 무장애, 원복 불필요 판단 |
| 12/24 ~ 12/30 | HV#01 → Worker2 편입 | 노드·네트워크·CSI 정상 확인 |
| 12/31 | 최종 검증·결과서 | 완료 |

- Worker2 전환 판단 기준: 이관 완료 후 최소 1주 안정화 + 원복 요청 없음 + 백업 복구 시험 통과 + 업무 담당 확인.
- 예비안: 12/11까지 이관 미완료 시 안정화 기간을 줄이지 않고 Worker2 전환을 1월로 이연.
- 원본 LUN·데이터스토어 회수는 Worker2 전환과 별도로 판단한다.
- 12/25 휴일 및 연말로 실제 작업 가능일이 줄어드는 점 반영.

## 5. 구성·네트워크 반영 사항

- **구성도(02장)·장비표(03장):** 2장 배정표 기준으로 수정. Master는 "KVM 호스트 · Master VM 3식"으로 표기.
- **신규 IP(04장) 재산정:**
  - 외부망: Master KVM 호스트, Master VM 3, Bootstrap(임시), Bastion, API·Ingress VIP
  - 내부망: Master KVM 호스트(HV#03 기존 IP 재사용), Master VM 3, Bootstrap(임시), Bastion, API·Ingress VIP
- **Bastion:** 설치 후에도 노드가 미러 레지스트리에서 이미지를 받으므로 상시 운영 서버로 관리(백업 대상). 디스크는 미러 용량(수백 GB~1TB 이상) 기준으로 산정. 이미지 반입은 망별로 수행.
- **DB 레거시:** 별도 DB 풀이므로 재구성·이관 대상에서 제외. 이관 VM → DB 풀 접속 확인은 이관 완료 점검표에 유지.

## 6. 위험 및 원복 항목 추가 (06장)

- Master VM 3식이 KVM 호스트 1대에 있어 **물리 단일 장애점**. 호스트 장애 시 API 중단(운영 VM은 Worker에서 계속 동작).
- etcd 디스크: SSD/NVMe 사용, fsync 지연 10ms 이하 확인. etcd 정기 백업을 KVM 호스트 외부에 보관하고 복구 절차 작성.
- Worker1 단독 운영 기간: Live Migration 불가, 노드 재부팅 시 전체 VM 중단 → OCP 업데이트·MachineConfig 변경 동결.
- 노드 재설치 전 EMC Host Group에서 VMFS LUN 매핑 해제, 설치 디스크는 `/dev/disk/by-id`로 지정, RHCOS 멀티패스 설정(MachineConfig) 포함.

## 7. 검증·확인 항목 추가

| 항목 | 내용 |
|---|---|
| 내부 HV#03 사양 | Master VM 3식 + Bootstrap 수용 가능 여부 (약 28~32 vCPU, 112~128GB, SSD) |
| MTV 버전 | OCP 4.22 정합 버전 MTV 2.12 기준으로 참고 문서 변경 (v0.2 각주는 2.9) |
| EMC CSI | EMC 모델 확인(VNX 등 구형은 CSI 미지원). Dell CSM의 OCP 4.22 지원 여부(카탈로그상 v1.12.x는 4.18~4.21). 미지원 시 Local Storage Operator 대안 |
| Copy Offload | 동일 EMC 원본·대상이므로 MTV 스토리지 복사 오프로드 적용 가능 여부 — 이관 기간 단축 요인 |
| vCenter | 유무 및 39식 포함 여부 → VM 집약(vMotion)·Warm 이관·Provider 구성에 영향. VDDK 이미지 미러 반입 |
| 구독 | KVM 호스트·Bastion RHEL 구독 및 OVE 구독 범위 |

## 추후 반영 예정 (사용자 요청)

- VMware VM 이관 방식에 VDDK 사용 방안을 추가합니다. VDDK 이미지의 확보·폐쇄망 반입·레지스트리 등록 절차와 적용 조건을 기록합니다.
- VDDK 사용 이관과 미사용 콜드 이관의 소요 시간·운영 영향·제약을 시험 이관으로 비교한 뒤 최종 방식을 확정합니다. vSAN 기반 VM 및 웜 이관 가능 여부도 함께 확인합니다.
- 위 내용은 이번 V2.1 작업계획서에는 아직 반영하지 않고, 사용자가 일괄 수정 요청 시 반영합니다.

- 재활용 서버를 Master 용도로 투입할 경우, 기존 MGMT 연결에 더해 NAS/BK 망의 물리 포설을 계획에 포함합니다. NAS/BK 연결은 이중화된 NIC 포트를 사용해 Bond 구성하는 방안을 검토하며, 장비 포트 수·스위치 이중 경로·스위치 포트채널 지원·Bond 모드와 VLAN 설계를 사전 확인합니다.
- etcd 백업은 OpenShift의 클러스터 백업 절차로 생성한 뒤 NAS/BK 망을 통해 통합 백업 스토리지로 주기적으로 전송하는 방안을 검토합니다. 백업 주기·보존 기간·전송 및 접근 통제·실패 모니터링을 정하고, 실제 복구 시험으로 복원 가능성을 확인합니다. 백업 파일은 클러스터 장애 시에도 접근 가능한 위치에 보관하고, etcd 백업이 VM·업무 데이터 백업을 대체하지 않도록 범위를 구분합니다.
- 위 포설 및 etcd 백업 내용도 이번 V2.1 작업계획서에는 아직 반영하지 않고, 사용자가 일괄 수정 요청 시 함께 반영합니다.

## 참고

- [MTV 2.12 / OCP 4.22 (Red Hat 블로그)](https://redhat.com/en/blog/storage-processing-accelerates-vm-migrations-migration-toolkit-virtualization-212)
- [Dell CSM Operator – Red Hat 카탈로그](https://catalog.redhat.com/en/software/container-stacks/detail/639c131cd113cc28c0c2f2d5)
- [MTV Copy Offload PowerStore 검증 이슈](https://issues.redhat.com/browse/MTV-4263)
