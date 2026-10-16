---
type: project
status: draft
created: 2026-10-15
target: SGIS_MTV_WorkPlan_v2.9.html → SGIS_MTV_WorkPlan_v2.9pt.pptx
---

# 국데처 MTV 설계 및 작업계획서 v2.9pt 릴리스 기록

[v2.9](SGIS_MTV_WorkPlan_v2.9_notes.md) HTML 문서를 발표·제출용 PowerPoint(16:9)로 변환한 버전입니다. 내용은 v2.9와 같고, v2.9 HTML은 그대로 둡니다. 반영본은 SGIS_MTV_WorkPlan_v2.9pt.pptx입니다.

## 구성 (46장)

- 표지(VERSION 2.9pt) · 목차 · 01~07장 · 작성 근거.
- 슬라이드 제목은 각 장의 소제목(h3)을 따르고, 한 슬라이드에 들어가지 않는 표·그림은 "(계속)" 슬라이드로 이어 붙임.

## 변환 방식

- 표: PowerPoint 표로 변환(편집 가능). 행이 많은 표는 머리행을 반복하여 나누고, 병합 셀(망별 rowspan)은 나누지 않음.
- 그림: v2.9 화면을 그대로 캡처한 이미지 — 01장 숫자 카드·현재 VMware 구성·구축할 OpenShift 인프라, 02장 망별 장비 재구성(행 단위로 나누어 범례와 함께 배치)·단계 카드, 04장 전체 구성도·VM 네트워크 매핑.
- 문단: 본문·참고(note, 배경 상자)·보충(muted, 작은 글씨) 구분 유지.

## 검증

- PowerPoint로 46장 전체를 렌더링하여 잘림·겹침 없음 확인.
- 슬라이드 텍스트에 IP 주소 없음, PowerMax · Copy Offload · Skip VDDK · 멀티패스 문구 없음.
