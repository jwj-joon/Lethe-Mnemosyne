# Lethe / Mnemosyne

**A Lightweight Framework for Emotional Memory Governance in AI Agents**
**AI 에이전트를 위한 감정 기반 기억 거버넌스 경량 프레임워크**

---

> *"Memory is not storage. It is selection."*
> *"기억은 저장이 아니라 선택이다."*

Lethe models **forgetting, decay, and reinforcement** of memories through affective rules.
Mnemosyne provides a DSL for **analysis, tracing, and reconstruction** of emotional memory patterns.

Together, they form a **dependency-free, auditable framework** for managing memory in AI agents — where privacy, trust, emotional salience, and explainability are first-class design principles.

Lethe는 감정 규칙을 통해 기억의 **망각, 감쇠, 강화**를 모델링합니다.
Mnemosyne은 감정 기억 패턴의 **분석, 추적, 재구성**을 위한 DSL을 제공합니다.

두 시스템은 함께 작동하여, 프라이버시·신뢰·감정 중요도·설명가능성을 핵심 설계 원칙으로 삼는 **외부 의존성 없는 감사 가능한 프레임워크**를 구성합니다.

---

## Why This Exists / 왜 만들었는가

Most AI memory systems are designed to **remember everything**. But humans don't work that way — we forget based on emotion, context, trust, and time. This isn't a flaw. It's a feature.

대부분의 AI 메모리 시스템은 **모든 것을 기억하도록** 설계됩니다. 하지만 인간은 그렇게 작동하지 않습니다 — 감정, 맥락, 신뢰, 시간에 기반하여 망각합니다. 이것은 결함이 아닙니다. 설계 원칙입니다.

Lethe/Mnemosyne asks a different question:

> **What should an AI forget, and why?**
> **AI는 무엇을 잊어야 하며, 왜 잊어야 하는가?**

This framework provides the tools to answer that question — declaratively, safely, and with a full audit trail.

---

## Core Concepts / 핵심 개념

### Emotion-Weighted Decay / 감정 가중 감쇠

Memory strength decays over time, modulated by emotional intensity, interaction frequency, and reward:

기억의 강도는 시간에 따라 감쇠하며, 감정 강도·상호작용 빈도·보상에 의해 조절됩니다:

```
W(t) = a(E) + [E × R] × exp(-λ(E) × t / I)
```

| Symbol | Meaning | 의미 |
|--------|---------|------|
| `W(t)` | Memory weight at time *t* | 시간 *t*에서의 기억 가중치 |
| `a(E)` | Emotion-specific floor (minimum retention) | 감정별 최소 유지값 |
| `E` | Emotion intensity | 감정 강도 |
| `R` | Reward (resolution, trust, coherence) | 보상 (해결, 신뢰, 일관성) |
| `λ(E)` | Emotion-based decay rate | 감정별 감쇠 속도 |
| `I` | Interaction count | 상호작용 횟수 |

Different emotions decay differently — sadness fades faster than gratitude; anxiety decays sharply but may leave residual traces. The DSL supports multiple decay kernels: `exponential`, `power_law`, `sigmoid`, `tanh`.

감정마다 감쇠 양상이 다릅니다 — 슬픔은 감사보다 빨리 사라지고, 불안은 급격히 감쇠하지만 잔류 흔적을 남길 수 있습니다. DSL은 `exponential`, `power_law`, `sigmoid`, `tanh` 등 다양한 감쇠 커널을 지원합니다.

### Selective Forgetting / 선택적 망각

Forgetting is not random deletion — it is a governed process:

망각은 무작위 삭제가 아닌, 통제된 프로세스입니다:

- **Trust-based**: When trust drops below a threshold, sensitive topics are suppressed
- **TTL expiration**: Memories expire after a defined period (shield or remove)
- **Keyword shielding**: Sensitive data (e.g., credit card numbers, self-harm mentions) is automatically shielded from retrieval while preserved for audit

- **신뢰 기반**: 신뢰도가 임계값 미만이면 민감한 주제가 억제됩니다
- **TTL 만료**: 정의된 기간 후 기억이 만료됩니다 (차폐 또는 제거)
- **키워드 차폐**: 민감 데이터(예: 카드번호, 자해 언급)는 검색에서 자동 차폐되되 감사용으로 보존됩니다

