# Architecture: Emotion-Guided Attention for Selective Memory

# 아키텍처: 감정 기반 선택적 기억을 위한 어텐션

> *Merged from: Memorial: Nostalgia + Memorial: Lightweight Control Supplement*

---

## 1. The Problem / 문제 정의

AI memory systems preserve all information indiscriminately or rely on fixed-size buffers. Humans don't work this way — we forget based on emotional relevance, contextual recurrence, and personal meaning.

AI 메모리 시스템은 모든 정보를 무차별적으로 보존하거나 고정 크기 버퍼에 의존합니다. 인간은 이렇게 작동하지 않습니다 — 감정적 관련성, 맥락적 반복, 개인적 의미에 기반하여 망각합니다.

This document proposes an architectural framework that integrates emotional context into attention and memory modulation in transformer-based systems.

이 문서는 트랜스포머 기반 시스템의 어텐션과 메모리 조절에 감정 맥락을 통합하는 아키텍처 프레임워크를 제안합니다.

---

## 2. Core Idea: Emotion as Memory Filter / 핵심 아이디어: 감정을 메모리 필터로

Memory is not a database. It is a dynamic structure governed by **affective salience**.

기억은 데이터베이스가 아닙니다. **감정적 중요도**에 의해 지배되는 동적 구조입니다.

In this view:
- Emotions are both **triggers** and **modulators** for memory retrieval, decay, and reweighting
- Query vectors represent **affective states**
- Value vectors encode **past interactions**
- Reward functions derive from **emotional resolution, coherence, and user feedback**
- Forgetting is no longer random or fixed — it is **affectively justified**

이 관점에서:
- 감정은 기억 검색, 감쇠, 재가중치를 위한 **트리거이자 조절자**
- 쿼리 벡터는 **감정 상태**를 표현
- 값 벡터는 **과거 상호작용**을 인코딩
- 보상 함수는 **감정적 해결, 일관성, 사용자 피드백**에서 파생
- 망각은 더 이상 무작위이거나 고정적이지 않음 — **감정적으로 정당화**됨

---

## 3. Q/K/V Reinterpretation / Q/K/V 재해석

The architecture modifies the transformer's Q, K, V components to be individually controllable via emotional context.

이 아키텍처는 트랜스포머의 Q, K, V 구성요소를 감정 맥락을 통해 개별적으로 제어 가능하도록 수정합니다.

### Q (Query) — Emotional Intent Vector / 감정 의도 벡터

Standard transformer: token embedding.

**Proposed**: Emotion-based intent vector reflecting the current affective state, time context, and underlying goal. Q encodes *what the agent is feeling and seeking right now*.

**제안**: 현재 감정 상태, 시간 맥락, 근본적 목표를 반영하는 감정 기반 의도 벡터. Q는 *에이전트가 지금 무엇을 느끼고 찾고 있는지*를 인코딩합니다.

### K (Key) — Emotionally-Filtered Memory Slots / 감정 필터링된 메모리 슬롯

Standard transformer: learned representation.

**Proposed**: Past memories filtered via associative matching to emotional context and conversation flow. K determines *which memories are even considered*, based on emotional similarity to the current state.

**제안**: 감정 맥락과 대화 흐름에 대한 연관 매칭을 통해 필터링된 과거 기억. K는 현재 상태와의 감정적 유사성에 기반하여 *어떤 기억이 고려될 것인지*를 결정합니다.

### V (Value) — Adaptive Response Strategy / 적응적 응답 전략

Standard transformer: output projection.

**Proposed**: Adaptive selection of response strategy — informational, empathetic, or deflective — regulated by emotional matching and historical trust. V determines *how the agent responds* once a memory is selected.

**제안**: 감정 매칭과 역사적 신뢰에 의해 조절되는 응답 전략의 적응적 선택 — 정보 제공적, 공감적, 또는 회피적. V는 기억이 선택된 후 *에이전트가 어떻게 응답하는지*를 결정합니다.

### Summary Table / 요약 표

| Component | Standard Transformer | Lethe Reinterpretation | Control Signal |
|-----------|---------------------|----------------------|----------------|
| **Q** | Token embedding | Affective state + time + goal | Current emotion |
| **K** | Learned representation | Emotionally-filtered memory slots | Emotional similarity |
| **V** | Output projection | Adaptive response strategy | Trust + emotional match |

