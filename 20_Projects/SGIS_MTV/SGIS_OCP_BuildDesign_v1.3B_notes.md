---
type: project
status: draft
created: 2026-10-14
target: SGIS_OCP_BuildDesign_v1.3B.html
---

# 국데처 SGIS OpenShift 구축설계서 v1.3B 릴리스 기록

v1.3([릴리스 기록](SGIS_OCP_BuildDesign_v1.3_notes.md))에서 02장 IP 표기를 간소화(B안)하고 03장 서버별 IP 기입표·08장 백업·운영 설계를 삭제한 버전입니다. 반영본은 [SGIS_OCP_BuildDesign_v1.3B.html](SGIS_OCP_BuildDesign_v1.3B.html)이며, v1.3은 그대로 둡니다.

## 변경 사항

1. **02장 IP 표기 (B안)**: 장비별 IP 박스를 개수 배지로 축약.
   - Bastion(외부·내부): "● IP 2개", Master(외부·내부): "● IP 5개".
   - 망별·용도별 내역 목록(관리망 · nasbak · KVM 호스트 · master-0·1·2 · Bootstrap)은 삭제.
2. **03장 서버별 IP 기입표 삭제**: 대외비 정보(장비별 호스트명·IP 기입 양식)라 설계서에서 제외. 망별 신규 IP 개수 문장(관리망 6 · nasbak 1)만 유지.
3. **08장 백업·운영 설계 삭제**: 백업 방식 표(etcd · VM 데이터 · Linux OS · Windows · Bastion/KVM 호스트)와 운영 제약 3줄 삭제. 목차에서 제외하고 "09. 설계 제약 및 확정 필요 항목"을 08장으로 번호 변경. 02·03장의 Bastion NAS/BK 포설(etcd 백업) 내용은 유지.
4. 버전 태그: "VERSION 1.3B / 내부 구축팀용 초안 · 03~08장 축약 · 02장 IP 표기 간소화 · 백업·운영 장 삭제".

## 검증

- 02장 IP 박스 4곳 치환, 03장 서버별 IP 기입표와 이를 가리키는 링크·앵커 제거 확인. 문서 내 IP 주소는 OCP 기본 Pod·Service 대역(10.128.0.0, 172.30.0.0)만 남음.
- 08장 섹션·목차 링크 제거, 이후 장 번호 08로 정정 확인.