### Explainable Retrieval / 설명 가능한 검색

Every retrieval returns a **score breakdown** — not just what was remembered, but *why*:

모든 검색 결과에는 **점수 분해**가 포함됩니다 — 무엇을 기억했는지뿐 아니라 *왜 기억했는지*:

```json
{
  "text": "Advisor praised the draft; felt gratitude and motivation.",
  "score": 0.872,
  "why": {
    "base_weight": 0.40,
    "tfidf": 0.072,
    "pin_boost": 1.0,
    "final": 0.872
  }
}
```

### Audit Trail / 감사 추적

Every rule application — every forget, shield, reinforce, expire — is logged with timestamp, previous weight, new weight, and the rule that triggered it. This enables full traceability and regulatory compliance (GDPR right to erasure, EU AI Act).

모든 규칙 적용 — 망각, 차폐, 강화, 만료 — 은 타임스탬프, 이전 가중치, 새 가중치, 발동 규칙과 함께 기록됩니다. 이를 통해 완전한 추적성과 규제 준수(GDPR 삭제권, EU AI Act)가 가능합니다.

---

## Architecture / 아키텍처

```
┌─────────────────────────────────────────────────────┐
│                   Lethe Engine                       │
│                                                     │
│  ┌───────────┐   ┌──────────────┐   ┌───────────┐  │
│  │ DSL Parser │──▶│ Rule Engine   │──▶│ Audit Log │  │
│  └───────────┘   │              │   └───────────┘  │
│                  │ 1. expire    │                   │
│  ┌───────────┐   │ 2. trust     │   ┌───────────┐  │
│  │ memories  │──▶│    forget    │──▶│ updated   │  │
│  │ .json     │   │ 3. reinforce │   │ memories  │  │
│  └───────────┘   └──────────────┘   └───────────┘  │
│                                                     │
│  ┌───────────┐   ┌──────────────┐   ┌───────────┐  │
│  │  context  │──▶│  Retrieval   │──▶│ ranked    │  │
│  │  .json    │   │ TF-IDF +     │   │ results   │  │
│  │           │   │ weight +     │   │ + why     │  │
│  └───────────┘   │ pin + synonym│   └───────────┘  │
│                  └──────────────┘                   │
└─────────────────────────────────────────────────────┘

      ┌──────────────────────────────────────┐
      │          Mnemosyne DSL               │
      │                                      │
      │  remember ─▶ trace ─▶ rebuild ─▶     │
      │                              export  │
      │  (pattern analysis &                 │
      │   emotional reconstruction)          │
      └──────────────────────────────────────┘
```

### Theoretical Foundation / 이론적 기반

The architecture extends to a proposed modification of transformer attention, where Q, K, V are reinterpreted through emotional context:

이 아키텍처는 트랜스포머 어텐션의 Q, K, V를 감정 맥락으로 재해석하는 구조로 확장됩니다:

| Component | Standard Transformer | Lethe Reinterpretation |
|-----------|---------------------|----------------------|
| **Q** (Query) | Token embedding | Emotion-based intent vector (affective state + time + goal) |
| **K** (Key) | Learned representation | Memory slots filtered by emotional associative matching |
| **V** (Value) | Output projection | Adaptive response strategy (informational / empathetic / deflective) |

Lightweight control alternatives (no RL required): Multi-Armed Bandits for Q, Sparse Attention with Associative Memory for K, Mixture-of-Experts for V. See `docs/ARCHITECTURE.md` for details.

경량 제어 대안 (RL 불필요): Q에 Multi-Armed Bandits, K에 연관 기억 기반 희소 어텐션, V에 Mixture-of-Experts. 상세 내용은 `docs/ARCHITECTURE.md`를 참고하세요.

---

## DSL Quick Reference / DSL 요약

Lethe rules are human-readable, declarative statements. No code required:

Lethe 규칙은 사람이 읽을 수 있는 선언형 문장입니다. 코드가 필요 없습니다:

```lethe
# Safety: shield self-harm mentions after 30 days (data preserved for audit)
# 안전: 자해 관련 언급을 30일 후 차폐 (감사용 데이터는 보존)
expire tag:"suicidal_thoughts" after:30d action:shield

# Privacy: remove credit card data after 24 hours
# 프라이버시: 카드번호를 24시간 후 제거
expire keyword:"credit card number" after:24h action:remove

# Pin important topics to boost retrieval
# 중요 주제를 고정하여 검색 가중치 가산
pin topic:"family" priority:1.0

# Suppress sensitive memories when trust is low
# 신뢰도가 낮을 때 민감한 기억 억제
rule on trust < 0.4 -> forget topic:"ex-relationship"

# Reinforce positive memories on milestone events (with runaway prevention)
# 마일스톤 이벤트 시 긍정 기억 강화 (러닝어웨이 방지 포함)
rule on event == "milestone" -> reinforce tag:"support-thread" by 0.2 cap:0.8 cooldown:24h

# Retrieval settings with synonym expansion
# 동의어 확장이 포함된 검색 설정
retrieval {
  topk:7
  synonyms support-thread=["check-in","mentor","encourage"]
}
```

### Emotion Kernels / 감정 커널

```lethe
emotion sadness   { lambda=0.35, floor=0.10, decay="power_law", k=1.2 }
emotion anxiety   { lambda=0.50, floor=0.05, decay="sigmoid",   k=0.8, t0=5 }
emotion calm      { lambda=0.08, floor=0.20, decay="exponential" }
emotion gratitude { lambda=0.05, floor=0.20, decay="tanh",      k=0.3, t0=7 }
```

### Full Grammar / 전체 문법

| Rule | Syntax | Effect |
|------|--------|--------|
| **Expire** | `expire topic\|tag\|keyword:"..." after:Nd\|Nh action:shield\|remove` | TTL-based expiration |
| **Pin** | `pin topic\|tag:"..." priority:F` | Boost retrieval score |
| **Forget** | `rule on trust < T -> forget topic\|tag:"..."` | Trust-gated suppression |
| **Reinforce** | `rule on event == "E" -> reinforce tag:"..." by F cap:F cooldown:Nh` | Event-driven weight boost |
| **Retrieval** | `retrieval { topk:N; synonyms alias=["a","b"] }` | Search configuration |

---

## Quickstart / 빠른 시작

### Requirements / 요구사항

Python 3.8+, no external dependencies.
Python 3.8 이상, 외부 의존성 없음.

### 1. Run the demo / 데모 실행

```bash
python demo.py
```

Output shows before/after memory states and a full audit log of every rule that fired.

규칙 적용 전/후 메모리 상태와 발동된 모든 규칙의 감사 로그가 출력됩니다.

### 2. Apply rules with audit logging / 규칙 적용 및 감사 로그 생성

```bash
python lethe_engine.py run \
  --mem examples/memories.json \
  --ctx examples/context.json \
  --dsl examples/rules.lethe \
  --event milestone \
  --audit lethe_audit.csv \
  --before lethe_before.csv \
  --after lethe_after.csv
```

This produces three CSV files:
- `lethe_before.csv` — memory state before rules
- `lethe_after.csv` — memory state after rules (with shield flags)
- `lethe_audit.csv` — every rule application with timestamps

세 개의 CSV 파일이 생성됩니다:
- `lethe_before.csv` — 규칙 적용 전 메모리 상태
- `lethe_after.csv` — 규칙 적용 후 메모리 상태 (차폐 플래그 포함)
- `lethe_audit.csv` — 타임스탬프가 포함된 모든 규칙 적용 기록

### 3. Retrieve memories with explainability / 설명 가능한 기억 검색

```bash
python lethe_engine.py retrieve \
  --mem examples/memories.json \
  --ctx examples/context.json \
  --dsl examples/rules.lethe \
  --query "support-thread" \
  --topk 7
```

Each result includes a `why` field explaining exactly how its score was computed.

각 결과에는 점수가 어떻게 계산되었는지 설명하는 `why` 필드가 포함됩니다.

---

## Use Cases / 활용 시나리오

**Recovery Journaling / 회복기 저널링** — Shield sensitive tags, surface self-affirmation templates. 민감 태그 차폐, 자기 안심 템플릿 노출.

