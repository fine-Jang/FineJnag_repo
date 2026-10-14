---
type: project
status: draft
created: 2026-10-14
target: SGIS_OCP_BuildDesign_v1.6s.html
---

# 국데처 SGIS OpenShift 구축설계서 v1.6s 릴리스 기록

v1.6([릴리스 기록](SGIS_OCP_BuildDesign_v1.6_notes.md))에 기입 칸 화면 입력과 인쇄 기능을 더한 버전입니다. 반영본은 [SGIS_OCP_BuildDesign_v1.6s.html](SGIS_OCP_BuildDesign_v1.6s.html)이며, 본문 내용은 v1.6과 같습니다.

## 변경 사항

1. **기입 칸 화면 입력**: 03장 서버별 NIC 인터페이스 표와 장비별 IP 기입표의 빈칸 86개를 눌러서 입력할 수 있게 함(연노랑 칸, Enter로 입력 완료, 붙여넣기는 글자만).
   - 입력값은 이 브라우저(localStorage)에만 저장되고 HTML 파일에는 들어가지 않음. 다른 PC·브라우저에는 보이지 않음.
   - 상단 "입력 지우기" 버튼으로 전체 삭제.
2. **인쇄 버튼(상단)**: 전체 인쇄 / 기입표만 인쇄 / 체크리스트만 인쇄.
   - 기입표만 인쇄: NIC 표(외부·내부) + IP 기입표(외부·내부), A3 가로 4쪽. 망별 표가 쪽 사이에서 끊기지 않게 함.
   - 인쇄 시 입력 칸 배경은 흰색, 입력값은 그대로 출력.
3. 버전 태그: "VERSION 1.6s / 기입 · 인쇄용".

## 검증

- 표본 값을 채운 상태로 "기입표만 인쇄" PDF 출력 확인(4쪽, 표 끊김 없음, 입력값 출력).
