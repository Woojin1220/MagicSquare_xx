# ECB · 계약 리뷰 (코드 수정 금지)

MagicSquare_xx / **MagicSquare_1004** — **읽기·분석만**. 파일 생성·수정·삭제·포맷·리팩터 **금지**.  
헌법: [`.cursorrules`](../../.cursorrules) · 요구: [`docs/PRD.md`](../../docs/PRD.md)

---

## 필수 선언

**응답 첫 줄:**

```
Phase: REVIEW | Layer: <all|entity|control|boundary> | Track: <Logic|UI|both> | Action: read-only
```

---

## 절차

1. 사용자가 지정한 경로(또는 `src/`, `tests/`)를 **Read/Grep만**으로 검사.
2. 아래 **체크 5항** 각각 ✅ / ❌ / N/A 판정.
3. ❌ 항목만 **위반 표**에 기록 (파일·줄·근거·헌법 조항).
4. 수정 패치·“이렇게 고치세요” 코드 블록 **제공하지 않음** (위반 사실만).
5. **commit / push 하지 않음**.

---

## 체크 5항 (계약)

### 1) ECB import 방향

| 허용 | 금지 |
|------|------|
| `boundary` → `control` → `entity` | `entity` → `control` / `boundary` |
| `control` → `entity` | `control` → `boundary` |
| `entity` → 동일 패키지 `entity` | `tests/entity`·`tests/control`에서 `boundary` 실구현 의존(Logic) |

**검색 힌트:** `from boundary`, `from control`, `from entity`, `import boundary` 등.

---

### 2) Entity — E001~E005 처리 금지

| 금지 (entity·순수 도메인) | 허용 |
|---------------------------|------|
| `"E001"`~`"E005"` 반환·raise·enum 값이 사용자 에러 코드와 1:1 | 줄 합 불일치 **판정**, 좌표·후보 **값** |
| Boundary 책임인 입력 검증 메시지 매핑 | `E006`/`E007`은 Boundary 전담 |

**검색 힌트:** `E001`, `E002`, … `E005` in `src/entity/`.

---

### 3) 성공 출력 `int[6]` · 좌표 **1-index**

| 계약 | 위반 예 |
|------|---------|
| `[r1, c1, n1, r2, c2, n2]` 길이 6 | 0-index 좌표를 성공 API로 노출 |
| 빈칸 2곳, 1~16 | `int[4]` 등 다른 형식 |

**검색 힌트:** `return [`, `int[6]`, `0-index`, 좌표 `(0,` vs `(1,`.

---

### 4) MagicConstant SSOT

| 계약 | 위반 |
|------|------|
| `34`, `16`, `4`, `0` → `src/entity/constants.py`(또는 re-export) | `src/`·`tests/`(Logic)에 **매직 리터럴** `34`/`16` 산재 |
| 테스트 Arrange 격자 숫자는 예외 가능(주석 권장) | entity/control **구현** 본문의 `== 34` 하드코딩 |

**검색 힌트:** `\b34\b`, `\b16\b` in `src/entity`, `src/control`.

---

### 5) Logic Track — Domain Mock 금지

| 경로 | 금지 | 허용 |
|------|------|------|
| `tests/entity/`, `tests/control/` | `unittest.mock`, `MagicMock`, `patch` on **entity/도메인 핵심** | 실제 import, 순수 함수, 테스트 더블이 **인프라만** |
| `tests/boundary/` | — | entity/control **Mock 허용** (UI Track) |

**검색 힌트:** `mock`, `patch`, `MagicMock` in `tests/entity`, `tests/control`.

---

## 보고 형식

### 요약

| 체크 | 결과 |
|------|------|
| 1 import 방향 | ✅ / ❌ / N/A |
| 2 entity E001~E005 | ✅ / ❌ / N/A |
| 3 int[6] 1-index | ✅ / ❌ / N/A |
| 4 MagicConstant SSOT | ✅ / ❌ / N/A |
| 5 Logic Domain Mock | ✅ / ❌ / N/A |

### 위반 표 (❌만)

| P | 파일 | 위치 | 위반 | 헌법·계약 |
|---|------|------|------|-----------|
| P0 | `src/entity/...` | L42 | `from boundary import ...` | ECB 역방향 |
| P1 | `tests/entity/...` | L10 | `patch("entity.sol...")` | Logic Domain Mock |

- **P0:** 빌드·ECB·Track 붕괴 (즉시 수정 권고 — 사용자가 구현 요청 시)
- **P1:** 계약·SSOT·Mom Test 재현 위험

**위반 0건:** “ECB·계약 위반 없음(검사 범위: …)” 한 줄.

---

## 금지 (본 Command)

| 금지 | |
|------|--|
| 코드·테스트·설정 **수정** | read-only |
| RED / GREEN / REFACTOR 수행 | REVIEW만 |
| 위반 없는데 리팩터 제안으로 확장 | 표 리뷰만 |

---

## 참고 범위

- 기본 스캔: `src/entity/`, `src/control/`, `src/boundary/`, `tests/entity/`, `tests/control/`, `tests/boundary/`
- 미구현(빈 `__init__.py`만): 체크 **N/A** 가능 — “골격만 존재” 명시
