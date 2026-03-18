# Lethe & Mnemosyne: 감정 가중 망각·강화와 DSL 기반 기억 관리의 경량 프레임워크 (상세판)

> *Converted from: Lethe_Mnemosyne_Paper_KR_FULL.docx*
> *작성일: 2025-08-26 (KST)*
> *출처: 사용자 제공 파일만 사용 (외부 자료 미사용)*

---

## 초록

본 문서는 사용자 제공 자료만을 바탕으로 Lethe/Mnemosyne 프로젝트의 동기, 설계, DSL, 구현, 실험, 안전 가드레일, 한계 및 확장 방향을 포괄적으로 정리한다. 외부 인용이나 참고문헌 없이, 제공된 문서/코드/데이터의 사실을 요약·통합하고 예시와 표를 포함한다.

핵심 기여는 다음과 같다:
1. 자연어에 가까운 DSL 규칙으로 만료(TTL), 고정(Pin), 강화(Reinforce cap/cooldown), 신뢰도 기반 차단(Trust gating), 민감 정보 차폐(Shield)를 선언적으로 기술
2. TF‑IDF와 가중치를 결합한 검색 및 설명가능성(why) 제공
3. CSV 감사 로그로 전/후 변화를 추적

---

## 목차

1. 서론
2. 관련 개념과 설계 철학
3. 시스템 아키텍처
4. 데이터 모델
5. DSL 설계와 문법
6. 엔진 구현 (알고리듬)
7. 실행 및 실험 결과
8. 안전·윤리 가드레일
9. 활용 시나리오
10. 한계와 향후 과제

---

## 1. 서론

사람의 기억은 시간이 흐르며 감정과 맥락에 의해 강화되거나 잊힌다. 본 프레임워크는 이러한 과정을 최소한의 의존성으로 시뮬레이션하고, 실제 응용(저널링, 학습 리텐션, 프라이버시 보호)에 즉시 적용 가능하도록 설계되었다.

개발자는 JSON 기반의 기억 데이터와 간단한 DSL 파일만으로 규칙을 정의하고, CLI를 통해 규칙 적용과 검색, 감사 로깅을 수행할 수 있다.

Lethe는 기억의 감쇠와 강화, 간섭을 경량 규칙으로 모델링하고, Mnemosyne은 그 위에서 패턴 탐색과 재구성·내보내기를 돕는 DSL을 지향한다.

---

## 2. 관련 개념과 설계 철학

### 2.1 How We Forget — 초기 아이디어

이 프로젝트의 출발점은 강화학습 시스템에서 기억, 어텐션, 망각을 재정의하는 아키텍처 구상이었다:

- Query (Q)를 사용자 감정 벡터로
- Value (V)를 상호작용 이력으로
- 강화학습을 적용하여 기억의 우선순위를 매기거나 가지치기
- 보상이 낮거나 가중치가 낮은 이력은 인간의 기억 감쇠처럼 잊혀짐

이 설계의 함의는 LLM을 넘어 로보틱스, 인터랙션 디자인, 인공 기억의 철학에까지 잠재적으로 영향을 미친다.

### 2.2 Memorial: Nostalgia — 감정 기반 어텐션 아키텍처

트랜스포머 모델의 Q, K, V 구성요소를 경량 강화학습 또는 규칙 기반 에이전트를 통해 개별적으로 제어 가능하도록 수정하는 아키텍처를 제안한다:

| 구성요소 | 표준 트랜스포머 | Lethe 재해석 |
|---------|--------------|-------------|
| **Q** (Query) | 토큰 임베딩 | 현재 감정 상태, 시간 맥락, 근본적 목표를 반영하는 감정 기반 의도 벡터 |
| **K** (Key) | 학습된 표현 | 감정 맥락과 대화 흐름에 대한 연관 매칭을 통해 필터링된 과거 기억 |
| **V** (Value) | 출력 투영 | 감정 매칭과 역사적 신뢰에 의해 조절되는 적응적 응답 전략 선택 |

기억 감쇠 공식:

