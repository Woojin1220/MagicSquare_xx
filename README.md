# MagicSquare_xx

4×4 **부분 마방진**(빈칸 2개)에서 **10선 합=34** 판정을 빠짐없이·기계적으로 수행하고, 깨진 줄(특히 **`/`**)을 즉시 식별하는 TDD · ECB 프로젝트입니다.

**상세 스펙:** [docs/PRD.md](docs/PRD.md)

---

## 배경 (Mom Test)

학습자가 **특정 행·열부터** 합을 맞추고 `\`·`/`까지 본 뒤 **맞다고 제출**했으나 **채점**에서 오답. 재풀이 중 **반대 대각선 `/` 합** 오류를 발견했고 **약 10분** 추가 소요 ([PRD §1](docs/PRD.md#1-배경-mom-test)).

| 항목 | 내용 |
|------|------|
| **페르소나** | 4×4 부분 마방진을 손으로/코드로 다루는 학습자 |
| **진짜 문제** | 손 검증·`/`` 34 비교 후에도 채점 오답 → `/` 합 오류 · **10분** |
| **증거** | 「행·열부터 맞춤」 / 「맞다고 넘어감」 / 「채점→10분→반대 대각선」 |
| **표면 문제 (비목표)** | 검증/풀이 프로그램·PyQt 완성 앱·ECB 설계 완성만 목표로 삼기 |

## 핵심 질문 ([PRD §12](docs/PRD.md#12-핵심-질문))

> **4×4 격자에서 빈칸 2개를 채운 결과가 부분 마방진 조건(10선=34)을 만족하는가?**

## 목표 · 비목표

