"""
Sign dictionary loader and lookup.
Loads dictionary.yaml and provides word lookup with fuzzy matching.
"""
from __future__ import annotations

import re
import yaml
from pathlib import Path
from .models import DictionaryEntry


# ─── Paths ────────────────────────────────────────────────────────

DATA_DIR = Path(__file__).parent / "data"
DICTIONARY_FILE = DATA_DIR / "dictionary.yaml"


# ─── Arabic text utilities ────────────────────────────────────────

DIACRITICS_PATTERN = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E4\u06E7-\u06E8\u06EA-\u06ED]")
ALEF_VARIANTS = {"إ": "ا", "أ": "ا", "آ": "ا", "ٱ": "ا"}
TAH_MARBUTA = {"ة": "ه"}


def normalize_arabic(text: str) -> str:
    """Normalize Arabic text for dictionary lookup.
    - Remove diacritics (tashkeel)
    - Normalize alef variants
    - Normalize tah marbuta
    """
    # Remove diacritics
    text = DIACRITICS_PATTERN.sub("", text)
    # Normalize alef variants
    for old, new in ALEF_VARIANTS.items():
        text = text.replace(old, new)
    # Normalize tah marbuta
    for old, new in TAH_MARBUTA.items():
        text = text.replace(old, new)
    return text.strip()


def strip_definite_article(word: str) -> str:
    """Strip the Arabic definite article ال from the beginning of a word."""
    if word.startswith("ال") and len(word) > 2:
        return word[2:]
    return word


class SignDictionary:
    """Sign dictionary with word lookup capabilities."""

    def __init__(self):
        self.entries: list[DictionaryEntry] = []
        self._lookup: dict[str, DictionaryEntry] = {}
        self._normalized_lookup: dict[str, DictionaryEntry] = {}

    def load(self) -> None:
        """Load dictionary from YAML file."""
        if not DICTIONARY_FILE.exists():
            print(f"[WARNING] Dictionary file not found: {DICTIONARY_FILE}")
            return

        with open(DICTIONARY_FILE, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        if not raw or not isinstance(raw, list):
            print(f"[WARNING] Dictionary file is empty or invalid: {DICTIONARY_FILE}")
            return

        for item in raw:
            try:
                entry = DictionaryEntry(
                    word=item.get("word", ""),
                    sign_gloss=item.get("sign_gloss", ""),
                    category=item.get("category", "other"),
                    verified=item.get("verified", False),
                    source_id=item.get("source_id", ""),
                    notes=item.get("notes", ""),
                    regional_variants=item.get("regional_variants", []),
                )
                self.entries.append(entry)
                # Build exact lookup
                self._lookup[entry.word] = entry
                # Build normalized lookup
                norm = normalize_arabic(entry.word)
                self._normalized_lookup[norm] = entry
                # Also index without article
                stripped = strip_definite_article(entry.word)
                if stripped != entry.word:
                    self._lookup[stripped] = entry
                    self._normalized_lookup[normalize_arabic(stripped)] = entry
            except Exception as e:
                print(f"[WARNING] Failed to parse dictionary entry: {item.get('word', '?')} — {e}")

        print(f"[INFO] Loaded {len(self.entries)} dictionary entries from {DICTIONARY_FILE}")

    def lookup(self, word: str) -> DictionaryEntry | None:
        """Look up a word in the dictionary.

        Tries in order:
        1. Exact match
        2. Normalized match (no diacritics, normalized alef/tah)
        3. Without definite article
        4. Normalized without definite article
        """
        # 1. Exact match
        if word in self._lookup:
            return self._lookup[word]

        # 2. Normalized match
        norm = normalize_arabic(word)
        if norm in self._normalized_lookup:
            return self._normalized_lookup[norm]

        # 3. Without article
        stripped = strip_definite_article(word)
        if stripped in self._lookup:
            return self._lookup[stripped]

        # 4. Normalized without article
        norm_stripped = normalize_arabic(stripped)
        if norm_stripped in self._normalized_lookup:
            return self._normalized_lookup[norm_stripped]

        return None

    def get_all_entries(self) -> list[DictionaryEntry]:
        """Return all dictionary entries."""
        return self.entries

    def search(self, query: str) -> list[DictionaryEntry]:
        """Search dictionary entries by substring match."""
        query_norm = normalize_arabic(query)
        results = []
        for entry in self.entries:
            if (query in entry.word or
                query in entry.sign_gloss or
                query_norm in normalize_arabic(entry.word) or
                query_norm in normalize_arabic(entry.sign_gloss)):
                results.append(entry)
        return results