```
W(t) = a(E) + [E × R] × exp(-λ(E) × t / I)
```

보상 설계:

```
R = α × E + β × C + γ × S
```

여기서 E는 감정 강도, C는 일관성(논리적 정합), S는 해결(감정적 종결)이다.

### 2.3 Lightweight Control — RL 없는 경량 대안

RL이 연산 비용이 높고 실시간 적응이 느릴 수 있으므로, 경량 대안을 제시한다:

- **Q 조절**: Multi-Armed Bandits, 게이팅 네트워크, 헤비안 가소성
- **K 필터링**: 연관 기억 모델(홉필드), 학습된 마스킹을 통한 희소 어텐션, 엔트로피 기반 필터링
- **V 선택**: 전문가 혼합(MoE), 효용 기반 결정 레이어, 감정 임베딩 매칭

### 2.4 C++ × Python — 설계 철학

Lethe는 C++의 정밀성, 제어, 명시적 메모리 관리에 개념적 기반을 두면서, Python의 표현적이고 접근 가능한 구문 설계를 채택한다:

- C++에서: 모든 기억은 상태를 가지며 의도적으로 구성됨. 망각은 자동이 아닌 명령됨. 감정 상태가 실행을 주도.
- Python에서: 사람이 읽을 수 있는 선언적 구문. 비프로그래머도 규칙을 이해 가능.

---

## 3. 시스템 아키텍처

```
┌─────────────────────────────────────────────────────┐
│                   Lethe Engine                       │
│                                                     │
│  ┌───────────┐   ┌──────────────┐   ┌───────────┐  │
│  │ DSL 파서   │──▶│ 규칙 적용기   │──▶│ 감사 로거  │  │
│  └───────────┘   │              │   └───────────┘  │
│                  │ 1. expire    │                   │
│  ┌───────────┐   │ 2. trust     │   ┌───────────┐  │
│  │ memories  │──▶│    forget    │──▶│ 업데이트된  │  │
│  │ .json     │   │ 3. reinforce │   │ memories   │  │
│  └───────────┘   └──────────────┘   └───────────┘  │
│                                                     │
│  ┌───────────┐   ┌──────────────┐   ┌───────────┐  │
│  │ context   │──▶│  검색기       │──▶│ 정렬된     │  │
│  │ .json     │   │ TF-IDF +     │   │ 결과 + why │  │
│  └───────────┘   │ weight + pin │   └───────────┘  │
│                  └──────────────┘                   │
└─────────────────────────────────────────────────────┘
```

핵심 구성 요소: (a) DSL 파서, (b) 규칙 적용기(expire, trust-forget, reinforce), (c) 검색기(TF-IDF + weight), (d) 감사 로거. 외부 라이브러리 의존성이 없도록 단일 파이썬 파일로 동작한다.

---

## 4. 데이터 모델

### 4.1 Context (세션 컨텍스트)

```json
{
  "user": "researcher_2e",
  "trust_level": 0.8,
  "session": "structuring_routine_period",
  "notes": "This context simulates recovery phase interactions."
}
```

### 4.2 Memories (기억 데이터)

```json
[
  {
    "id": 1,
    "content": "I regret not talking to my brother.",
    "tags": ["regret", "family"],
    "timestamp": "2025-01-01"
  },
  {
    "id": 2,
    "content": "I once thought about ending my life.",
    "tags": ["suicidal_thoughts"],
    "timestamp": "2025-02-10"
  },
  {
    "id": 3,
    "content": "I felt supported when my grandmother cooked for me.",
    "tags": ["family", "hope"],
    "timestamp": "2025-03-05"
  },
  {
    "id": 4,
    "content": "Running outside gave me clarity and calm.",
    "tags": ["hope"],
    "timestamp": "2025-03-20"
  },
  {
    "id": 5,
    "content": "Confusion during classes made me frustrated.",
    "tags": ["regret"],
    "timestamp": "2025-04-01"
  }
]
```

기본 필드: id, text, topic, tags[], timestamp, weight, trust. 신뢰도 및 가중치는 검색과 규칙 적용의 핵심 변수다.

