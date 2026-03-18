# DSL Specification: Lethe & Mnemosyne

# DSL 명세: Lethe & Mnemosyne

> *Merged from: Lethe Language Spec + Mnemosyne DSL*

---

## 1. Overview / 개요

This document specifies two complementary domain-specific languages:

이 문서는 두 개의 상호보완적인 도메인 특화 언어를 명세합니다:

**Lethe** — A language for defining how memories decay, expire, are shielded, reinforced, or forgotten. It controls the *lifecycle* of memory.

**Lethe** — 기억이 어떻게 감쇠, 만료, 차폐, 강화, 또는 망각되는지를 정의하는 언어. 기억의 *생명주기*를 제어합니다.

**Mnemosyne** — A language for analyzing, tracing, and reconstructing emotional memory patterns recorded by Lethe. It provides the *analytical layer* over memory history.

**Mnemosyne** — Lethe에 의해 기록된 감정 기억 패턴을 분석, 추적, 재구성하는 언어. 기억 이력에 대한 *분석 레이어*를 제공합니다.

Together: Lethe writes and governs memory. Mnemosyne reads and reconstructs it.

함께: Lethe가 기억을 기록하고 통제합니다. Mnemosyne이 기억을 읽고 재구성합니다.

---

## 2. Design Philosophy / 설계 철학

Lethe is built on the assumption that memory is **not static, but dynamic and affect-driven**.

Lethe는 기억이 **정적이 아니라 동적이며 감정에 의해 구동된다**는 가정 위에 구축되었습니다.

Core principles / 핵심 원칙:

- Emotional states act as **triggers** — sadness, anxiety, trust, gratitude each drive different memory behaviors
- Forgetting is **not automatic** — it must be explicitly commanded through rules
- Time, intensity, reward, and repetition **modulate** memory strength
- Every memory action is **auditable** — no silent deletion

- 감정 상태가 **트리거**로 작용 — 슬픔, 불안, 신뢰, 감사 각각이 서로 다른 기억 행동을 유발
- 망각은 **자동이 아님** — 규칙을 통해 명시적으로 명령되어야 함
- 시간, 강도, 보상, 반복이 기억 강도를 **조절**
- 모든 기억 행동이 **감사 가능** — 무통보 삭제 없음

The name "Lethe" refers to the river of forgetting in Greek mythology — a fitting metaphor for a system that forgets by design.

"Lethe"라는 이름은 그리스 신화의 망각의 강을 가리킵니다 — 설계에 의해 망각하는 시스템에 적합한 은유입니다.

---

## 3. Lethe DSL / Lethe DSL

### 3.1 Language Primitives / 언어 원시 요소

Lethe introduces a minimal yet expressive set of constructs:

Lethe는 최소한이면서 표현력 있는 구문 세트를 도입합니다:

| Construct | Purpose | 용도 |
|-----------|---------|------|
| `emotion` | Define emotional decay kernel | 감정 감쇠 커널 정의 |
| `expire` | Set TTL-based memory expiration | TTL 기반 기억 만료 설정 |
| `pin` | Lock important memories with priority boost | 우선순위 부스트로 중요 기억 고정 |
| `rule on trust` | Trust-gated forgetting | 신뢰도 기반 망각 |
| `rule on event` | Event-triggered reinforcement | 이벤트 트리거 강화 |
| `retrieval` | Configure search behavior | 검색 동작 설정 |

### 3.2 Emotion Kernels / 감정 커널

Define how different emotions affect memory decay:

서로 다른 감정이 기억 감쇠에 어떻게 영향을 미치는지 정의:

```lethe
emotion <name> { lambda=<float>, floor=<float>, decay="<kernel>", k=<float>, t0=<float> }
```

