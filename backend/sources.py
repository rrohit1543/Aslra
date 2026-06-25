"""
Source registry loader.
Loads sources.yaml and provides lookup by ID.
"""
from __future__ import annotations

import yaml
from pathlib import Path
from .models import Source


# ─── Paths ────────────────────────────────────────────────────────

DATA_DIR = Path(__file__).parent / "data"
SOURCES_FILE = DATA_DIR / "sources.yaml"


def load_sources() -> list[Source]:
    """Load sources from sources.yaml and return as list of Source models."""
    if not SOURCES_FILE.exists():
        print(f"[WARNING] Sources file not found: {SOURCES_FILE}")
        return []

    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    if not raw or not isinstance(raw, list):
        print(f"[WARNING] Sources file is empty or invalid: {SOURCES_FILE}")
        return []

    sources = []
    for item in raw:
        try:
            source = Source(
                id=item.get("id", ""),
                title=item.get("title", ""),
                language=item.get("language", "en"),
                url=item.get("url", ""),
                acquisition_method=item.get("acquisition_method", ""),
                type=item.get("type", ""),
                credibility=item.get("credibility", "medium"),
                credibility_reason=item.get("credibility_reason", ""),
                rules_supported=[str(r) for r in item.get("rules_supported", [])],
                limitations=item.get("limitations", ""),
                year=str(item.get("year", "")),
                author=item.get("author", ""),
            )
            sources.append(source)
        except Exception as e:
            print(f"[WARNING] Failed to parse source: {item.get('id', '?')} — {e}")

    print(f"[INFO] Loaded {len(sources)} sources from {SOURCES_FILE}")
    return sources


def get_source_by_id(sources: list[Source], source_id: str) -> Source | None:
    """Look up a source by its ID."""
    for source in sources:
        if source.id == source_id:
            return source
    return None


def get_sources_for_rule(sources: list[Source], rule_id: str) -> list[Source]:
    """Get all sources that support a given rule."""
    return [s for s in sources if rule_id in s.rules_supported]