**Learning Retention / 학습 리텐션** — Event-based reinforcement for key concepts through spaced repetition. 이벤트 기반 강화를 통한 핵심 개념의 간격 반복 학습.

**Privacy Keeper / 프라이버시 보호** — TTL on by default; users explicitly pin what they want to keep. TTL 기본 활성화, 사용자가 유지할 항목을 명시적으로 고정.

**AI Companion Memory / AI 동반자 기억** — Long-term conversational agents that forget gracefully, not abruptly. 갑작스럽지 않고 자연스럽게 망각하는 장기 대화형 에이전트.

---

## Documentation / 문서

| Document | Description |
|----------|-------------|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Q/K/V emotional attention architecture + lightweight control alternatives |
| [`docs/DSL_SPEC.md`](docs/DSL_SPEC.md) | Full Lethe & Mnemosyne language specification |
| [`docs/DESIGN_PHILOSOPHY.md`](docs/DESIGN_PHILOSOPHY.md) | C++ memory control philosophy meets Python accessibility |
| [`docs/PAPER_KR.md`](docs/PAPER_KR.md) | 한국어 논문 전문 (Korean full paper) |

---

## Project Structure / 프로젝트 구조

```
Lethe-Mnemosyne/
├── README.md                  # This file
├── lethe_engine.py            # Core engine (single file, zero dependencies)
├── demo.py                    # Interactive demo
├── examples/
│   ├── rules.lethe            # DSL rule file
│   ├── memories.json          # Sample memory data
│   └── context.json           # Session context
├── docs/
│   ├── ARCHITECTURE.md        # Theoretical foundation + Q/K/V architecture
│   ├── DSL_SPEC.md            # Language specification (Lethe + Mnemosyne)
│   ├── DESIGN_PHILOSOPHY.md   # Design rationale
│   └── PAPER_KR.md            # 한국어 논문
├── LICENSE-ACADEMIC.md
└── LICENSE-COMMERCIAL.md
```

---

## Research Roadmap / 연구 로드맵

This project contains material for **4 distinct papers**, each targeting a different community. Below is the strategy, recommended venues, and timeline.

이 프로젝트는 **4편의 독립 논문** 소재를 포함하며, 각각 다른 커뮤니티를 타겟으로 합니다.

---

### Paper 1: Framework Paper (가장 빠르게 제출 가능 / Fastest to submit)

**Title (working):** *"Lethe: A Lightweight DSL for Explainable Memory Governance in AI Agents"*

**Focus:** DSL design + engine implementation + audit trail + safety guardrails. This is the most "complete" paper — working code, DSL examples, audit logs, and use cases already exist.

**핵심:** DSL 설계 + 엔진 구현 + 감사 추적 + 안전 가드레일. 작동하는 코드, DSL 예제, 감사 로그, 활용 시나리오가 이미 존재하므로 가장 빠르게 제출 가능.

**What's needed / 필요 사항:**
- [ ] Quantitative experiment: compare decay functions (exponential vs power_law vs tanh) on synthetic memory datasets
- [ ] Baseline comparison: Lethe vs naive TTL vs full retention vs MemGPT-style tiered memory
- [ ] Ablation study: audit trail completeness, shield effectiveness

**Target venues / 추천 학회:**

| Venue | Why | Deadline | Tier |
|-------|-----|----------|------|
| **ICLR 2026 — MemAgents Workshop** | "Memory for LLM-Based Agentic Systems" — 이 프로젝트를 위해 존재하는 워크숍. 에이전트 메모리의 설계·검색·망각·감사를 정확히 다룸 | TBD (ICLR 2026) | Workshop |
| **AAAI-26 W51** | "How Can We Trust and Control Agentic AI?" — XAI 오딧 트레일 각도로 제출 | Passed (Jan 2026) → AAAI-27 타겟 | Workshop |
| **AAMAS 2026/2027** | Autonomous Agents — DSL 기반 에이전트 메모리 제어 시스템 | ~Oct annually | Main/Workshop |
| **EMNLP 2026** | NLP 시스템 논문 트랙 — 대화형 에이전트 메모리 관리 도구 | ~Jun 2026 | Main |

---

### Paper 2: Architecture Paper (이론적 기여 / Theoretical contribution)