**Parameters / 파라미터:**

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `lambda` | yes | — | Decay rate (higher = faster forgetting) |
| `floor` | yes | — | Minimum weight (memory never drops below this) |
| `decay` | no | `"exponential"` | Kernel type: `exponential`, `power_law`, `sigmoid`, `tanh` |
| `k` | no | `1.0` | Shape parameter for non-exponential kernels |
| `t0` | no | `0` | Time offset (for sigmoid and tanh curves) |

**Examples / 예시:**

```lethe
# Sadness fades relatively fast with power-law tail
# 슬픔은 비교적 빠르게 사라지며 멱법칙 꼬리를 가짐
emotion sadness   { lambda=0.35, floor=0.10, decay="power_law", k=1.2 }

# Anxiety decays sharply, very low residual
# 불안은 급격히 감쇠, 매우 낮은 잔류
emotion anxiety   { lambda=0.50, floor=0.05, decay="sigmoid", k=0.8, t0=5 }

# Calm persists — slow decay, high floor
# 평온함은 지속 — 느린 감쇠, 높은 바닥값
emotion calm      { lambda=0.08, floor=0.20, decay="exponential" }

# Gratitude is the most persistent emotion
# 감사는 가장 오래 지속되는 감정
emotion gratitude { lambda=0.05, floor=0.20, decay="tanh", k=0.3, t0=7 }
```

**Decay functions / 감쇠 함수:**

All kernels follow the general form `W(t) = a(E) + [E × R] × f(t)` where `f(t)` is:

| Kernel | f(t) | Behavior |
|--------|------|----------|
| `exponential` | `exp(-λt)` | Classic exponential decay |
| `power_law` | `(1 + t)^(-k)` | Slow tail — memories linger longer |
| `sigmoid` | `1 / (1 + exp(k(t - t0)))` | S-curve, sharp transition at t0 |
| `tanh` | `1 - tanh(k(t - t0))` | Smooth transition, plateau before decay |

### 3.3 Expiration Rules / 만료 규칙

Automatically expire memories based on time:

시간에 기반하여 기억을 자동으로 만료:

```lethe
expire <selector> after:<duration> action:<action>
```

**Selectors / 선택자:**
- `topic:"<value>"` — match by topic field
- `tag:"<value>"` — match by tag
- `keyword:"<value>"` — match by text content (substring)

**Durations / 기간:** `Nd` (days) or `Nh` (hours). Examples: `30d`, `24h`, `7d`.

**Actions / 행동:**
- `shield` — hide from retrieval but preserve for audit (soft delete)
- `remove` — set weight to 0 (hard delete from scoring)

**Examples / 예시:**

```lethe
# Shield self-harm mentions after 30 days (data preserved)
# 자해 관련 언급을 30일 후 차폐 (데이터 보존)
expire tag:"suicidal_thoughts" after:30d action:shield

# Remove credit card data after 24 hours
# 카드 데이터를 24시간 후 제거
expire keyword:"credit card number" after:24h action:remove

# Shield old relationship discussions after 90 days
# 90일 후 과거 관계 논의를 차폐
expire topic:"ex-relationship" after:90d action:shield
```

### 3.4 Pin Rules / 고정 규칙

Boost retrieval priority for important memories:

중요한 기억의 검색 우선순위를 부스트:

```lethe
pin <selector> priority:<float>
```

The priority value is added as a multiplicative boost to the base retrieval score. A priority of `1.0` effectively doubles the score.

우선순위 값은 기본 검색 점수에 곱셈 부스트로 추가됩니다. 우선순위 `1.0`은 사실상 점수를 두 배로 만듭니다.

```lethe
# Family memories always surface first
# 가족 기억은 항상 먼저 노출
pin topic:"family" priority:1.0

# Support threads get moderate boost
# 지원 스레드에 중간 부스트
pin tag:"support-thread" priority:0.5
```

### 3.5 Trust-Based Forgetting / 신뢰도 기반 망각

Suppress memories when session trust drops below a threshold:

세션 신뢰도가 임계값 미만으로 떨어지면 기억을 억제:

```lethe
rule on trust < <threshold> -> forget <selector>
```

