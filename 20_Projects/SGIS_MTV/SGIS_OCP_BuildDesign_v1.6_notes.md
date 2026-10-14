---
type: project
status: draft
created: 2026-10-14
target: SGIS_OCP_BuildDesign_v1.6.html
---

# 국데처 SGIS OpenShift 구축설계서 v1.6 릴리스 기록

v1.5([릴리스 기록](SGIS_OCP_BuildDesign_v1.5_notes.md))에 인터페이스·bond·bridge 이름 확정 항목을 더한 버전입니다. 반영본은 [SGIS_OCP_BuildDesign_v1.6.html](SGIS_OCP_BuildDesign_v1.6.html)이며, v1.5는 그대로 둡니다.

## 변경 사항

1. **08장 확정 필요 항목 (구축팀)** 추가:
   - bond·bridge·NAD 이름(현재 안: bond0/1/2, br0·br-svc·br-bk). br-ex는 OVN이 자동 생성하는 이름이라 제외.
   - 서버별 물리 인터페이스명(실사 시 RHCOS live ISO로 확인 · Ignition 생성 전). 설치 시 bond0·고정 IP 설정에 실제 포트 이름이 필요하기 때문.
2. **07장 체크리스트 4단계(Ignition 준비)** 맨 앞에 "서버별 물리 인터페이스명 확인 (RHCOS live ISO · ip link) → NIC 표 기입" 작업 추가(확인 기준: NIC 표 인터페이스 칸 완료). 체크 저장 키를 v1.6용으로 분리.
3. MAC 주소 칸은 넣지 않음.
4. **전체 구성도**: Master KVM 호스트 안 "KVM 브리지 br0 (관리망)" → "브리지 br0 (관리망)".
5. 버전 태그: "VERSION 1.6 / 내부 구축팀 현장 설치용 · 인터페이스·bond·bridge 이름 확정 항목".

## 검증

- 브라우저 렌더링으로 07장 4단계 새 작업, 08장 구축팀 항목 확인.