---

## 4. Emotion-Weighted Decay / 감정 가중 감쇠

Memory strength decays as a function of time, emotional intensity, interaction frequency, and affective category:

기억의 강도는 시간, 감정 강도, 상호작용 빈도, 감정 범주의 함수로 감쇠합니다:

```
W(t) = a(E) + [E × R] × exp(-λ(E) × t / I)
```

| Symbol | Meaning | 의미 |
|--------|---------|------|
| `W(t)` | Memory weight at time *t* | 시간 *t*에서의 기억 가중치 |
| `a(E)` | Emotion-specific memory floor | 감정별 최소 유지값 (바닥값) |
| `E` | Emotion intensity | 감정 강도 |
| `R` | Reward (resolution, trust, coherence) | 보상 (해결, 신뢰, 일관성) |
| `λ(E)` | Emotion-based decay rate | 감정별 감쇠 속도 |
| `t` | Time elapsed | 경과 시간 |
| `I` | Interaction count | 상호작용 횟수 |

**Key property**: High emotional relevance → slower decay. The floor `a(E)` ensures memories never fully vanish — even suppressed memories leave traces, which is both psychologically realistic and useful for audit.

**핵심 특성**: 높은 감정적 관련성 → 느린 감쇠. 바닥값 `a(E)`는 기억이 완전히 사라지지 않도록 보장합니다 — 억제된 기억도 흔적을 남기며, 이는 심리학적으로 현실적이고 감사에도 유용합니다.

### Decay Kernels / 감쇠 커널

Different emotions decay differently. The DSL supports configurable kernels:

감정마다 감쇠 양상이 다릅니다. DSL은 구성 가능한 커널을 지원합니다:

| Emotion | λ | Floor | Kernel | Behavior |
|---------|---|-------|--------|----------|
| Sadness | 0.35 | 0.10 | `power_law` | Fades relatively fast, low residual |
| Anxiety | 0.50 | 0.05 | `sigmoid` | Sharp initial decay, near-zero floor |
| Calm | 0.08 | 0.20 | `exponential` | Very slow decay, high retention |
| Gratitude | 0.05 | 0.20 | `tanh` | Slowest decay, highest floor |

---

## 5. Reward Design / 보상 설계

Rewards are not based on external success metrics, but on **internal coherence**:

보상은 외부 성공 지표가 아닌 **내부 일관성**에 기반합니다:

```
R = α × E + β × C + γ × S
```

| Symbol | Meaning | 의미 |
|--------|---------|------|
| `E` | Emotion intensity | 감정 강도 |
| `C` | Coherence (logical alignment) | 일관성 (논리적 정합) |
| `S` | Resolution (affective closure) | 해결 (감정적 종결) |
| `α, β, γ` | Tunable weights | 조절 가능한 가중치 |

System behavior is shaped by these internal evaluations, enabling memory pruning and reinforcement in an emotionally aligned manner.

시스템 행동은 이러한 내부 평가에 의해 형성되며, 감정적으로 정렬된 방식으로 기억의 가지치기와 강화를 가능하게 합니다.

---

## 6. Lightweight Control Alternatives / 경량 제어 대안

> *This section addresses a practical concern: RL is powerful but computationally expensive and slow to adapt in real-time. What if we don't need it?*
>
> *이 섹션은 실용적 문제를 다룹니다: RL은 강력하지만 연산 비용이 높고 실시간 적응이 느립니다. RL 없이도 가능하다면?*

### 6.1 Query Modulation (Q) / 쿼리 조절

The query vector represents emotional and intentional state. RL-free alternatives:

쿼리 벡터는 감정적·의도적 상태를 표현합니다. RL 없는 대안:

**Multi-Armed Bandits (UCB, Thompson Sampling)** — Select from a set of query strategies based on estimated emotional reward. Simple, low-overhead, and naturally balances exploration vs exploitation of different emotional framings.

**다중 슬롯 머신 (UCB, 톰슨 샘플링)** — 추정된 감정 보상에 기반하여 쿼리 전략 세트에서 선택. 단순하고 오버헤드가 낮으며, 다양한 감정 프레이밍의 탐색 대 활용을 자연스럽게 균형잡습니다.

