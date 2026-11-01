---
type: study
status: review
created: 2026-11-01
target: 30_Study/OCP_Install_Guide_v0.1.html → v0.2
---

# OCP 폐쇄망 설치 가이드 v0.1 검토 및 v0.2 작업 요청

대상 문서: [OCP_Install_Guide_v0.1.html](OCP_Install_Guide_v0.1.html) (릴리스 기록: [OCP_Install_Guide_v0.1_notes.md](OCP_Install_Guide_v0.1_notes.md))

결론: 장 순서가 어긋나 있고, 실제 설치에 필요한 단계가 빠져 있다. 그대로 따라 하면 14장(Bootstrap)에서 쓸 ignition 파일을 만드는 절차가 없어 막힌다.

## 현재 구성 (v0.1)

00 환경 · 01 Bastion 기본 설정 · 02 설치 파일 준비(인터넷) · 03 Bastion 사전 작업 · 04 미러 레지스트리 · 05 자격증명 · 06 oc-mirror · 카탈로그 · 07 mirror → disk · 08 disk → mirror · 09 문제 해결 · 10 설치 파일 확인 · 11 현재 Bastion 구성 · 12 DNS · 13 HAProxy · 14 Bootstrap

## 1. 빠진 단계 (필수)

| 빠진 단계 | 위치 | 내용 |
|---|---|---|
| install-config → manifests → ignition | 13과 14 사이 | `ssh-keygen`, install-config.yaml 작성(pullSecret · additionalTrustBundle · imageDigestSources · networking · platform none · compute replicas 0), `openshift-install create manifests`, `mastersSchedulable: false`, chrony MachineConfig(`99-*-chrony.bu` → butane) 추가, `create ignition-configs`, install-config 백업 |
| Master · Worker 설치 | 14 다음 | 같은 coreos-installer 스크립트를 `m.ign` · `w.ign`으로 실행, worker CSR 승인(`oc get csr` / `oc adm certificate approve`, client → serving 2회) |
| 설치 완료 · 후속 | 마지막 | `openshift-install wait-for install-complete`, kubeadmin 로그인, `oc get co` · `oc get nodes`, IDMS · ITMS · CatalogSource · 서명 configmap 적용, OperatorHub 기본 소스 끄기(`disableAllDefaultSources`) |
| Bastion NTP (chrony) | Bastion 설정 쪽 | 노드 시간 기준. `allow <클러스터망>`, 상위 NTP 없으면 `local stratum 10` |

## 2. 순서 문제

| 현재 | 문제 · 조치 |
|---|---|
| 01 Bastion 설정 → 02 설치 파일 준비(인터넷) → 03 사전 작업 | 인터넷 작업이 Bastion 설정 사이에 끼어 있음. 파일 준비를 맨 앞으로, 01과 03을 합침 |
| 09 문제 해결이 중간 | 맨 끝으로 옮기고 14-5(bootstrap 문제 해결)와 합침 |
| 10 설치 파일 확인 | install-config 작성 바로 앞으로 |
| 11 현재 Bastion 구성 | 환경 정보이므로 00으로 합침 |
| 12 DNS · 13 HAProxy가 미러 레지스트리 뒤 | DNS를 먼저 구성하면 4-1의 /etc/hosts 임시 등록이 필요 없음. DNS · LB를 Bastion 기본 설정 직후로 |

## 3. 내용 불일치

- 환경 혼재: 00~10장은 `ocp.aon.cloud` · OCP 4.20.16 · 10.1.1.30(또는 192.168.45.30), 11~14장은 `ocp.test.local` · 4.18.19 · 10.182.10.x. RHCOS도 4.20.13 / 4.18.1 혼재. 재설치 환경 하나(`ocp.test.local`, 10.182.10.x)로 통일.
- 방화벽: 01장 명령에 DNS(53/tcp · udp) · NTP(123/udp) 누락.

## 4. v0.2 제안 순서

```
00 환경 (+ 현재 Bastion 구성: 호스트 · IP 표)
01 설치 파일 준비 (인터넷)                 ← v0.1 02
02 Bastion 기본 설정 · 로컬 저장소 · 패키지   ← v0.1 01 + 03
03 DNS (bind)                              ← v0.1 12
04 HAProxy                                 ← v0.1 13
05 httpd(Ignition) · NTP(chrony)            ← v0.1 03 일부 + 신규
06 미러 레지스트리 (Quay)                    ← v0.1 04
07 자격증명 (pull secret)                    ← v0.1 05
08 oc-mirror (조회 · mirror→disk · disk→mirror) ← v0.1 06~08
09 설치 파일 확인                            ← v0.1 10
10 install-config · manifests · ignition     ← 신규
11 Bootstrap                                ← v0.1 14
12 Master · Worker 설치 · CSR 승인            ← 신규
13 설치 완료 · 후속 작업                       ← 신규
14 문제 해결                                 ← v0.1 09 + 14-5
```

## 작업 시 지킬 것

- 새 버전은 `OCP_Install_Guide_v0.2.html` + `OCP_Install_Guide_v0.2_notes.md`로 만들고 v0.1은 그대로 둔다.
- 비밀값(pull secret 토큰 · Quay 암호 · base64 계정 · 이메일 · kubeadmin 암호)은 넣지 않고 `<...>` 자리표시자로 쓴다.
- 새로 쓰는 단계의 명령은 예시로 표시하고, 실습 Bastion에서 확인한 값만 실제 값으로 쓴다.
- 실습 환경 값(2026-11-01 Bastion 조회): Bastion 10.182.10.2/23 (GW 10.182.10.1), bootstrap 10.182.10.20, master01~03 10.182.10.3~5, worker01~03 10.182.10.6~8, api · api-int · *.apps → 10.182.10.2, 미러 레지스트리 `init-quay.ocp.test.local:8443`, 설치 폴더 `/var/www/html/ocp`, ignition `b.ign` · `m.ign` · `w.ign`(httpd 8080), 노드 chrony `pool 10.182.10.2 iburst`.