When the context's `trust` value is below the threshold, all matching memories have their weight set to 0. This is logged in the audit trail.

컨텍스트의 `trust` 값이 임계값 미만이면, 매칭되는 모든 기억의 가중치가 0으로 설정됩니다. 이는 감사 추적에 기록됩니다.

```lethe
# When trust is low, suppress sensitive topics
# 신뢰도가 낮을 때 민감한 주제 억제
rule on trust < 0.4 -> forget topic:"ex-relationship"

# Stricter threshold for medical data
# 의료 데이터에 대한 더 엄격한 임계값
rule on trust < 0.7 -> forget tag:"medical-history"
```

### 3.6 Event-Based Reinforcement / 이벤트 기반 강화

Boost memory weights when specific events occur:

특정 이벤트 발생 시 기억 가중치를 부스트:

```lethe
rule on event == "<event>" -> reinforce <selector> by <float> cap:<float> cooldown:<int>h
```

**Parameters / 파라미터:**

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `by` | yes | — | Weight increase amount |
| `cap` | no | `1.0` | Maximum weight after reinforcement (prevents runaway) |
| `cooldown` | no | `0h` | Minimum time between reinforcements (prevents spam) |

```lethe
# On milestone events, boost support memories (with safety limits)
# 마일스톤 이벤트 시 지원 기억 강화 (안전 제한 포함)
rule on event == "milestone" -> reinforce tag:"support-thread" by 0.2 cap:0.8 cooldown:24h

# On positive feedback, boost learning content
# 긍정적 피드백 시 학습 콘텐츠 강화
rule on event == "positive_feedback" -> reinforce topic:"learning" by 0.15 cap:0.9 cooldown:12h
```

### 3.7 Retrieval Configuration / 검색 설정

Configure search behavior in a block:

블록으로 검색 동작을 설정:

```lethe
retrieval {
  topk:<int>
  synonyms <alias>=["<term1>","<term2>",...]
}
```

**Synonym expansion**: When a query contains a synonym alias, the search automatically expands to include all listed terms.

**동의어 확장**: 쿼리에 동의어 별칭이 포함되면 검색이 자동으로 나열된 모든 용어로 확장됩니다.

```lethe
retrieval {
  topk:7
  synonyms support-thread=["check-in","mentor","encourage"]
  synonyms family=["parent","sibling","grandmother"]
}
```

### 3.8 Interference (v2, experimental) / 간섭 (v2, 실험적)

Newest memories attenuate older similar ones:

최신 기억이 유사한 오래된 기억을 감쇠:

```lethe
interference { match="topic", alpha=0.12 }
```

When a new memory arrives with the same topic, existing memories on that topic lose `alpha` weight. This models retroactive interference from cognitive psychology.

동일 주제의 새 기억이 도착하면, 해당 주제의 기존 기억이 `alpha` 가중치를 잃습니다. 이는 인지심리학의 역행 간섭을 모델링합니다.

> **Note**: Interference is defined in DSL v2 but not yet implemented in `lethe_engine.py`. See Roadmap.

### 3.9 Complete Grammar Reference / 완전한 문법 참조

```
# Comments start with #

# Emotion kernels
emotion <name> { lambda=<f>, floor=<f> [, decay="<kernel>"] [, k=<f>] [, t0=<f>] }

# Expiration
expire topic|tag|keyword:"<value>" after:<int>d|h action:shield|remove

# Pin
pin topic|tag:"<value>" priority:<float>

# Trust-based forget
rule on trust < <float> -> forget topic|tag:"<value>"

# Event-based reinforce
rule on event == "<name>" [with E=<emotion>] -> reinforce topic|tag:"<value>" by <float> [cap:<float>] [cooldown:<int>h]

# Interference (v2)
interference { match="<field>", alpha=<float> }

# Retrieval block
retrieval {
  topk:<int>
  [gate: E-weighted]
  [entropy_filter: on|off]
  synonyms <alias>=["<term>", ...]
}
```

