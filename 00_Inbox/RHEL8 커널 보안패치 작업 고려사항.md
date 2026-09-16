---
title: RHEL 8 커널 보안패치 작업 고려사항
tags:
  - rhel
  - kernel
  - patch
  - security
created: 2026-09-16
---

# RHEL 8 커널 보안패치 작업 고려사항

- **작업 대상**: RHEL 8
- **작업 순서**: RHEL 8.x → 8.10 마이너 업데이트 → 최신 커널 패치
- **작업 시간**: 1대당 재기동 2회, 1시간 30분 (검토 의견은 아래 참고)
- **목적**: 보안 취약점 조치

> [!note] 계획 검토 의견
> - **재기동 2회 필요 여부 확인**: `dnf update`로 8.10까지 올리면 그 시점의 최신 커널이 함께 설치되므로, 리포지토리가 최신이라면 재기동 1회로 끝나는 경우가 많다. 8.10 적용 후 안정화·검증을 거쳐 이후 커널 errata를 별도 반영하는 의도적 분리라면 계획서에 사유를 명시한다.
> - **작업 시간**: 1시간 30분은 가상 서버 기준. 물리 서버는 POST·RAID 초기화로 재기동 1회당 10~20분이 추가되므로, 재기동 2회 기준 **2시간 30분 ~ 3시간** 확보를 권고한다. 8.2/8.4 등 낮은 버전에서 점프하는 경우 패키지 1,000개 이상으로 설치 시간이 더 필요하다.

---

# 1. 작업 전 호환성 검증

## 1-1. 대상 커널 버전 확정

벤더 확인을 위해 목표 버전을 먼저 숫자로 고정한다.

```bash
cat /etc/redhat-release ; uname -r
dnf check-update kernel            # 적용 예정 커널 버전 확인
```

RHEL 8.10 기준 커널은 `4.18.0-553.x.el8_10` 계열이다. 이 버전을 기준으로 아래 검증을 진행한다.

## 1-2. 서드파티 커널 모듈 식별 (최우선)

커널이 올라가면 kABI 비호환으로 모듈이 로드되지 않아, 재기동 후 서비스가 기동되지 않거나 디스크·네트워크를 인식하지 못하는 장애가 발생한다.

```bash
# 커널 모듈 형태로 설치된 패키지
rpm -qa | grep -i -E 'kmod|dkms'

# Red Hat 제공이 아닌 모듈 확인
find /lib/modules/$(uname -r)/extra /lib/modules/$(uname -r)/weak-updates -type f 2>/dev/null

# 현재 로드된 모듈 중 서드파티 모듈 확인
lsmod | awk 'NR>1{print $1}' | while read m; do
  modinfo -F filename -F vermagic "$m" 2>/dev/null | grep -q extra && echo "$m"
done
```

## 1-3. 구성요소별 호환성 확인표

작업계획서에 아래 표를 채워 운영자 확인을 받는다.

| 구분 | 대상 예시 | 확인 방법 | 확인 결과 |
|---|---|---|---|
| 커널 모듈 SW | 서버보안·접근제어, 백신, 파일암호화 | 벤더 지원 매트릭스에서 RHEL 8.10 / 4.18.0-553 지원 여부 | |
| 백업 에이전트 | NetBackup, Networker, Commvault | 에이전트 버전의 8.10 지원 여부 | |
| 모니터링 에이전트 | Zabbix, SMS, APM | 동일 | |
| DBMS | Oracle, Tibero, PostgreSQL | 벤더 인증 OS 목록 확인 | |
| WAS | JEUS, WebLogic, Tomcat | 동일 | |
| HA·볼륨관리 | Veritas InfoScale(VxVM/VxFS), Pacemaker | 커널 모듈 사용으로 위험도 높음, 반드시 벤더 확인 | |
| 멀티패스·HBA | 스토리지 벤더 드라이버, HBA 펌웨어 | 스토리지 벤더 호환성 매트릭스 | |
| 하드웨어 | 서버 모델, NIC | Red Hat 하드웨어 인증 목록(HCL) 및 서버 벤더 확인 | |

Veritas 계열, 보안 에이전트, 백신 세 가지는 실제로 사고가 잦으므로 반드시 서면 확인을 받는다.

## 1-4. 커스텀 설정 확인

기본값이 아닌 설정이 새 커널에서도 유지되는지 확인한다.

```bash
cat /proc/cmdline                     # 부팅 파라미터
grubby --info=ALL
cat /etc/sysctl.conf /etc/sysctl.d/*.conf
ls /etc/modprobe.d/                   # 모듈 옵션, 블랙리스트
mokutil --sb-state                    # Secure Boot 사용 시 서드파티 모듈 서명 필요
```

## 1-5. 선행 검증 절차 (권고)