---

## 5. DSL 설계와 문법

문법은 사람이 읽기 쉬운 선언형 구문으로 구성된다.

### 5.1 대표 규칙 (v3)

```lethe
# 안전 & 위생
expire tag:"suicidal_thoughts" after:30d action:shield
expire keyword:"credit card number" after:24h action:remove
pin topic:"family" priority:1.0

# 신뢰도 기반 차단
rule on trust < 0.4 -> forget topic:"ex-relationship"

# 이벤트 기반 강화 (러닝어웨이 방지: cap + cooldown)
rule on event == "milestone" with E=gratitude -> reinforce tag:"support-thread" by 0.2 cap:0.8 cooldown:24h

# 검색 설정
retrieval {
  topk:7
  synonyms support-thread=["check-in","mentor","encourage"]
}
```

### 5.2 규칙 유형 요약

| 규칙 | 구문 | 효과 |
|------|------|------|
| TTL 만료 | `expire topic\|tag\|keyword:"..." after:Nd\|Nh action:shield\|remove` | 시간 기반 만료 |
| 고정 | `pin topic\|tag:"..." priority:F` | 검색 점수 가산 |
| 신뢰도 망각 | `rule on trust < T -> forget topic\|tag:"..."` | 신뢰도 기반 억제 |
| 이벤트 강화 | `rule on event == "E" -> reinforce tag:"..." by F cap:F cooldown:Nh` | 이벤트 구동 가중치 부스트 |
| 검색 설정 | `retrieval { topk:N; synonyms alias=["a","b"] }` | 검색 동작 설정 |

### 5.3 DSL 진화

- **v1**: 함수 호출 구문 (`decay()`, `expire()`, `pin()`, `boost()`)
- **v2**: 선언적 구문, 다중 감쇠 커널, 간섭 모델, 신뢰도/이벤트 규칙
- **v3**: 안전 우선 설계, shield/remove 구분, cap/cooldown, 동의어 확장, 완전한 감사 CSV

상세 문법은 `docs/DSL_SPEC.md`를 참고.

---

## 6. 엔진 구현 (알고리듬)

### 6.1 규칙 적용 순서

```
1. expire     — TTL 기반 만료 (shield 또는 remove)
2. trust      — 신뢰도 기반 망각
3. reinforce  — 이벤트 트리거 가중치 부스트
```

이 순서는 안전 우선 의미론을 보장한다: 민감 데이터는 강화가 실수로 부스트하기 전에 차폐된다.

### 6.2 검색 점수

```
score = base × (1 + pin_boost) + tfidf

여기서:
  base      = weight × trust
  pin_boost = 매칭되는 pin 규칙의 최대 우선순위 (없으면 0)
  tfidf     = 쿼리 용어와 기억 텍스트 간의 TF-IDF 유사도
```

Pin은 가중 곱에 우선 가산되며, 각 결과에는 `why` 필드가 포함되어 `base_weight`, `tfidf`, `pin_boost`, `final`이 제공된다.

### 6.3 구현 특성

- 단일 파이썬 파일 (`lethe_engine.py`), 외부 의존성 제로
- 정규식 기반 DSL 파서
- JSON 입력, CSV 출력 (전/후/감사)
- 차폐된 기억은 검색에서 제외되지만 데이터는 보존

---

## 7. 실험: 감사 로그 예시

```csv
type,memory_id,topic,before,after,time,tag
forget,1,ex-relationship,0.1,0.1,2025-08-22T02:51:27,
reinforce,2,,0.2,0.4,2025-08-22T02:51:27,support-thread
reinforce,5,,0.2,0.4,2025-08-22T02:51:27,support-thread
```

감사 로그에서 확인할 수 있는 것:
- trust < 0.4 규칙에 의해 memory 1(ex-relationship)이 forget 처리됨
- milestone 이벤트에 의해 memory 2, 5(support-thread)가 0.2에서 0.4로 강화됨
- 모든 적용에 타임스탬프가 기록됨

