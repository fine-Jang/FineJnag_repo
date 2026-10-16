---
type: project
status: draft
created: 2026-10-16
target: SGIS_OCP_BuildDesign_v1.9.html → SGIS_OCP_BuildDesign_v1.9t.html
---

# 국데처 SGIS OpenShift 구축설계서 v1.9t 릴리스 기록

v1.9([릴리스 기록](SGIS_OCP_BuildDesign_v1.9_notes.md))에서 03 네트워크 설계의 구성 기준을 삭제한 버전입니다. 반영본은 [SGIS_OCP_BuildDesign_v1.9t.html](SGIS_OCP_BuildDesign_v1.9t.html)이며, v1.9는 그대로 둡니다. 네트워크 장은 전면 개편 예정입니다.

## 변경 사항

1. 버전 태그: "VERSION 1.9t / 기입 · 인쇄용 · 네트워크 구성 기준 삭제".
2. **03 네트워크 설계 — 구성 기준 표 삭제**(bond 매핑 · 기본 게이트웨이 · Worker 브리지 · Bastion 포트 · Master KVM 호스트 · 클러스터 네트워크 · DNS · Bastion 서비스 · NTP · VM NIC 매핑 · VLAN 701 · MTU).
3. 서버별 인터페이스 · IP 기입표, 방화벽 신청은 그대로 유지.

## 검토 후 제외

- install-config 기입표 → Bastion 설치 참조값 기입표로 검토했으나 문서에서 제외.

## 검증

- 기입칸 data-f 92개(v1.9와 같음), 설치 참조값 표·CSS 남은 것 없음.
