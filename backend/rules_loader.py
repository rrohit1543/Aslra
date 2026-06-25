"""
YAML data loaders for rules, sources, and dictionary.
Loads data at import time and provides lookup functions.
"""
from __future__ import annotations

import yaml
from pathlib import Path
from .models import GrammarRule, EvidenceEntry, RuleExample


# ─── Paths ────────────────────────────────────────────────────────

DATA_DIR = Path(__file__).parent / "data"
RULES_FILE = DATA_DIR / "rules.yaml"


def load_rules() -> list[GrammarRule]:
    """Load grammar rules from rules.yaml and return as list of GrammarRule models."""
    if not RULES_FILE.exists():
        print(f"[WARNING] Rules file not found: {RULES_FILE}")
        return []

    with open(RULES_FILE, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if not raw or not isinstance(raw, list):
        print(f"[WARNING] Rules file is empty or invalid: {RULES_FILE}")
        return []

    rules = []
    for item in raw:
        try:
            # Convert nested dicts to proper models
            evidence = []
            for e in item.get("evidence", []):
                evidence.append(EvidenceEntry(**e))

            examples = []
            for ex in item.get("examples", []):
                examples.append(RuleExample(**ex))

            rule = GrammarRule(
                id=item.get("id", ""),
                name=item.get("name", ""),
                category=item.get("category", ""),
                description=item.get("description", ""),
                trigger=item.get("trigger", ""),
                action=item.get("action", ""),
                evidence_type=item.get("evidence_type", "speculative"),
                evidence=evidence,
                confidence=item.get("confidence", "low"),
                priority=item.get("priority", 50),
                examples=examples,
                notes=item.get("notes", ""),
                requires_expert_review=item.get("requires_expert_review", True),
                review_questions=item.get("review_questions", []),
            )
            rules.append(rule)
        except Exception as e:
            print(f"[WARNING] Failed to parse rule: {item.get('id', '?')} — {e}")

    # Sort by priority (lower = first)
    rules.sort(key=lambda r: r.priority)
    print(f"[INFO] Loaded {len(rules)} rules from {RULES_FILE}")
    return rules


def get_rule_by_id(rules: list[GrammarRule], rule_id: str) -> GrammarRule | None:
    """Look up a rule by its ID."""
    for rule in rules:
        if rule.id == rule_id:
            return rule
    return None


def get_rules_by_category(rules: list[GrammarRule], category: str) -> list[GrammarRule]:
    """Get all rules in a given category."""
    return [r for r in rules if r.category == category]
