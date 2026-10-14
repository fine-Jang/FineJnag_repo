---
type: project
status: draft
created: 2026-10-14
target: SGIS_OCP_BuildDesign_v1.5.html
---

# 국데처 SGIS OpenShift 구축설계서 v1.5 릴리스 기록

v1.4([릴리스 기록](SGIS_OCP_BuildDesign_v1.4_notes.md))에서 설명 글을 줄이고 그림 위주로 바꾼 버전입니다. 반영본은 [SGIS_OCP_BuildDesign_v1.5.html](SGIS_OCP_BuildDesign_v1.5.html)이며, v1.4는 그대로 둡니다.

## 변경 사항

1. **설명 글 삭제**: 01 소개 문단, 02 구성도 설명·재구성 그림 설명·TNS-2100 여유분 문단, 03 NetworkMap·IP 기입표 설명, 04 용량 산식 설명, 05~07 안내 문장, 꼬리말 문서 성격 문장 삭제. 01 "설계 범위" 표 삭제. 남긴 짧은 캡션: 이관 제외 VM, NIC 표 기입 안내.
2. **01 개요 3분할**: 숫자 카드 4개 아래에
   - ① 현재 VMware 구성: 망별 HV 박스 그림(장비 · 올라가 있는 VM · 데이터스토어).
   - ② 이관 대상 VM: VM 약식 표 + 제외 VM 한 줄.
   - ③ 구축할 OpenShift 인프라: 망별 노드 그림(Bastion 서비스 · Master KVM의 master VM 3 + bootstrap · Worker1 · Worker2 MTV 완료 후) + 적용 버전 표.
3. **스토리지 구성 전부 삭제**: 적용 버전 Dell CSI 행, 05장 OpenShift 스토리지 구성 표, MachineConfig multipathd, 06장 그림 4 스토리지 매핑, 체크리스트 CSI 작업, 08장 스토리지 담당 행, 전체 구성도 스토리지 박스의 CSI·PVC 문구, 꼬리말 Dell CSM 카탈로그 링크. 현행 VMware 데이터스토어 정보와 HV 재구성 시 VMFS LUN 매핑 해제 단계는 유지.
4. **장비별 IP 기입표 망별 분리**: 외부망·내부망 표를 따로 두고 표마다 머리줄(역할 · 장비 · 호스트명 · 관리망 IP · nasbak IP · 비고). 망 공통 값(관리망 대역/GW · nasbak 대역/VLAN · NTP 서버 · base domain)은 각 표 아래 2행.
5. **서버별 NIC 인터페이스 표(신규, 03장)**: 망별로 서버 · 장비 · 인터페이스 1·2(빈칸, 실사 후 기입) · bond · bridge · 망·용도.
   - Bastion: bond0(관리) · bond2(nasbak) · IPMI.
   - Master KVM 호스트: bond0 → br0 · IPMI. master VM: VM NIC → br0.
   - Worker1·2: bond0 → br-ex(OVN 자동 생성) · bond1 → br-svc · bond2 → br-bk · IPMI.
6. **01 숫자 카드**: "망별 노드 3 + 2" → "클러스터별 구성 서버 4식 (Bastion 1 · Master KVM 1 · Worker 2)".
7. 체크리스트 체크 저장 키를 v1.5용으로 분리. 버전 태그: "VERSION 1.5 / 내부 구축팀 현장 설치용 · 그림 위주 · 스토리지 구성 삭제 · NIC 인터페이스 표".

## 검증

- 구성도 SVG 글자 넘침 검사 결과 넘침 없음.
- 브라우저 렌더링으로 01장 그림 3개 영역, 03장 NIC 표·IP 기입표 확인.
- 본문에 CSI · StorageClass · PowerMax · multipath · 설명 문단 클래스가 남지 않음을 스크립트로 확인.
