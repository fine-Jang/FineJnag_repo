---
type: project
status: draft
created: 2026-10-16
target: SGIS_OCP_BuildDesign_v1.8.html → SGIS_OCP_BuildDesign_v1.9.html
---

# 국데처 SGIS OpenShift 구축설계서 v1.9 릴리스 기록

v1.8([릴리스 기록](SGIS_OCP_BuildDesign_v1.8_notes.md))에서 문서 경량화를 위해 3개 장을 삭제한 버전입니다. 반영본은 [SGIS_OCP_BuildDesign_v1.9.html](SGIS_OCP_BuildDesign_v1.9.html)이며, v1.8은 그대로 둡니다.

## 변경 사항

1. 버전 태그: "VERSION 1.9 / 기입 · 인쇄용 · 경량화(용량·MTV·제약/협의 장 삭제)".
2. 삭제한 장:
   - 04 하드웨어·용량 설계(장비·노드 사양, Worker1 수용 용량)
   - 05 MTV 이관 설계(이관 기준)
   - 07 설계 제약 및 요청·협의 사항(설계 제약, 요청 및 협의 사항)
3. 장 번호 정리: 01 개요 · 02 아키텍처 · 03 네트워크 설계 · 04 설치 체크리스트. 목차 링크도 같이 수정.
4. v1.8의 04장 뒤에 남아 있던 중복 `</section>` 태그도 같이 정리.

## 검증

- 목차·장 제목 번호 01~04 확인, `<section>` 열림·닫힘 4쌍 일치.
- 본문에 삭제한 장(#hw · #mtv · #open)을 가리키는 링크·참조 없음.
