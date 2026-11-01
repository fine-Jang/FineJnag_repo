---
type: study
status: draft
created: 2026-11-01
target: OCP_Install_Guide_v0.1.html
---

# OCP 폐쇄망 설치 가이드 v0.1 릴리스 기록

개인 노션의 OCP 4.20 폐쇄망 설치 기록(2026-05)을 스터디용 HTML로 정리한 첫 버전입니다. 반영본은 [OCP_Install_Guide_v0.1.html](OCP_Install_Guide_v0.1.html)입니다.

## 결정

- 범위: 환경 → Bastion 기본 설정 → 설치 파일 준비 → 사전 작업 → 미러 레지스트리(Quay) → 자격증명 → oc-mirror 설치·카탈로그 조회 → mirror to disk → disk to mirror → 문제 해결 → 설치 파일 확인. install-config 이후 단계는 범위 밖.
- 보안: pull secret 토큰, Quay 암호, base64 계정 문자열, 이메일은 `<...>` 자리표시자로 가림. 노션 내부 링크·이미지는 넣지 않음. 실습 환경 IP·도메인은 기록 그대로.
- 긴 내용(install_quay.sh, Operator 31개 목록, IDMS 예, additionalImages 설명)은 펼치기로 접음. 코드 블록마다 복사 버튼.

## 원본에서 고치거나 표시한 곳

- 다운로드 목록: "미러 레지스트리 아카이브"에 oc 주소가 들어가 있던 것을 mirror-registry 주소로 바꿈. 4.20.16 파일이 `/ocp/4.20.21/` 폴더를 가리키던 것을 `/ocp/4.20.16/`으로 맞춤(실제 경로 확인 필요).
- 방화벽: 8443을 01장 명령에 합침.
- 확인 필요 표시: IP(192.168.45.30 vs 10.1.1.30), DNS 검색 도메인(ocp.test.local vs ocp.aon.cloud) 불일치. RHCOS 4.20.13 ISO가 4.20.16용인지.
- 인증서: 10년은 Root CA만, Quay 서버 인증서는 397일임을 표시. 원본의 확인 명령이 다른 파일을 보고 있어 올바른 확인 명령으로 대체.
- ICSP 확인 명령은 v2 기준 IDMS(`oc get imagedigestmirrorset`)로 안내. `--dest-skip-tls`는 쓰지 않음.

## 추가 (2026-11-01)

- 11 현재 Bastion 구성 · 12 DNS(bind) · 13 HAProxy 추가. 실습 Bastion(bastion.ocp.test.local, 10.182.10.2)에서 조회한 실제 설정(zone 파일, haproxy.cfg, 노드 IP)을 기준으로 작성.
  - 노드: bootstrap 10.182.10.20, master01~03 10.182.10.3~5, worker01~03 10.182.10.6~8, api · api-int · *.apps → 10.182.10.2.
  - 현재 서버와 다르게 권장한 점(본문에 표시): 한 IP에 PTR 여러 개(init-quay · ns · lb) 정리, resolv.conf의 8.8.8.8(완전 폐쇄망 시험 시 제거), haproxy defaults를 tcp로 단순화, /23 대역의 두 번째 역방향 zone.
- 14 Bootstrap 구성 추가(노션 bootstrap 기록 기준, 실습 Bastion 값으로 바꿈): bootstrap 10.182.10.20/23 · GW 10.182.10.1 · DNS 10.182.10.2, 설치 폴더 /var/www/html/ocp, ignition b.ign · m.ign · w.ign(8080). ignition 준비, ISO 부팅 후 nmcli, coreos-installer 스크립트(해시 검증 선택), 진행 확인(bootkube 로그 · 6443/22623 · wait-for bootstrap-complete), 문제 해결, 완료 후 HAProxy · VM 정리.
  - 원본 수정: `dd if=dev/zero` → `dd if=/dev/zero`. 원본의 ocp.kims.local · 192.168.45.x 값은 실습 값으로 대체.
  - 주의 표시: 설치 폴더가 웹 루트 안에 있음(auth 권한 750이라 노출은 안 됨, 웹 루트 밖 권장).

## 검증

- 토큰·암호·이메일 문자열이 남아 있지 않음을 검색으로 확인.
- Chrome 렌더링으로 머리글 · 00~02장 확인.