1. **검증 서버 선행 적용** 후 최소 1주 관찰, 이후 운영 적용
2. 검증 서버가 없으면 업무 영향도가 가장 낮은 서버 1대를 **파일럿**으로 먼저 적용
3. 파일럿 결과(부팅, 모듈 로드, 애플리케이션 기동)를 운영자와 공유한 뒤 전체 확대

검증 없이 전체 서버를 동시 진행하는 것은 권고하지 않는다.

---

# 2. 작업 절차 및 백업·롤백

## 2-1. 사전 작업 (작업일 전)

```bash
# 1) 현황 기록 (롤백 시 비교 기준)
mkdir -p /root/backup_$(date +%Y%m%d)
cd /root/backup_$(date +%Y%m%d)
uname -r                 > before_kernel.txt
rpm -qa | sort           > before_rpm_list.txt
lsmod                    > before_lsmod.txt
df -h                    > before_df.txt
ip a                     > before_ip.txt
multipath -ll            > before_multipath.txt 2>/dev/null
systemctl list-units --state=running > before_services.txt

# 2) 설정 백업
tar czvf etc_backup.tar.gz /etc/fstab /etc/multipath.conf /etc/sysconfig/network-scripts \
    /etc/sysctl.conf /etc/sysctl.d /etc/modprobe.d /etc/default/grub /boot/grub2/grub.cfg

# 3) 패키지 사전 다운로드 (작업 시간 단축)
dnf update --downloadonly -y
```

**추가 백업**

- VM: **스냅샷** (가장 확실한 롤백 수단, 작업 직전 생성)
- 물리: OS 영역 백업 또는 이미지 백업
- 어느 쪽도 불가하면, 롤백이 **커널 단위로만 가능**하다는 점을 사전에 합의

## 2-2. 작업 절차

| 순서 | 작업 내용 | 명령 / 확인 |
|---|---|---|
| 1 | 서비스 중지, 애플리케이션 정상 종료 | 운영자 수행 |
| 2 | 클러스터 노드 standby / 가상화 호스트 maintenance 전환 | |
| 3 | 스냅샷 또는 백업 생성 | |
| 4 | `/boot` 여유 공간 확인 (500MB 이상) | `df -h /boot` |
| 5 | 마이너 버전 고정 해제 | `subscription-manager release --set=8.10` |
| 6 | **tmux 또는 screen 세션에서** 업데이트 수행 | `tmux new -s patch` → `dnf update -y` |
| 7 | 커널 및 grub 반영 확인 | `rpm -qa kernel \| sort -V`, `grubby --default-kernel` |
| 8 | initramfs 생성 확인 | `ls -l /boot/initramfs-*.img` |
| 9 | `/etc/fstab` 검증 | `mount -a` (오류 없어야 함) |
| 10 | **1차 재기동** | `reboot` |
| 11 | 검증 (2-3 항목 수행) | |
| 12 | 서드파티 모듈 재설치 (필요 시) | 벤더 절차 |
| 13 | 잔여 커널 errata 적용 | `dnf update --security -y` |
| 14 | **2차 재기동** 및 최종 검증 | |
| 15 | 서비스 기동, 운영자 확인 | 운영자 수행 |

## 2-3. 재기동 후 검증

```bash
uname -r                        # 목표 커널 확인
cat /etc/redhat-release         # 8.10 확인
systemctl --failed              # 기동 실패 서비스 (없어야 정상)
lsmod > /tmp/after_lsmod.txt ; diff before_lsmod.txt /tmp/after_lsmod.txt
multipath -ll                   # 경로 수가 작업 전과 동일한지
df -h                           # 마운트 누락 확인
ip a                            # 인터페이스명, IP, 본딩 상태
dnf updateinfo list security    # 잔여 보안 errata
```

애플리케이션 기동 및 서비스 정상 여부는 운영자가 직접 확인하고 확인서를 남기는 절차를 권고한다.

## 2-4. 롤백 절차

### ① 커널만 롤백 (부팅은 되나 문제 발생 시)

```bash
# 설치된 커널 목록 확인
grubby --info=ALL | grep -E '^kernel|^index'

# 이전 커널로 기본값 변경 후 재기동
grubby --set-default=/boot/vmlinuz-<이전커널버전>
grubby --default-kernel          # 확인
reboot
```

### ② 부팅 실패 시

콘솔(iLO / iDRAC / vSphere)에서 부팅 시 GRUB 메뉴 진입 → 이전 커널 선택 → 부팅 후 위 `grubby --set-default` 수행

### ③ 패키지 전체 롤백

```bash
dnf history list
dnf history undo <ID>
```

> [!warning] 마이너 버전 업데이트는 `dnf history undo`로 완전히 되돌아가지 않는다
> 의존성 문제로 실패하거나 부분 롤백에 그칠 수 있다. 실질적인 전체 롤백 수단은 **스냅샷 또는 백업 복구뿐**이라는 점을 운영자와 사전에 합의한다.