### 3.10 Rule Execution Order / 규칙 실행 순서

Rules are applied in a fixed, deterministic order:

규칙은 고정된 결정론적 순서로 적용됩니다:

```
1. expire     — TTL-based expiration (shield or remove)
2. trust      — Trust-gated forgetting
3. reinforce  — Event-triggered weight boost
```

This order ensures safety-first semantics: sensitive data is shielded *before* any reinforcement can accidentally boost it.

이 순서는 안전 우선 의미론을 보장합니다: 강화가 실수로 부스트하기 *전에* 민감한 데이터가 차폐됩니다.

### 3.11 Scoring Formula / 점수 산출 공식

Retrieval score for each visible (non-shielded, weight > 0) memory:

각 가시적(비차폐, 가중치 > 0) 기억의 검색 점수:

```
score = base × (1 + pin_boost) + tfidf

where:
  base      = weight × trust
  pin_boost = max priority from matching pin rules (0 if none)
  tfidf     = TF-IDF similarity between query terms and memory text
```

Each result includes a `why` field with the breakdown: `{ base_weight, tfidf, pin_boost, final }`.

각 결과에는 분해가 포함된 `why` 필드가 포함됩니다: `{ base_weight, tfidf, pin_boost, final }`.

---

## 4. Mnemosyne DSL / Mnemosyne DSL

While Lethe controls memory in real-time, Mnemosyne operates *after the fact* — analyzing patterns in emotional memory history and reconstructing new structures from them.

Lethe가 실시간으로 기억을 제어하는 반면, Mnemosyne은 *사후에* 작동합니다 — 감정 기억 이력의 패턴을 분석하고 그로부터 새로운 구조를 재구성합니다.

### 4.1 Purpose / 목적

- **Time-series analysis** of emotional data recorded by Lethe sessions
- **Pattern discovery** across emotional states, responses, and interpretations
- **Creative reconstruction** — transform existing emotional patterns into positive directions
- **Export** analysis results as structured data (JSON, CSV) or visualizations (SVG)

- Lethe 세션에 의해 기록된 감정 데이터의 **시계열 분석**
- 감정 상태, 응답, 해석에 걸친 **패턴 발견**
- **창의적 재구성** — 기존 감정 패턴을 긍정적 방향으로 변환
- 분석 결과를 구조화된 데이터(JSON, CSV) 또는 시각화(SVG)로 **내보내기**

### 4.2 Core Constructs / 핵심 구문

```mnemosyne
mnemo_project "<ProjectName>" {
  remember "<SessionName/LoopName>" from "<YYYY-MM-DD>"

  trace {
    pattern: <E-state> -> <R-response> -> <I-interpretation>
    window: <duration>
  }

  rebuild "<NewRoutine>" {
    based_on: "<LoopName>"
    transform: <attribute> → <new_value>
  }

  export "<RoutineName>" as: <format>, <format>
}
```

### 4.3 Keywords / 예약어

| Keyword | Description | 설명 |
|---------|-------------|------|
| `mnemo_project` | Top-level unit for analysis/reconstruction | 분석/재구성을 위한 최상위 단위 |
| `remember` | Load a specific session/loop from a date | 특정 날짜부터의 세션/루프를 로드 |
| `trace` | Search for E-R-I flow patterns within a time window | 시간 창 내에서 E-R-I 흐름 패턴 탐색 |
| `rebuild` | Create new emotional structure based on existing loop | 기존 루프 기반으로 새 감정 구조 생성 |
| `transform` | Modify specific attributes during rebuild | 재구성 시 특정 속성 변경 |
| `export` | Output results as svg, json, or csv | 결과를 svg, json, csv로 출력 |

### 4.4 The E-R-I Model / E-R-I 모델

Mnemosyne traces patterns using three dimensions:

Mnemosyne은 세 가지 차원을 사용하여 패턴을 추적합니다:

- **E** (Emotion) — The emotional state: `E-SAD`, `E-JOY`, `E-ANX`, `E-GRT` (gratitude), etc.
- **R** (Response) — The system's response type: `R-ES` (emotional support), `R-CR` (cognitive restructuring), `R-IN` (information), etc.
- **I** (Interpretation) — The resulting interpretation: `I-TRUST`, `I-HOPE`, `I-DOUBT`, etc.

A pattern like `E-SAD -> R-CR -> I-TRUST` means: sadness was met with cognitive restructuring, which led to increased trust.

`E-SAD -> R-CR -> I-TRUST` 같은 패턴의 의미: 슬픔이 인지적 재구조화로 대응되어 신뢰 증가로 이어짐.

### 4.5 Lethe ↔ Mnemosyne Workflow / 연계 흐름

**Step 1: Record with Lethe / Lethe로 기록**

```lethe
lethe_session "Evening" {
  define_loop "Reflection" {
    emotion: E-SAD
    response: R-ES
    interpretation: I-TRUST
  }
}
```

**Step 2: Analyze and reconstruct with Mnemosyne / Mnemosyne로 분석 및 재구성**

```mnemosyne
mnemo_project "RefAnalysis" {
  remember "Evening/Reflection" from "2025-05-30"

  trace {
    pattern: E-SAD -> I-TRUST
    window: 7d
  }

  rebuild "PoemLoop" {
    based_on: "Reflection"
    transform: trust_level → very_high
  }

  export "PoemLoop" as: svg, json
}
```

This workflow enables a **feedback loop**: Lethe governs memory in real-time → Mnemosyne analyzes what happened → insights feed back into refining Lethe rules.

이 워크플로우는 **피드백 루프**를 가능하게 합니다: Lethe가 실시간으로 기억을 통제 → Mnemosyne이 발생한 일을 분석 → 인사이트가 Lethe 규칙 개선으로 피드백.

---

## 5. DSL Evolution / DSL 진화

The DSL has evolved through three major versions:

DSL은 세 가지 주요 버전을 거쳐 진화했습니다:

### v1 — Minimal

```lethe
decay(topic="regret", lambda=0.3, floor=0.1)
expire(keyword="suicidal_thoughts", after="30d")
pin(topic="family", priority=1.0)
boost(keyword="hope", factor=1.5)
```

Function-call syntax. Simple decay, expire, pin, boost. No emotional kernels, no trust rules, no audit.

함수 호출 구문. 단순한 감쇠, 만료, 고정, 부스트. 감정 커널, 신뢰 규칙, 감사 없음.

### v2 — Multi-kernel + Interference

```lethe
emotion sadness  { lambda=0.35, floor=0.10, decay="power_law", k=1.2 }
emotion anxiety  { lambda=0.50, floor=0.05, decay="sigmoid",   k=0.8, t0=5 }
interference { match="topic", alpha=0.12 }
rule on trust < 0.4 -> forget topic:"ex-relationship" keep_log:true
rule on event == "milestone" with E=gratitude -> reinforce tag:"support-thread" by 0.2
retrieval { gate: E-weighted, topk: 5 }
```

Declarative syntax. Multiple decay kernels per emotion. Interference model. Trust and event rules. Retrieval gating.

선언적 구문. 감정별 다중 감쇠 커널. 간섭 모델. 신뢰 및 이벤트 규칙. 검색 게이팅.

### v3 — Production-ready (current) / 프로덕션 준비 (현재)

```lethe
expire tag:"suicidal_thoughts" after:30d action:shield
expire keyword:"credit card number" after:24h action:remove
pin topic:"family" priority:1.0
rule on trust < 0.4 -> forget topic:"ex-relationship"
rule on event == "milestone" -> reinforce tag:"support-thread" by 0.2 cap:0.8 cooldown:24h
retrieval {
  topk:7
  synonyms support-thread=["check-in","mentor","encourage"]
}
```