**Title (working):** *"Memorial: Emotion-Guided Attention for Selective Memory in Transformers"*

**Focus:** Q/K/V reinterpretation through emotional context. Q as affective intent vector, K as emotionally-filtered memory slots, V as adaptive response strategy. Includes the decay formula `W(t) = a(E) + [E × R] × exp(-λ(E) × t / I)` and reward design `R = αE + βC + γS`.

**핵심:** 트랜스포머 Q/K/V를 감정 맥락으로 재해석하는 아키텍처 제안. 감쇠 공식과 보상 설계를 포함하는 이론 논문.

**What's needed / 필요 사항:**
- [ ] Implement Q/K/V emotional attention on a small transformer (proof of concept)
- [ ] Compare against standard attention on emotion-tagged dialogue datasets
- [ ] Ablation: emotion-weighted vs uniform attention on memory retention tasks

**Target venues / 추천 학회:**

| Venue | Why | Deadline | Tier |
|-------|-----|----------|------|
| **ACII 2026** | Affective Computing flagship. "Explainability and Transparency in Affective Computing"이 명시적 토픽. IEEE Xplore 수록 | **Mar 27, 2026** (Main), May 30 (Workshop) | Top (Affective) |
| **NeurIPS 2026** | AI Safety / Alignment 트랙 — 감정 기반 메모리 거버넌스 | ~May 2026 | Top |
| **ICLR 2027** | Representation Learning — 감정 임베딩 기반 어텐션 변형 | ~Oct 2026 | Top |

---

### Paper 3: Lightweight Control Paper (RL 대안 / RL-free alternatives)

**Title (working):** *"Beyond Reinforcement Learning: Lightweight Control for Emotional Memory Modulation"*

**Focus:** Systematic comparison of RL-free alternatives for Q/K/V modulation — Multi-Armed Bandits (UCB, Thompson Sampling) for Q, Associative Memory + Sparse Attention for K, Mixture-of-Experts for V. The argument: emotional memory control doesn't need heavy RL; lightweight methods achieve comparable results with better interpretability and lower compute.

**핵심:** Q/K/V 조절을 위한 RL 없는 경량 대안들의 체계적 비교. MAB, 연관기억, MoE 등이 RL과 비교하여 해석 가능성과 연산 효율에서 이점을 가진다는 주장.

**What's needed / 필요 사항:**
- [ ] Implement at least 3 lightweight control methods (MAB for Q, Sparse Attention for K, MoE for V)
- [ ] Benchmark against PPO/DQN-based memory controller
- [ ] Measure: compute cost, interpretability (human eval), memory quality (retention + forgetting accuracy)

**Target venues / 추천 학회:**

| Venue | Why | Deadline | Tier |
|-------|-----|----------|------|
| **ACII 2026 Workshop** | Affective Computing + lightweight systems | **May 30, 2026** | Workshop |
| **AAMAS 2027** | Multi-agent memory efficiency | ~Oct 2026 | Main |
| **AAAI 2027** | AI Alignment 트랙 — 해석 가능한 메모리 제어 | ~Aug 2026 | Top |

---

### Paper 4: XAI / Compliance Paper (규제 적합성 / Regulatory alignment)

**Title (working):** *"Explainable Forgetting: Audit Trails for Memory Governance in AI Systems"*

**Focus:** The audit trail as an XAI mechanism. Every memory decision (forget, shield, reinforce, expire) is logged with full provenance. Connects to GDPR Article 17 (right to erasure), EU AI Act transparency requirements, and emerging AI governance frameworks.

**핵심:** 오딧 트레일을 XAI 메커니즘으로 활용. 모든 메모리 결정이 완전한 출처와 함께 기록됨. GDPR 17조(삭제권), EU AI Act 투명성 요건과의 연결.

**What's needed / 필요 사항:**
- [ ] Formal compliance mapping: Lethe audit fields → GDPR/EU AI Act requirements
- [ ] Case study: deploy Lethe in a simulated therapeutic chatbot, show audit trail satisfies regulatory checklist
- [ ] Expert evaluation: have compliance/legal reviewers assess the audit log

**Target venues / 추천 학회:**