### ④ 롤백 판단 기준 (작업계획서에 사전 명시)

- 재기동 후 부팅 불가, 스토리지 경로 미인식, 네트워크 미기동 → 즉시 롤백
- 애플리케이션 기동 실패로 운영자가 판단 → 롤백
- **롤백 결정 시점은 작업 종료 예정 시각 1시간 전으로 설정** (롤백에도 재기동 시간이 필요)

---

# 3. 업데이트 시 주의사항

**① 작업 세션이 끊기면 시스템이 손상될 수 있다.**
SSH로 `dnf update` 실행 중 세션이 끊기면 RPM 트랜잭션이 중단되어 패키지 DB가 깨진다. 반드시 `tmux` 또는 `screen` 안에서 실행한다.

```bash
tmux new -s patch      # 끊겨도 tmux attach -t patch 로 복귀
```

**② 콘솔 접근 수단을 먼저 확보한다.**
재기동 후 부팅 실패나 네트워크 미기동이면 SSH로 접속할 수 없다. iLO / iDRAC / IPMI / vSphere 콘솔 접속이 가능한지 작업 전에 실제로 테스트한다. 이것 없이 원격으로 재기동하는 것은 권고하지 않는다.

**③ `/boot` 공간 부족**
가장 흔한 실패 원인이다. 부족하면 업데이트가 중간에 실패하거나 initramfs 생성이 실패해 부팅되지 않는다.

```bash
df -h /boot                                  # 500MB 이상 여유 권장
dnf remove --oldinstallonly --setopt installonly_limit=2 kernel
```

**④ 구 커널을 삭제하지 않는다.**
롤백 수단이다. `installonly_limit`을 최소 3으로 유지한다.

```bash
grep installonly_limit /etc/dnf/dnf.conf     # installonly_limit=3
```

**⑤ 마이너 버전 고정(release lock) 및 EUS 리포지토리**
고정되어 있으면 8.10으로 올라가지 않는다. EUS 리포지토리를 사용하는 경우 8.10은 EUS 대상이 아니므로 일반 리포지토리로 전환이 필요하다.

```bash
subscription-manager release --show
subscription-manager repos --list-enabled
```

**⑥ 서드파티 모듈은 커널 업데이트 후 재설치가 필요할 수 있다.**
벤더 절차와 설치 미디어를 작업 전에 미리 확보한다. 작업 중에 구하려 하면 작업 창을 넘긴다.

**⑦ 네트워크 인터페이스 이름 변경 가능성**
드라이버가 바뀌면 인터페이스명이 변경되어 네트워크가 올라오지 않을 수 있다. 본딩 구성 서버는 특히 주의하고, 작업 전 `ip a` 결과를 반드시 남겨둔다.

**⑧ 클러스터·이중화 노드는 동시에 작업하지 않는다.**
반드시 노드 단위로 순차 진행하고, 한 노드 검증 완료 후 다음 노드로 넘어간다.

**⑨ 자동 업데이트 설정 확인**
`dnf-automatic`이 활성화되어 있으면 의도치 않은 시점에 커널이 변경된다.

```bash
systemctl is-enabled dnf-automatic.timer
```

**⑩ 커널만 올려서는 취약점 스캔이 해소되지 않을 수 있다.**
스캐너는 openssl, glibc 등 userspace 패키지도 함께 본다. 조치 대상 CVE 목록과 요구 버전을 사전에 받아 대조하고, 작업 후 재스캔까지 일정에 포함한다.

```bash
dnf updateinfo list security             # 적용 대상 보안 errata 확인
```

**⑪ 재기동 전 `mount -a`를 생략하지 않는다.**
`/etc/fstab` 오류는 현재 마운트된 상태에서는 드러나지 않다가 재기동 시 부팅 실패로 나타난다. 외부 의존 마운트에는 `_netdev,nofail` 적용을 검토한다.

**⑫ 재기동 소요 시간을 과소평가하지 않는다.**
물리 서버는 POST와 RAID 초기화만으로 10~20분이 걸린다. 재기동 2회 기준으로 작업 창을 산정한다.

---

# 참고

- RHEL 8.10은 RHEL 8의 마지막 마이너 릴리스이며, 이후로는 새 마이너 버전 없이 유지보수 단계에서 보안 errata만 제공된다(지원 종료: 2029-05-31). 이번 8.10 전환은 향후 커널 보안 패치를 계속 받기 위한 전제 조건이므로 계획서 근거로 활용할 수 있다.
- 재기동이 어려운 시스템은 커널 라이브 패치(`kpatch-patch`)로 일부 CVE를 재기동 없이 조치할 수 있다. 다만 특정 커널 스트림에 한정되고 모든 취약점을 덮지 못하므로 임시 수단으로만 사용한다.
