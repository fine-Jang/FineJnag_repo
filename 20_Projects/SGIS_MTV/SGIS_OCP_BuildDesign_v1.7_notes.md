---
type: project
status: draft
created: 2026-10-15
target: SGIS_OCP_BuildDesign_v1.6s.html → SGIS_OCP_BuildDesign_v1.7.html
---

# 국데처 SGIS OpenShift 구축설계서 v1.7 릴리스 기록

v1.6s([릴리스 기록](SGIS_OCP_BuildDesign_v1.6s_notes.md))에서 기존 VMware DNS VM 처리 방침을 바꾼 버전입니다. 반영본은 [SGIS_OCP_BuildDesign_v1.7.html](SGIS_OCP_BuildDesign_v1.7.html)이며, v1.6s는 그대로 둡니다. 기입 칸 입력·인쇄 기능은 v1.6s와 같습니다.

## 결정 (2026-10-15)

- 기존 DNS VM은 vCenter·ESXi 호스트 관리용 이름 해석을 담당하므로 Bastion으로 레코드를 이관하지 않음.
- 전환 작업 전 DNS VM을 MTV 원본 유지 HV로 이동: 외부 HV#02 → HV#01, 내부 HV#03 → HV#02.
- RHOCP DNS는 Bastion에 구성. OCP 노드(MTV·VDDK)가 vCenter·원본 ESXi 이름을 조회할 수 있도록 Bastion에 vCenter·원본 ESXi A 레코드를 둠.
- DNS VM은 MTV 완료 후 vCenter 정리 시(보관·원복 기준 충족 후, Worker2 전환 단계) 삭제.

## 변경 사항

1. 버전 태그: "VERSION 1.7 / 기입 · 인쇄용 · DNS VM 처리 변경".
2. **01 ② 이관 대상 VM**: 제외 문구에 DNS VM 용도(vCenter·ESXi 관리용)와 처리(원본 HV로 이동, MTV 완료 후 삭제) 추가.
3. **02 그림 1**: 소스 VMware 상자 "DNS VM(원본 HV로 이동)·vCLS는 이관 안 함".
4. **02 그림 2**:
   - 외부 Worker1: "DNS VM → HV#01 이동 → 호스트 제거·LUN 매핑 해제 후 편입". 내부 Master: "DNS VM → HV#02 이동 → …".
   - 원본 HV 상자: 외부 HV#01 "DNS VM(HV#02에서 이동)", 내부 HV#02 "DNS VM(HV#03에서 이동)".
   - Worker2 상자: "DNS VM은 vCenter 정리 시 삭제".
   - 단계 카드: ① "DNS VM 레코드 이관" → "vCenter·ESXi 조회 레코드 등록", ②/③ "DNS VM 종료" → "DNS VM → 원본 HV 이동", ⑤에 "vCenter·DNS VM 정리" 추가.
5. **03 구성 기준 DNS (Bastion)**: 레코드 이관 삭제 → OCP 레코드 + vCenter·원본 ESXi A 레코드(MTV 접속용), VMware 관리용 이름 해석은 기존 DNS VM이 계속 담당.
6. **07 체크리스트**:
   - 1단계 DNS 항목에 vCenter·원본 ESXi A 레코드와 조회 확인 추가.
   - 2단계 "기존 DNS 이관" → "DNS VM 이동": 원본 HV로 이동(vMotion) / 이동 후 vCenter·ESXi 이름 해석 확인.
   - 9단계 Worker2 전환에 "DNS VM 삭제 (vCenter 정리와 함께 · 보관·원복 기준 충족 후)" 추가(체크 항목 e41/i41).
7. **08 요청 및 협의 사항** (기존 "확정 필요 항목"):
   - 이름 변경: 장 제목 "08. 설계 제약 및 요청·협의 사항", 소제목 "요청 및 협의 사항".
   - 표를 협의 항목 1건당 1행으로 분리(담당 · No. · 협의 항목 · 세부 내용). 최종 14건: 구축팀 7 · 네트워크 담당 4 · VMware 엔지니어 3.
   - 구축팀: Ignition HTTP 포트 삭제. "서버별 물리 인터페이스명" → "인터페이스명 확인"(이기종 장비 TR2210 H4 · TNS-2100 인터페이스명 통일, RHCOS live ISO로 확인 · Ignition 생성 전).
   - 네트워크 담당: "신규 IP" → "추가 IP 할당" 상세(망별 7개 = 관리망 6: Bastion 1 · Master KVM 호스트 1 · master-0/1/2 VM 3 · bootstrap VM 1(bootstrap 구성 완료 후 반납), nasbak 1: Bastion, 내부 HV#03 기존 IP 재사용 시 1개 감소). 망별 대역·게이트웨이, 내부 HV#03 호스트 IP, MTV 접속 경로, 스위치 포트, MTU, TNS-2100 NIC 삭제.
   - VMware 엔지니어: vSphere 버전 · 호스트 제거 방법 · VDDK 패키지 삭제. DNS VM 이동 방식·일정, VMware Tools 미설치 VM 설치 협의(설치 방법·일정, 이관 전 설치) 추가.
   - 작업 담당·고객사 항목 전부 삭제(VLAN 701 사용 VM, VMware Tools 미설치 VM 목록, 장비 로컬 디스크 구성).
   - 03 장비별 IP 기입표 bootstrap 비고: "신규 · 설치 후 반납" → "신규 · bootstrap 구성 완료 후 반납"(외부·내부).
8. 꼬리말 설계 근거에 2026-10-15 DNS VM 처리 변경 추가.
9. **회사 로고**: 표지(머리글) 오른쪽 위에 AONSOFT 로고 추가. 이미지는 HTML에 내장(별도 파일 불필요), 모바일 폭에서는 제목 위에 배치.

## 검증

- 본문에 "레코드 이관", "DNS VM 종료", "Bastion DNS 전환" 문구가 남지 않음을 스크립트로 확인.
- 브라우저 렌더링으로 그림 1 소스 VMware 상자, 그림 2 외부망 재구성·내부망 단계 카드 확인.

## 남은 사항

- 고객 제출용 작업계획서 v2.9 · v2.9pt에는 이전 방침(레코드 이관 → DNS VM 종료)이 남아 있음 — 별도 반영 필요.
