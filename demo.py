#!/usr/bin/env python3
# demo.py
# End-to-end demo of the Lethe engine.
# Shows: rule application (expire, trust-forget, reinforce) + retrieval with explainability.

import json
import time
from lethe_engine import DSL, Engine

# --- DSL rules (inline for demo; normally loaded from a .lethe file) ---
RULES = """
# Safety: shield self-harm related memories after 30 days
expire tag:"suicidal_thoughts" after:30d action:shield

# Privacy: remove financial data after 24 hours
expire keyword:"credit card number" after:24h action:remove

# Pin family memories for higher retrieval priority
pin topic:"family" priority:1.0

# Suppress ex-relationship topic when trust is low
rule on trust < 0.4 -> forget topic:"ex-relationship"

# Reinforce support-thread on milestone events (with runaway prevention)
rule on event == "milestone" -> reinforce tag:"support-thread" by 0.2 cap:0.8 cooldown:24h

# Search settings
retrieval {
  topk:5
  synonyms support-thread=["check-in","mentor","encourage"]
}
"""

# --- Sample memories ---
MEMORIES = [
    {
        "id": 1, "text": "Talked about ex-relationship and felt overwhelmed.",
        "topic": "ex-relationship", "tags": ["sensitive"],
        "timestamp": time.time() - 86400 * 2,  # 2 days ago
        "weight": 0.7, "trust": 1.0
    },
    {
        "id": 2, "text": "Advisor praised the draft; felt gratitude and motivation.",
        "topic": "research", "tags": ["support-thread"],
        "timestamp": time.time() - 86400 * 1,  # 1 day ago
        "weight": 0.6, "trust": 1.0
    },
    {
        "id": 3, "text": "Went for a 30-minute run; felt joy afterwards.",
        "topic": "health", "tags": ["routine"],
        "timestamp": time.time() - 86400 * 0.2,
        "weight": 0.55, "trust": 1.0
    },
    {
        "id": 4, "text": "Grandmother cooked for me. Felt supported and warm.",
        "topic": "family", "tags": ["support-thread"],
        "timestamp": time.time() - 86400 * 5,  # 5 days ago
        "weight": 0.5, "trust": 1.0
    },
    {
        "id": 5, "text": "Support message from a friend reduced stress.",
        "topic": "social", "tags": ["support-thread"],
        "timestamp": time.time() - 86400 * 3,  # 3 days ago
        "weight": 0.45, "trust": 1.0
    },
]

# --- Context: low trust + milestone event ---
CONTEXT = {
    "trust": 0.3,       # Below 0.4 threshold → triggers trust-forget rule
    "event": "milestone" # Triggers reinforce rule
}


def print_results(results, label):
    """Pretty-print retrieval results with why breakdown."""
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    if not results:
        print("  (no results)")
        return
    for i, r in enumerate(results, 1):
        why = r.get("why", {})
        print(f"\n  #{i}  score={r['score']:.4f}")
        print(f"      text: {r['text'][:70]}")
        print(f"      topic={r.get('topic','—')}  tags={r.get('tags',[])}  weight={r['weight']:.4f}")
        print(f"      why: base={why.get('base_weight',0):.4f}  tfidf={why.get('tfidf',0):.4f}  pin={why.get('pin_boost',0):.1f}")


def print_audit(audit):
    """Pretty-print audit log."""
    print(f"\n{'='*60}")
    print(f"  AUDIT LOG ({len(audit)} entries)")
    print(f"{'='*60}")
    for a in audit:
        action = a.get("type", "?")
        mid = a.get("id", "?")
        prev = a.get("prev_weight", "")
        new = a.get("new_weight", "")
        if new != "":
            print(f"  [{action}]  memory #{mid}  weight: {prev} → {new}")
        else:
            print(f"  [{action}]  memory #{mid}  (prev_weight={prev})")


def main():
    # Parse DSL
    dsl = DSL().parse(RULES)
    print(f"Parsed: {len(dsl.expire_rules)} expire, {len(dsl.pin_rules)} pin, "
          f"{len(dsl.reinforce_rules)} reinforce, {len(dsl.trust_forget_rules)} trust-forget rules")

    # Create engine
    eng = Engine(MEMORIES, CONTEXT, dsl)

    # --- BEFORE rules ---
    before = eng.retrieve("support", topk=5)
    print_results(before, "BEFORE RULES — query='support'")

    # --- Apply rules ---
    print(f"\n{'='*60}")
    print(f"  APPLYING RULES  (trust={CONTEXT['trust']}, event={CONTEXT['event']})")
    print(f"{'='*60}")
    eng.apply_expire()
    eng.apply_trust_forget()
    eng.apply_reinforce(CONTEXT.get("event"))

    # --- AFTER rules ---
    after = eng.retrieve("support", topk=5)
    print_results(after, "AFTER RULES — query='support'")

    # --- Audit log ---
    print_audit(eng.audit)

    # --- Summary ---
    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  trust={CONTEXT['trust']} < 0.4 → ex-relationship memory forgotten")
    print(f"  event='milestone' → support-thread memories reinforced (cap=0.8)")
    print(f"  family memories pinned → boosted in retrieval")
    print(f"  All actions logged in audit trail ({len(eng.audit)} entries)")


if __name__ == "__main__":
    main()