**목표** ([PRD §2](docs/PRD.md#2-목표))

- 10선 합 **34** 검증 · 실패 시 **줄 식별**(행/열/`\`/`/`)
- 빈칸 좌표·후보 판정 (Logic Track)
- **채점 전** SC-1~3 충족 (채점 후 10분 재작업 방지)

**비목표** ([PRD §3](docs/PRD.md#3-비목표))

- PyQt 상용 앱 · 배포
- 3×3 / 5×5 / 자동 생성
- 세션 3 Domain GREEN · UI **완료**
- 수동 “대충 맞음” 확인만으로 완료

## 도메인 규칙 ([PRD §5](docs/PRD.md#5-도메인-규칙))

| 규칙 | 설명 |
|------|------|
| R-01 | 격자 **4×4** |
| R-02 | 셀: `0`(빈칸) 또는 `1..16` |
| R-03 | 빈칸 **정확히 2개** |
| R-04 | 1~16 **중복 없음** |
| R-05 | **10선** 각각 합 = **34** |
| R-06 | 10선 = 행4 + 열4 + `\` + `/` |

### 예시 격자 (슬라이드 4.1)

| | c1 | c2 | c3 | c4 |
|---|----|----|----|-----|
| r1 | 16 | 3 | 2 | 13 |
| r2 | 5 | 10 | 11 | **0** |
| r3 | 9 | 6 | **0** | 12 |
| r4 | 4 | 15 | 14 | 1 |

빈칸: (r2,c4), (r3,c3).

## 성공 기준 ([PRD §7](docs/PRD.md#7-성공-기준-mom-test))

| ID | 기준 | Mom Test |
|----|------|----------|
| SC-1 | 10선 합 **전부** 검증 (`\`·`/` 포함) | 「행·열부터 맞춤」 |
| SC-2 | ≠34 → 실패 + **줄 식별** | 「맞다고 넘어감」+ 「반대 대각선」 |
| SC-3 | 원인 줄 특정 **1분 이내** | 「10분」+ 「처음부터 다시」 |

## 문제 인식 조건 ([PRD §6.5](docs/PRD.md#65-문제-인식-조건-슬라이드--3개-이상))

| # | 조건 |
|---|------|
| P-01 | 10선 중 한 줄 합 ≠ 34 (예: `/`) |
| P-02 | 빈칸 개수 ≠ 2 |
| P-03 | 1~16 중복 또는 범위 위반 |
| P-04 | (선택) 빈칸 미채움 상태에서 완료 |

## 에러 코드 ([PRD §10](docs/PRD.md#10-에러-코드))

| 코드 | 의미 |
|------|------|
| E001 | 크기 ≠ 4×4 |
| E002 | 빈칸 ≠ 2 |
| E003 | 범위·중복·null |
| E004 | 특정 줄 합 ≠ 34 |

## 아키텍처 ([PRD §9](docs/PRD.md#9-아키텍처-ecb--슬라이드))

| 계층 | 책임 | 후보 |
|------|------|------|
| **Entity** | 격자·셀·판정 | `MagicSquare`, `Cell`, `SolveResult` |
| **Control** | 검증·탐색·풀이 | `SquareValidator`, `MissingFinder`, `Solver` |
| **Boundary** | I/O·표시 | `GridUI`, `InputHandler`, `ResultDisplay` |

- **Dual-Track TDD:** Logic `D-*` + UI `U-*`
- **RED 우선:** pytest FAIL → GREEN → REFACTOR

### 세션 3 산출

| 계층 | 산출 |
|------|------|
| Rule | `.cursorrules` |
| Command | `/tdd-red`, `/pytest-logic` |
| Skill | `magic-square-tdd` |
| Test Loop | pytest RED → FAIL |

## C2C · RED 순서 ([PRD §8](docs/PRD.md#8-c2c-추적-예시))

**권장:** `D-VAL-04` (`/`) → `D-VAL-05` (10선 전체)

| Test ID | PRD | 요약 | 상태 |
|---------|-----|------|------|
| D-VAL-04 | FR-VAL-04 | `/` 합 = 34 | ⏳ |
| D-VAL-05 | FR-VAL-05 | 10선 전체 | ⏳ |
| D-VAL-03 | FR-VAL-03 | `\` 합 = 34 | ⏳ |
| D-LOC-01 | FR-LOC-01 | 빈칸 2좌표 | ⏳ |
| D-SOL-01 | FR-SOL-01 | 빈칸 대입 풀이 | ⏳ |
| U-IN-01~05 | FR-IN-01~05 | 입력 검증 | ⏳ |
| U-OUT-01~02 | FR-OUT-01~02 | 출력 | ⏳ |

## 사용자 ([PRD §4](docs/PRD.md#4-사용자))

- **Primary:** 4×4 부분 마방진 과제 학습자
- **Secondary:** TDD / ECB / Cursor 워크플로 실습자

## 문서

| 문서 | 설명 |
|------|------|
| [docs/PRD.md](docs/PRD.md) | **SSOT** — FR/SC/C2C/ECB/에러 코드 |
| [Report/01.MagicSquare_ProblemDefinition_Report.md](Report/01.MagicSquare_ProblemDefinition_Report.md) | Mom Test · 세션 3 워크북 |
| [Prompt/01.MagicSquare_Session1_MomTest_ProblemDefinition-Transcript.md](Prompt/01.MagicSquare_Session1_MomTest_ProblemDefinition-Transcript.md) | 세션 1 Transcript |

## 프로젝트 구조

```
MagicSquare_xx/
├── README.md
├── docs/PRD.md
├── Report/01.*.md
├── Prompt/01.*-Transcript.md
│
│  (예정 — [PRD §13](docs/PRD.md#13-다음-단계))
├── .cursorrules
├── src/{entity,control,boundary}/
└── tests/{entity,control,boundary}/
```

## 개발 환경 (코드 골격 추가 후)

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -e ".[dev]"
python -m pytest tests/ -v
```

## 다음 단계 ([PRD §13](docs/PRD.md#13-다음-단계))

1. Mom Test Q11 보완(선택) — `/` 검증 시 빈칸에 최종 숫자 여부
2. `.cursorrules` + `/tdd-red`
3. `tests/entity/test_d_val_04.py` RED — `/` 합 ≠ 34 FAIL 로그

## 용어 ([PRD §11](docs/PRD.md#11-용어))

| 용어 | 정의 |
|------|------|
| 마법 상수 | **34** |
| 10선 | 행4 + 열4 + `\` + `/` |
| 빈칸 | `0`인 셀 (**2개**) |
| 부분 마방진 | 빈칸 2개를 채우면 완전 마방진이 되는 4×4 격자 |
