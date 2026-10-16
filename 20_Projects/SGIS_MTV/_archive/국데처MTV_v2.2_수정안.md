---
type: project
status: draft
created: 2026-10-12
target: SGIS_MTV_WorkPlan_v2.1.html → SGIS_MTV_WorkPlan_v2.2.html
---

# 국데처MTV 작업계획서 v2.2 수정안

v2.1 이후 현장 실사 정보(VMware→OCP 마이그레이션 설계 페이지, 2026-10-12 갱신)와 사용자 확정 사항을 반영한 수정안이다. 반영본은 `SGIS_MTV_WorkPlan_v2.2.html`이다. v2.1 결정 사항은 [[국데처MTV_v2.1_수정안]]을 따르고 여기에는 바뀐 것만 적는다.

## 1. 실사로 확인된 환경

| 항목 | 값 |
|---|---|
| 소스 | vSphere 8(고객사 표기 VCF 8), 망마다 vCenter → MTV Provider 2개 |
| 기존 HV | CPU 48c, 메모리 1TB, 물리 포트 6(관리 2·서비스 2·nasbak 2) + IPMI + FC HBA |
| VM 배치 | 외부: HV#01에 업무 VM 12 + vCenter, HV#02에 DNS VM·vCLS / 내부: HV#01 vCLS만, HV#02 업무 VM 25 + vCenter, HV#03 DNS VM·vCLS |
| 이관 대상 | 37대(외부 12, 내부 25). vCenter·DNS VM·vCLS 제외 |
| VDDK | 사용 불가 |
| 데이터스토어 | VMFS6, FC LUN, 모든 HV에 연결. 외부 1개(12.4TB 사용), 내부 3개(62.3TB 사용). 여유 거의 없음 |
| 배열 | 장치 모델 SYMMETRIX(VMAX/PowerMax 계열). 세대 확인 필요 |
| VLAN | 관리 태그 없음, 서비스 130, nasbak 701·710(외부·내부 동일). 701은 구형 NFS용, 11월 중 사용 중단 예정 |
| bond | 서비스·nasbak·관리 모두 mode 1(active-backup) |
| VM 조건 | IP 유지 필수(Preserve static IPs), 동시 이관 10대 이하, BIOS 부팅(1대 확인), VMware Tools 혼재 → 미설치 VM은 이관 전 설치 |
| DNS VM | 망별 1대, Windows, 로컬 디스크, HV·vCenter 레코드만 → 이관하지 않음 |
| 설치 | 전체 UPI(Master VM에 BMC 없음), Bootstrap은 Master KVM의 임시 VM |

## 2. 장비 배정 (확정, 2026-10-12)

■ 기존 서버 재구성 · □ 재활용 TNS-2100

| 망 | 역할 | 구분 | 장비 | IP |
|---|---|---|---|---|
| 외부 | Master (KVM, VM 3식) | □ | TNS-2100 | 신규 |
| 외부 | Bastion (+미러·DNS·LB) | □ | TNS-2100 | 신규 |
| 외부 | Worker1 | ■ | HV#02 | 재사용 |
| 외부 | Worker2 (MTV 이후) | ■ | HV#01 | 재사용 |
| 내부 | Master (KVM, VM 3식) | □ | TNS-2100 | 신규 |
| 내부 | Bastion (+미러·DNS·LB) | ■ | HV#01 | 재사용 |
| 내부 | Worker1 | ■ | HV#03 | 재사용 |
| 내부 | Worker2 (MTV 이후) | ■ | HV#02 | 재사용 |

v2.1 대비 변경: 내부 Master HV#03 → TNS-2100, 내부 Bastion TNS-2100 → HV#01, 내부 Worker1 HV#02 → HV#03, 내부 Worker2 HV#01 → HV#02. 수량은 그대로(HV 5대 재구성, TNS-2100 3대 투입·2대 여유).

## 3. 네트워크 구성안

### 노드별 포트

