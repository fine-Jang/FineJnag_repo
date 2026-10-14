---
type: project
status: draft
created: 2026-10-14
target: SGIS_OCP_BuildDesign_v1.4.html
---

# 국데처 SGIS OpenShift 구축설계서 v1.4 릴리스 기록

v1.3B([릴리스 기록](SGIS_OCP_BuildDesign_v1.3B_notes.md))를 **전산실 현장에서 보면서 설치를 진행하는 문서**로 바꾼 버전입니다. 반영본은 [SGIS_OCP_BuildDesign_v1.4.html](SGIS_OCP_BuildDesign_v1.4.html)이며, v1.3B는 그대로 둡니다.

## 장 구성

01 개요 · 02 아키텍처 · 03 네트워크 · 04 하드웨어·용량 · 05 클러스터 설치 · 06 MTV · **07 설치 체크리스트(신규)** · 08 제약·확정 항목. 스토리지 장은 삭제.

## 변경 사항

1. **01 개요 — 현행 VMware 환경 추가**: 망별 HV 5대(장비 · 현재 VM · 전환 후) 표와 이관 대상 VM 약식 표(07장에서 이동). 문서 성격 문장을 "현장 설치 문서"로 변경.
2. **02 아키텍처 — 그림 순서**: 그림 1 전체 구성도(TO-BE, 03장에서 이동) → 그림 2 망별 장비 재구성(AS-IS → TO-BE). 이후 그림 번호 3(VM 네트워크 매핑) · 4(스토리지 매핑).
3. **스토리지 작업 영역 삭제**: 05 스토리지 설계 장 삭제. OCP에서 하는 항목(CSI 드라이버 · StorageClass · VolumeSnapshotClass)만 05 클러스터 설치의 "OpenShift 스토리지 구성"으로 이동. 호스트 마스킹 · 추가 용량 · 스토리지 모델 확인 등 삭제. 08장 "스토리지 엔지니어" 행은 "스토리지 담당: CSI 연결 정보, VMFS LUN 매핑 해제"로 축소.
4. **03 네트워크 — 장비별 IP 기입표(빈칸 양식)**: 망별 Bastion · Master KVM 호스트 · master-0/1/2 · bootstrap · worker-1/2 각 1행(호스트명 · 관리망 IP · nasbak IP 빈칸), 망별 공통 값(관리망 대역/GW · nasbak 대역/VLAN · NTP 서버 · base domain) 빈칸. 실제 IP는 파일에 저장하지 않음(대외비).
5. **현장 설치 문서 방향**: 설계 항목 표의 상태 열(확정 / 결정 필요 / 확인 필요) 삭제, 미확정 값은 TBD 표시. 03장 "확인 필요 사항"은 08장 확정 필요 항목으로 합침(vCenter·ESXi 443·902 경로, 사내 대역 중복, 내부 HV#03 호스트 IP).
6. **MTV 방식 = VDDK**: Copy Offload · Skip VDDK cold 선택지와 "이관 방식 미확정" 제약 삭제. 스토리지 매핑 그림 가운데 열을 VDDK 하나로 변경. VDDK 이미지 빌드 → Bastion 미러 레지스트리 push 항목 추가. 08장 VMware 항목의 "ESXi SSH·VIB, VDDK 라이선스"를 "VDDK 패키지(vSphere 8 대응)"로 변경.
7. **07 설치 체크리스트(신규)**: 기존 설치 순서 9단계를 단계별 세부 작업 40개로 확장. 각 작업에 외부망 · 내부망 체크 칸과 확인 기준. 화면에서 누르면 체크가 브라우저에 저장되고(체크 초기화 버튼), 인쇄하면 빈 체크 칸.
8. **기타 문구**: 02장 작업 카드 ⑤ "안정화·원복 조건 확인" → "MTV 완료 확인", CSS 주석 동일 정정. 08장 "Windows 백업툴 방식" 삭제.
9. 버전 태그: "VERSION 1.4 / 내부 구축팀 현장 설치용 · VMware 현황 · VDDK · 설치 체크리스트".

## 검증

- 구성도 SVG 글자 넘침 검사 결과 넘침 없음.
- 브라우저 렌더링으로 01장 VMware 환경, 03장 IP 기입표, 06장 스토리지 매핑(VDDK), 07장 체크리스트 확인.
- 본문에 Copy Offload · Skip VDDK · 안정화 · 상태 배지 문구가 남지 않음을 스크립트로 확인.
