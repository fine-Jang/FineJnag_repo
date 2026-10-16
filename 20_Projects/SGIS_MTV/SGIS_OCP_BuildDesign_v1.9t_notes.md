---
type: project
status: draft
created: 2026-10-16
target: SGIS_OCP_BuildDesign_v1.9.html → SGIS_OCP_BuildDesign_v1.9t.html
---

# 국데처 SGIS OpenShift 구축설계서 v1.9t 릴리스 기록

v1.9([릴리스 기록](SGIS_OCP_BuildDesign_v1.9_notes.md))에서 03 네트워크 설계의 구성 기준을 삭제한 버전입니다. 반영본은 [SGIS_OCP_BuildDesign_v1.9t.html](SGIS_OCP_BuildDesign_v1.9t.html)이며, v1.9는 그대로 둡니다. 네트워크 장은 전면 개편 예정입니다.

## 변경 사항

1. 버전 태그: "VERSION 1.9t / 기입 · 인쇄용 · 네트워크 구성 기준 삭제 · Master KVM 관리망 4회선".
2. **03 네트워크 설계 — 구성 기준 표 삭제**(bond 매핑 · 기본 게이트웨이 · Worker 브리지 · Bastion 포트 · Master KVM 호스트 · 클러스터 네트워크 · DNS · Bastion 서비스 · NTP · VM NIC 매핑 · VLAN 701 · MTU).
3. 서버별 인터페이스 · IP 기입표, 방화벽 신청은 그대로 유지.
4. **Master KVM 호스트 관리망 4회선**(외부·내부 공통, 2026-10-16, 버전 유지 반영):
   - 2회선 bond0 = 호스트 원격접속(관리망 IP 1개 신규), 2회선 bond1 → br0 브리지(IP 설정 안 함, Master VM·bootstrap 연결).
   - 신규 IP 망별 6개 → 7개(관리망 6 · nasbak 1). 기입표 제목 · 그림 2 Master IP 배지(4개 → 5개) · 내부 Master 설명 수정.
   - 기입표 Master KVM 호스트 행: bond0(인터페이스 1·2 · IP 기입, 비고 호스트 원격접속) / bond1(인터페이스 1·2, IP 없음, br0 · Master VM 연결) / IPMI. 새 기입칸 f345~f350.
   - 그림 1 Master KVM 호스트: "브리지 br0 ← bond1 (IP 없음)", "관리 ×4: bond0 호스트 IP · bond1 br0", 아래 설명 문구.
   - 체크리스트 5단계: "bond0 호스트 IP · bond1 위 br0(IP 없음)".

5. **01 개요 정리**(2026-10-16, 버전 유지 반영):
   - 숫자 카드 4개(이관 대상 VM ~ 원본 데이터 사용량), "망별 구축 인프라" 표, "① 현재 VMware 구성" 삭제.
   - 그 자리에 "이관 VM 정보" 그림 추가(근거: 2026-10-10 VMware→OCP 마이그레이션 설계 페이지의 이관 VM 정보). 카드 3개를 막대로 표시.
     - VM 수 35대(vCenter · DNS VM 제외): 외부망 11대(RHEL 8 · Windows 3) · 내부망 24대(RHEL 22 · Windows 2), RHEL 8.9 30대 · Windows Server 2022 5대.
     - 메모리 VM 합계 1,124GB: 외부망 364GB · 내부망 760GB를 HV(기존 ESXi 서버) 1대 최대 1TB 대비 36% · 74%로 표시.
     - 데이터스토어 사용량 74.7TB(대략적인 용량): 외부망 12.4TB(17%) · 내부망 62.3TB(83%).
   - 소제목 번호 당김: ① 이관 대상 VM · ② 구축할 OpenShift 인프라.

## 검토 후 제외

- install-config 기입표 → Bastion 설치 참조값 기입표로 검토했으나 문서에서 제외.

## 검증

- 기입칸 data-f 98개 중복 없음, 설치 참조값 표·CSS 남은 것 없음.
- Chrome 렌더링으로 그림 1·2, 기입표 Master KVM 행, 개요 이관 VM 정보 그림 확인.