| 서버 | 관리망 bond0 | 서비스망 bond1 | nasbak bond2 | IPMI · FC |
|---|---|---|---|---|
| Worker1·2 (HV 전환) | 2포트, mode 1, 태그 없음, 노드 IP·기본 GW | 2포트, mode 1, trunk 130, IP 없음 → br-svc | 2포트, mode 1, trunk 701·710, IP 없음 → br-bk | 기존 IPMI, HBA 재사용(호스트 등록·마스킹 재확인) |
| Master KVM (TNS-2100) | 2포트, mode 1 → KVM 브리지 br0 (Master VM 3·Bootstrap) | 없음 | 없음 | IPMI 연결 확인, FC 없음 |
| 외부 Bastion (TNS-2100) | 2포트, mode 1 | 없음 | 없음 | IPMI 연결 확인, FC 없음 |
| 내부 Bastion (HV#01) | 2포트, mode 1 | 미사용 | 미사용 | 기존 IPMI, VMFS LUN 매핑 해제 |

- 노드 간 통신과 MTV 이관 트래픽(OCP 노드 → vCenter·ESXi 443·902)은 관리망 bond0 사용.
- 기본 게이트웨이는 관리망에만. 서비스망·nasbak망은 노드 IP 없이 브리지로 VM에만 연결.
- mode 1이라 LACP 불필요. 대기 포트에도 같은 VLAN trunk 허용 필요.

### Bastion 서비스

| 서비스 | 포트 | 대상 |
|---|---|---|
| API LB | 6443 | Bootstrap + Master VM 3 |
| Machine Config Server | 22623 | Bootstrap + Master VM 3 (내부 전용) |
| Ingress LB | 443·80 | Worker (콘솔·인증 Route, 관리망) |
| DNS | 53 | api·api-int·*.apps, 노드, HV·vCenter 레코드 복사 |
| 미러 레지스트리 | 8443 | mirror registry for Red Hat OpenShift(Quay), 상시 운영·백업 |
| HTTP | 설치 시 지정 | Ignition 배포 |

### IP

| 망 | 새 IP 필요 | 기존 IP 재사용 |
|---|---|---|
| 외부 | Master KVM 호스트, Master VM 3, Bootstrap, Bastion | Worker1(HV#02), Worker2(HV#01) |
| 내부 | Master KVM 호스트, Master VM 3, Bootstrap | Bastion(HV#01), Worker1(HV#03), Worker2(HV#02) |

### VM 네트워크 매핑 (MTV NetworkMap)

| 소스 포트그룹 | VLAN | 대상 | 비고 |
|---|---|---|---|
| MGMT | 태그 없음 | ignored | DNS·vCenter 전용, 이관 안 함 |
| 서비스 | 130 | NAD svc-130 → br-svc → bond1 | |
| nasbak 701 | 701 | NAD bk-701 → br-bk → bond2 (조건부) | 11월 중단 완료 시 만들지 않음. 게스트 내부 NFS VM은 별도 계획 |
| nasbak 710 | 710 | NAD bk-710 → br-bk → bond2 | |
| 사용하지 않는 NIC | – | ignored | VM별 게스트 IP 유무로 판단 |

VM 안에서는 VLAN을 설정하지 않고 NAD의 vlan 값이 태깅한다. 브리지는 NNCP로 노드마다 만든다. MAC은 보존되고 IP는 Preserve static IPs로 유지한다.

## 4. 스토리지 매핑안

### StorageMap

| 망 | 소스 | 사용량 | 대상 | 비고 |
|---|---|---|---|---|
| 외부 | VMFS6 FC LUN 1개 | 12.4TB | PowerMax CSI StorageClass (RWX, Block) | |
| 내부 | VMFS6 FC LUN 3개 | 62.3TB | 같은 StorageClass (풀 분리 시 망별) | |
| 공통 | 로컬 (Local DELL Disk) | DNS VM 약 110GB | 매핑 안 함 | HV 전환 전 Storage vMotion |

### 이관 방식

| 방식 | 조건 | 특징 |
|---|---|---|
| ① Storage Copy Offload (1순위) | PowerMax, PowerMax CSI, ESXi SSH(권장)/VIB, 배열 관리 주소·계정·Symmetrix ID·포트 그룹 | 배열 내부 XCOPY, warm 가능 |
| ② Skip VDDK cold (대안) | vSAN 아님(해당) | ESXi 443·902 네트워크 복사, 속도 저하 가능 |
| OVA (예외) | NFS 공유 | 개별 예외 VM만 |

- 한 plan에서 ①·② 혼용 불가. 이관 전 스냅샷 삭제(남으면 소프트웨어 복사로 후퇴).
- 추가 용량: 원본 74.7TB와 대상 볼륨 동시 보유 → 약 74.7TB 이상 + 오버헤드.
- 전송 시간(일정 속도 가정): 100MB/s 외부 1.4일·내부 7.2일 / 400MB/s 8.6시간·1.8일 / 1GB/s 3.4시간·17.3시간.

### 연결 준비

- Worker 전환 HV: HBA 재사용, 배열 호스트 등록·마스킹 재확인. 재설치 전 VMFS LUN 매핑 해제.
- 내부 Bastion(HV#01): LUN 매핑 해제, FC 미사용.
- TNS-2100: FC 미연결, etcd는 내장 SSD/NVMe.

## 5. 설치 순서 변경 (05장)

1. 현황·백업, VMware Tools 미설치 VM 설치, 스냅샷 정리, 배열 모델 확인 (10월)
2. 빈 HV 정리: VM 집약 단계 삭제(이미 모여 있음). DNS VM을 Storage vMotion으로 이동 (외부 HV#02, 내부 HV#03)
3. 비운 HV 초기화 준비: 외부 HV#02, 내부 HV#01·HV#03 — vCenter 호스트 제거, LUN 매핑 해제
4. Bastion 구축: 외부 TNS-2100 / 내부 HV#01
5. Master KVM: 외부·내부 TNS-2100
6. Bootstrap·Master VM 설치
7. Worker1: 외부 HV#02 / 내부 HV#03
8. Virtualization·NMState·NAD·PowerMax CSI
9. MTV 준비·시험 이관(실제 전송 속도 측정)
10. 본 이관 12/1~12/11: 외부망 먼저 → 내부망, 동시 10대 이하
11. 안정화 12/14~12/23
12. Worker2: 외부 HV#01 / 내부 HV#02 (vCenter·DNS VM 종료 후)
13. 완료 12/31

## 6. 위험 추가·변경 (06장)

- Master 구성 지원 범위: KVM은 Red Hat 시험 구성에서 Not Tested, 문서는 머신별 물리 호스트 권고. Red Hat 문의 없이 진행 → 백업·복구 절차 설치 직후 준비. (v2.1의 "Red Hat 지원 가능 확인" 문구는 이 내용으로 대체)
- VDDK 불가: Skip VDDK 속도 저하로 내부망 62.3TB가 12/11을 넘길 수 있음 → Copy Offload 우선, 11월 시험 이관 속도로 회차 재산정.
- 배열 세대·CSI: PowerMax가 아니거나 CSI가 OCP 4.22 미지원이면 Copy Offload 불가.
- VLAN 701 NFS VM, DNS VM 이동, VMware Tools 미설치 VM 항목 추가.

## 7. 실행 전 확정 항목

- 스토리지 엔지니어: 배열 세대·펌웨어, PowerMax CSI의 OCP 4.22 지원, RWX Block·스냅샷, 약 74.7TB 추가 용량, 호스트 등록·마스킹, Copy Offload용 계정·Symmetrix ID·포트 그룹
- VMware 엔지니어: vSphere 정확한 버전(SDDC Manager 여부), 호스트 제거, MTV 권한, ESXi SSH·VIB
- 네트워크 담당: 포트 속도, trunk 허용 VLAN과 대기 포트, 망별 대역·게이트웨이
- 작업 담당·고객사: VLAN 701 사용 VM과 중단 일정, warm 필요 VM·다운타임 창, Tools 미설치 VM, 게스트 OS 버전
- TNS-2100 사양(Master VM 3 + Bootstrap), 관리 포트 2개, 신규 장비 IPMI 연결
- 미러 레지스트리 형태와 PowerMax CSI 이미지 반입, 디스크 용량