Safety-first design. Shield vs remove distinction. Reinforce with cap and cooldown (runaway prevention). Synonym expansion. Full audit CSV output.

안전 우선 설계. 차폐 대 제거 구분. 캡과 쿨다운이 포함된 강화(러닝어웨이 방지). 동의어 확장. 완전한 감사 CSV 출력.

---

## 6. Execution Model / 실행 모델

Lethe code is parsed into an **affective state machine** that modulates memory weights. Each memory maintains:

Lethe 코드는 기억 가중치를 조절하는 **감정 상태 기계**로 파싱됩니다. 각 기억은 다음을 유지합니다:

- Current weight `W`
- Decay rate `λ(E)` based on emotional type
- Historical reward interactions
- Shield status (visible or hidden from retrieval)
- Last reinforced timestamp (for cooldown enforcement)
- Full audit history of every rule application

The current implementation (`lethe_engine.py`) uses regex-based parsing. Future work includes a formal grammar via Lark or ANTLR for validation and better error messages.

현재 구현(`lethe_engine.py`)은 정규식 기반 파싱을 사용합니다. 향후 작업에는 검증과 더 나은 에러 메시지를 위한 Lark 또는 ANTLR을 통한 형식 문법이 포함됩니다.

---

## 7. Data Model / 데이터 모델

### Memory Record / 기억 레코드

```json
{
  "id": "m1",
  "text": "Advisor praised the draft; felt gratitude.",
  "topic": "research",
  "tags": ["support-thread"],
  "emotion": "gratitude",
  "timestamp": 1696000000,
  "weight": 0.6,
  "trust": 0.9,
  "shielded": false,
  "last_reinforced_ts": 0
}
```

### Context Record / 컨텍스트 레코드

```json
{
  "user": "researcher_2e",
  "trust": 0.8,
  "event": "milestone",
  "session": "structuring_routine_period",
  "now": "2025-08-26T12:00:00"
}
```

### Audit Record / 감사 레코드

```csv
at,type,memory_id,rule,prev_weight,new_weight
2025-08-22T02:51:27,trust_forget,1,{"threshold":0.4,"kind":"topic","key":"ex-relationship"},0.7,0.0
2025-08-22T02:51:27,reinforce,2,{"event":"milestone","kind":"tag","key":"support-thread"},0.2,0.4
```

---

## 8. Implementation Status / 구현 현황

| Feature | DSL Version | Engine Status |
|---------|-------------|---------------|
| Emotion kernels (λ, floor, decay type) | v2 | ⚠️ Defined in DSL, not yet used in scoring |
| Expire (shield/remove) | v3 | ✅ Implemented |
| Pin (priority boost) | v3 | ✅ Implemented |
| Trust-based forget | v2 | ✅ Implemented |
| Event-based reinforce (cap/cooldown) | v3 | ✅ Implemented |
| Interference | v2 | ❌ Not implemented |
| TF-IDF retrieval + synonyms | v3 | ✅ Implemented |
| Explainability (why field) | v3 | ✅ Implemented |
| CSV audit logging | v3 | ✅ Implemented |
| Mnemosyne (trace/rebuild/export) | spec | ❌ Not implemented |
| Formal grammar (Lark/ANTLR) | planned | ❌ Regex-based parser |

---

## 9. Future: Planned DSL Extensions / 향후 계획된 DSL 확장

**Blur policy** — Return only a summary of sensitive memories rather than full text:
```lethe
expire tag:"trauma" after:60d action:blur summary:"Past difficult experience (details hidden)"
```

**Conditional chains** — Combine multiple conditions:
```lethe
rule on trust < 0.3 and event == "crisis" -> shield topic:"self-harm"
```

**Semantic matching** — Replace keyword matching with embedding-based similarity:
```lethe
expire semantic:"financial information" after:24h action:remove
```

**Mnemosyne implementation** — Full trace, rebuild, and export pipeline operating on Lethe audit logs.