**Gating Networks** — Use emotion vectors as inputs to a softmax-based gating layer that mixes multiple query strategies. Differentiable and trainable end-to-end.

**게이팅 네트워크** — 감정 벡터를 소프트맥스 기반 게이팅 레이어의 입력으로 사용하여 다중 쿼리 전략을 혼합. 미분 가능하고 종단간 훈련 가능.

**Hebbian Plasticity** — Strengthen query-response paths that were emotionally rewarding through associative learning. No explicit reward signal needed — just correlation.

**헤비안 가소성** — 연관 학습을 통해 감정적으로 보상된 쿼리-응답 경로를 강화. 명시적 보상 신호 불필요 — 상관관계만으로 충분.

### 6.2 Key Filtering (K) / 키 필터링

Key vectors represent memory slots. RL-free alternatives:

키 벡터는 메모리 슬롯을 표현합니다. RL 없는 대안:

**Associative Memory (Hopfield-style)** — Automatically activate memories with high emotional similarity to the current state. Content-addressable retrieval without learned policies.

**연관 기억 (홉필드 스타일)** — 현재 상태와 감정적 유사성이 높은 기억을 자동으로 활성화. 학습된 정책 없이 내용 주소 지정 검색.

**Sparse Attention with Learned Masking** — Only top-k keys with high emotional alignment are considered. Reduces computational cost while maintaining relevance.

**학습된 마스킹을 통한 희소 어텐션** — 감정 정렬이 높은 상위 k개의 키만 고려. 관련성을 유지하면서 연산 비용 절감.

**Entropy-Based Filtering** — Suppress or amplify key activations based on the uncertainty or clarity of emotional match. High-entropy (ambiguous) matches are suppressed; low-entropy (clear) matches are amplified.

**엔트로피 기반 필터링** — 감정 매칭의 불확실성 또는 명확성에 기반하여 키 활성화를 억제하거나 증폭. 고엔트로피(모호한) 매칭은 억제; 저엔트로피(명확한) 매칭은 증폭.

### 6.3 Value Selection (V) / 값 선택

Value vectors define response strategy. RL-free alternatives:

값 벡터는 응답 전략을 정의합니다. RL 없는 대안:

**Mixture-of-Experts (MoE)** — Multiple output modules (empathy, information, reflection), weighted by emotional relevance. Each expert specializes in a response style.

**전문가 혼합 (MoE)** — 감정 관련성에 의해 가중치가 부여된 다중 출력 모듈 (공감, 정보, 성찰). 각 전문가가 응답 스타일에 특화.

**Utility-Based Decision Layer** — Simple rules to pick responses with highest emotional utility. Interpretable and fast.

**효용 기반 결정 레이어** — 가장 높은 감정 효용을 가진 응답을 선택하는 간단한 규칙. 해석 가능하고 빠름.

**Emotion-Embedding Matching** — Match current emotional vector with stylistic templates to select tone and form. No training required — works from pre-defined emotional profiles.

**감정 임베딩 매칭** — 현재 감정 벡터를 스타일 템플릿과 매칭하여 톤과 형식을 선택. 훈련 불필요 — 사전 정의된 감정 프로파일로 작동.

### 6.4 Integrated Lightweight Framework / 통합 경량 프레임워크

Combining the above methods into a full architecture:

위 방법들을 완전한 아키텍처로 결합:

```
Q: Gating network with emotion vector input
   → selects query strategy based on current affective state

K: Sparse key selection with associative memory
   → activates only emotionally relevant memory slots

V: Mixture-of-Experts for emotionally aligned responses
   → routes to empathy / information / reflection expert
```

This system is **modular** (swap any component independently), **explainable** (each decision has a traceable cause), and **adaptable** to real-time interaction constraints.

이 시스템은 **모듈식** (어떤 구성요소든 독립적으로 교체 가능), **설명 가능** (각 결정에 추적 가능한 원인이 있음), 실시간 상호작용 제약에 **적응 가능**합니다.

### 6.5 Comparison: RL vs Lightweight / RL 대 경량 비교