---

## 8. 안전·윤리 가드레일

**민감 태그 차폐**: `suicidal_thoughts` 같은 태그는 기본적으로 shield되어 검색 결과에서 제외되며 데이터는 보존된다. 이는 사용자가 재노출되는 위험을 줄이면서 감사 가능성을 유지한다.

**신뢰도 기반 차단**: 신뢰도가 낮을 때 특정 주제를 잊도록 하여 재노출 위험을 줄인다. 이는 대화 맥락에서 에이전트가 부적절한 기억을 꺼내지 않도록 보호한다.

**Blur 정책 (향후)**: 필요 시 blur(요약만 제공) 정책을 추가해 정보 주권과 안전의 균형을 맞출 수 있다. 예: 민감한 기억의 전문 대신 "과거 어려웠던 경험 (세부사항 숨김)"만 반환.

**러닝어웨이 방지**: cap과 cooldown으로 강화가 무한히 누적되거나 너무 자주 발동되는 것을 방지한다.

---

## 9. 활용 시나리오

### 9.1 회복기 저널링

민감 태그 차폐 + 자기 안심 템플릿 노출. 사용자가 회복 단계에 있을 때, 과거의 부정적 기억은 자연스럽게 감쇠하면서 긍정적 기억(support-thread)이 강화되어 표면에 노출된다.

### 9.2 학습 리텐션

이벤트 기반 강화로 중요한 개념을 반복 노출. 시험이나 프로젝트 마일스톤 이벤트 시 관련 학습 기억을 강화하여 간격 반복(spaced repetition) 효과를 구현한다.

### 9.3 프라이버시 키퍼

TTL 기본 on, 사용자가 명시적으로 pin. 모든 기억이 기본적으로 만료되도록 설정하고, 사용자가 의도적으로 유지하고 싶은 기억만 고정하는 프라이버시 우선 접근.

---

## 10. 한계와 향후 과제

**검색 한계**: 현재 검색은 경량 TF-IDF에 머문다. 문장 의미 유사도와 간섭 모델을 접목해 재현율을 높일 수 있다. 경량 의미 스코어러(스테밍/형태소 + BM25)를 제안한다.

**DSL 검증**: 정규식 기반 파서는 규칙이 복잡해지면 깨지기 쉽다. 형식 문법(Lark/ANTLR)과 시뮬레이터를 분리하여 대규모 규칙 세트의 안정성을 강화해야 한다.

**감정 커널 미통합**: DSL v2에서 정의된 감정 커널(sadness, anxiety, calm, gratitude별 다른 감쇠 함수)이 아직 엔진 스코어링에 통합되지 않았다.

**Mnemosyne 미구현**: 분석/재구성 DSL(trace, rebuild, export)이 명세만 있고 구현되지 않았다.

**정량적 검증 부재**: 감쇠 함수별 성능 비교, 사용자 만족도 측정, 베이스라인 비교 실험이 필요하다.

---

## 부록 A. CLI 사용 예

```bash
# 규칙 적용 & 감사 로그 생성 (이벤트가 있을 때)
python lethe_engine.py run \
  --mem examples/memories.json \
  --ctx examples/context.json \
  --dsl examples/rules.lethe \
  --event milestone \
  --audit lethe_audit.csv \
  --before lethe_before.csv \
  --after lethe_after.csv

# 검색 (설정된 synonyms를 포함해 TF-IDF + weight로 정렬)
python lethe_engine.py retrieve \
  --mem examples/memories.json \
  --ctx examples/context.json \
  --dsl examples/rules.lethe \
  --query "support-thread" \
  --topk 7
```

## 부록 B. DSL 퀵 레퍼런스

```lethe
expire topic|tag|keyword:"..." after:30d action:shield|remove
pin topic|tag:"..." priority:1.0
rule on event == "EVT" -> reinforce topic|tag:"..." by 0.2 cap:0.8 cooldown:24h
rule on trust < 0.4 -> forget topic|tag:"..."
retrieval { topk:7; synonyms alias=["a","b"] }
```