| Venue | Why | Deadline | Tier |
|-------|-----|----------|------|
| **XAI 2026** | World Conference on Explainable AI — 정확한 타겟 | TBD | Main |
| **FAccT 2027** | Fairness, Accountability, Transparency — AI 거버넌스 | ~Jan 2027 | Top |
| **CHI 2027** | W64-style workshop: "Trust in Evolving AI Systems" — 감사 가능한 AI 메모리의 HCI 관점 | ~Sep 2026 | Top (HCI) |
| **AAAI 2027 AI Alignment** | 설명 가능한 망각의 안전성 | ~Aug 2026 | Top |

---

### Recommended Submission Timeline / 추천 제출 일정

```
2026
├── Mar 27  ─── ACII 2026 Main Track (Paper 2: Architecture) ⚡ SOON
├── May 30  ─── ACII 2026 Workshop (Paper 3: Lightweight Control)
├── Jun     ─── EMNLP 2026 (Paper 1: Framework)
├── Aug     ─── AAAI 2027 submission (Paper 1 or 4)
├── Sep     ─── CHI 2027 submission (Paper 4: XAI)
├── Oct     ─── AAMAS 2027 (Paper 1: Framework)
│           ─── ICLR 2027 (Paper 2: Architecture)
│
2027
├── Jan     ─── FAccT 2027 (Paper 4: XAI/Compliance)
├── TBD     ─── ICLR 2027 MemAgents Workshop (Paper 1: Framework)
└── TBD     ─── XAI 2026/2027 (Paper 4: XAI)
```

> **Priority recommendation / 우선순위 추천:**
> Paper 1 (Framework) first — it's 80% done. Then Paper 4 (XAI) — the audit trail is already built, just needs regulatory framing. Papers 2 and 3 require implementation work but have the highest ceiling.

> **우선순위:** Paper 1 (프레임워크)을 먼저 — 80% 완성 상태. 그 다음 Paper 4 (XAI) — 오딧 트레일이 이미 구현됨, 규제 프레이밍만 추가하면 됨. Paper 2, 3은 구현 작업이 필요하지만 천장이 가장 높음.

---

## Engineering Roadmap / 엔지니어링 로드맵

- [ ] Formal grammar (Lark/ANTLR) for DSL validation — eliminates regex fragility
- [ ] Sentence-level semantic scoring (BM25 / lightweight embeddings) — replaces TF-IDF
- [ ] LangChain / LlamaIndex plugin — 5-minute integration for existing agent frameworks
- [ ] Emotion labeling pipeline — automatic tagging via sentiment classifier
- [ ] Interactive audit dashboard — visualize memory lifecycle and rule applications
- [ ] Q/K/V emotional attention prototype — implement Memorial architecture on small transformer

---

## Citation / 인용

If you use Lethe/Mnemosyne in research, please cite:

```bibtex
@misc{jung2025lethe,
  author       = {Wonjun Jung},
  title        = {Lethe \& Mnemosyne: A Lightweight Framework for Emotional Memory Governance},
  year         = {2025},
  howpublished = {GitHub},
  url          = {https://github.com/jwj-joon/Lethe-Mnemosyne}
}
```

---

## License / 라이선스

- **Academic & Nonprofit Use**: Free — see [LICENSE-ACADEMIC](LICENSE-ACADEMIC.md)
- **Commercial Use**: Requires a paid license — see [LICENSE-COMMERCIAL](LICENSE-COMMERCIAL.md)

> Contact / 문의: dnjswns11228@gmail.com

---

## Acknowledgments / 감사의 말

Named after the rivers of Greek mythology:
- **Lethe (Λήθη)** — the river of forgetting
- **Mnemosyne (Μνημοσύνη)** — the goddess of memory

그리스 신화의 강에서 이름을 따왔습니다:
- **레테 (Λήθη)** — 망각의 강
- **므네모시네 (Μνημοσύνη)** — 기억의 여신

*This project started from a simple question: what if forgetting wasn't a bug, but the most important feature an AI memory system could have?*

*이 프로젝트는 단순한 질문에서 시작되었습니다: 망각이 버그가 아니라, AI 메모리 시스템이 가질 수 있는 가장 중요한 기능이라면?*