| Dimension | RL-based | Lightweight |
|-----------|----------|-------------|
| Compute cost | High (policy gradient, replay buffer) | Low (forward pass only) |
| Adaptation speed | Slow (needs many episodes) | Fast (immediate rule application) |
| Interpretability | Low (black-box policy) | High (explicit gating, rules, experts) |
| Optimality ceiling | Higher (learns nuanced policies) | Lower (bounded by pre-defined strategies) |
| Deployment | GPU-heavy, server-side | Edge-viable, mobile-friendly |

**Recommendation**: Start with lightweight control for initial deployment. Hybridize with RL fine-tuning for long-term personalization once sufficient interaction data is collected.

**추천**: 초기 배포는 경량 제어로 시작. 충분한 상호작용 데이터가 수집된 후 장기 개인화를 위해 RL 파인튜닝과 하이브리드화.

---

## 7. Applications / 응용 분야

- **Digital therapeutic companions** — Emotion-aware memory enables agents to remember what matters to the user, forget what should fade, and respond with appropriate emotional tone
- **Emotionally-aware education systems** — Reinforce concepts tied to positive learning experiences; let frustrating associations decay naturally
- **Long-term trust-building human-AI interfaces** — Memory governance builds trust through transparency: the user knows what the agent remembers, forgets, and why
- **Mobile or edge AI** — Lightweight control makes emotional memory viable on resource-constrained devices
- **Transparent AI models** — Every memory decision is auditable, supporting regulatory compliance

- **디지털 치료 동반자** — 감정 인식 메모리로 사용자에게 중요한 것을 기억하고, 사라져야 할 것을 잊고, 적절한 감정 톤으로 응답
- **감정 인식 교육 시스템** — 긍정적 학습 경험에 연결된 개념을 강화; 좌절감 연관은 자연스럽게 감쇠
- **장기 신뢰 구축 인간-AI 인터페이스** — 투명성을 통한 신뢰 구축: 에이전트가 무엇을 기억하고 잊는지, 왜 그런지를 사용자가 인지
- **모바일 또는 에지 AI** — 경량 제어로 자원 제한 장치에서 감정 메모리 구현 가능
- **투명한 AI 모델** — 모든 메모리 결정이 감사 가능, 규제 준수 지원

---

## 8. Open Questions / 미해결 질문

These are the research gaps that the proposed papers (see README) aim to address:

이것들은 제안된 논문들(README 참고)이 다루고자 하는 연구 공백입니다:

1. **Empirical validation**: How does emotion-weighted decay compare to uniform decay on real dialogue datasets? Does it improve user satisfaction, trust, or safety?
2. **Optimal kernel selection**: Which decay function (exponential, power_law, sigmoid, tanh) works best for which emotion category? Is this universal or user-dependent?
3. **Lightweight vs RL ceiling**: At what point does the lightweight approach plateau, and when does RL fine-tuning become worth the compute cost?
4. **Cross-cultural validity**: Do the decay parameters transfer across cultures, or do they need per-culture calibration?
5. **Formal safety guarantees**: Can we prove that the shield/expire rules in the DSL prevent re-exposure of sensitive memories under all rule combinations?

---

## 9. Relationship to Lethe Engine / Lethe 엔진과의 관계

The current `lethe_engine.py` implements a **rule-based subset** of this architecture:

현재 `lethe_engine.py`는 이 아키텍처의 **규칙 기반 부분집합**을 구현합니다:

| Architecture Component | Current Implementation | Gap |
|----------------------|----------------------|-----|
| Emotion-weighted decay | DSL emotion kernels (λ, floor) | Not yet integrated into engine scoring |
| Q modulation | Context-based query (trust, event) | No learned query strategy |
| K filtering | TF-IDF + synonym expansion + shield | No associative memory or sparse attention |
| V selection | Single retrieval mode | No MoE or response strategy routing |
| Reward design | Rule-based reinforce/forget | No learned reward function |
| Audit trail | Full CSV audit logging | ✅ Complete |

The path from current implementation to full architecture is incremental — each component can be upgraded independently without breaking the DSL or audit system.

현재 구현에서 전체 아키텍처로의 경로는 점진적입니다 — 각 구성요소가 DSL이나 감사 시스템을 깨뜨리지 않고 독립적으로 업그레이드될 수 있습니다.
