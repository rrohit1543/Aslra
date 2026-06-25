"""
Arabic text tokenizer.
Handles normalization, diacritic removal, and word-level tokenization.
"""
from __future__ import annotations

import re
from .models import TokenInfo


# ─── Arabic Unicode ranges and patterns ───────────────────────────

# Diacritics (tashkeel) pattern
DIACRITICS_PATTERN = re.compile(
    r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E4\u06E7-\u06E8\u06EA-\u06ED]"
)

# Alef variants → unified alef
ALEF_VARIANTS = {"إ": "ا", "أ": "ا", "آ": "ا", "ٱ": "ا"}

# Tah marbuta → hah (for matching, not display)
TAH_MARBUTA_MAP = {"ة": "ه"}

# Common prefixes in Arabic
PREFIXES = {
    "سأ": {"type": "future_first_person", "base_prefix": "س"},  # will (I)
    "سن": {"type": "future_first_person_plural", "base_prefix": "س"},  # will (we)
    "ست": {"type": "future_second_person", "base_prefix": "س"},  # will (you)
    "سي": {"type": "future_third_person", "base_prefix": "س"},  # will (he)
    "س": {"type": "future", "base_prefix": "س"},
    "و": {"type": "conjunction", "base_prefix": "و"},
    "ف": {"type": "conjunction", "base_prefix": "ف"},
    "ب": {"type": "preposition", "base_prefix": "ب"},
    "ل": {"type": "preposition", "base_prefix": "ل"},
    "ك": {"type": "preposition", "base_prefix": "ك"},
}

# Common suffixes in Arabic
SUFFIXES = {
    "ات": {"type": "feminine_plural"},
    "ون": {"type": "masculine_plural"},
    "ين": {"type": "masculine_plural_oblique"},
    "ان": {"type": "dual"},
    "ة": {"type": "feminine"},
    "ها": {"type": "possessive_her"},
    "هم": {"type": "possessive_them"},
    "هن": {"type": "possessive_them_f"},
    "نا": {"type": "possessive_us"},
    "كم": {"type": "possessive_you_pl"},
    "ك": {"type": "possessive_you"},
    "ه": {"type": "possessive_him"},
    "ي": {"type": "possessive_my"},
}

# Question words
QUESTION_WORDS = {"أين", "اين", "ماذا", "ما", "من", "متى", "كيف", "لماذا", "هل", "كم", "أي", "اي"}

# Negation words
NEGATION_WORDS = {"لم", "لن", "لا", "ما", "ليس", "ليست", "غير"}

# Time expressions
TIME_WORDS = {
    "أمس", "امس", "اليوم", "غداً", "غدا", "الآن", "الان", "صباحاً", "صباحا",
    "مساءً", "مساء", "ليلاً", "ليلا", "دائماً", "دائما",
    "أبداً", "أبدا", "أحياناً", "احيانا", "عادةً", "عادة",
    "قبل", "بعد", "منذ",
}

# Prepositions
PREPOSITIONS = {
    "إلى", "الى", "من", "في", "على", "عن", "مع",
    "بين", "خلال", "حول", "فوق", "تحت", "أمام", "خلف", "عند",
}

# Demonstratives
DEMONSTRATIVES = {"هذا", "هذه", "ذلك", "تلك", "هؤلاء", "أولئك"}

# Numbers (text form)
NUMBER_WORDS = {
    "واحد", "اثنان", "اثنين", "ثلاثة", "ثلاث", "أربعة", "أربع",
    "خمسة", "خمس", "ستة", "ست", "سبعة", "سبع", "ثمانية", "ثماني",
    "تسعة", "تسع", "عشرة", "عشر",
}


def normalize_text(text: str) -> str:
    """Normalize Arabic text:
    - Remove diacritics
    - Normalize alef variants
    - Clean whitespace
    - Remove tatweel (kashida)
    """
    # Remove diacritics
    text = DIACRITICS_PATTERN.sub("", text)

    # Normalize alef variants
    for old, new in ALEF_VARIANTS.items():
        text = text.replace(old, new)

    # Remove tatweel
    text = text.replace("\u0640", "")

    # Clean whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Remove question mark for processing (we detect it separately)
    text = text.replace("؟", "").replace("?", "").strip()

    return text


def detect_sentence_type(text: str) -> str:
    """Detect the sentence type: declarative, question, negation, imperative."""
    original = text.strip()

    # Check for question mark
    if "؟" in original or "?" in original:
        return "question"

    # Tokenize for word-level checks
    words = original.split()

    # Check for question words
    for word in words:
        clean = DIACRITICS_PATTERN.sub("", word)
        if clean in QUESTION_WORDS:
            return "question"

    # Check for negation
    for word in words:
        clean = DIACRITICS_PATTERN.sub("", word)
        if clean in NEGATION_WORDS:
            return "negation"

    return "declarative"


def classify_word(word: str) -> str:
    """Classify a word into a broad POS category using pattern matching."""
    clean = DIACRITICS_PATTERN.sub("", word)

    if clean in QUESTION_WORDS:
        return "QUESTION"
    if clean in NEGATION_WORDS:
        return "NEG"
    if clean in TIME_WORDS:
        return "TIME"
    if clean in PREPOSITIONS:
        return "PREP"
    if clean in DEMONSTRATIVES:
        return "DEM"
    if clean in NUMBER_WORDS:
        return "NUM"

    # Check for definite article → likely noun
    if clean.startswith("ال"):
        return "NOUN"

    # Check for verb patterns (very simplified)
    # Past tense: فَعَلَ pattern (3 root letters common)
    if len(clean) == 3:
        return "VERB"  # Could be either, but 3-letter roots are common verbs

    # Words ending in ة are often nouns/adjectives
    if clean.endswith("ة"):
        return "NOUN"

    # Default
    return "UNKNOWN"


def extract_prefix(word: str) -> tuple[str | None, str]:
    """Extract prefix from an Arabic word.

    Returns (prefix, remaining_word) or (None, word).
    """
    # Check multi-char prefixes first (longer match wins)
    for prefix in sorted(PREFIXES.keys(), key=len, reverse=True):
        if word.startswith(prefix) and len(word) > len(prefix) + 1:
            return prefix, word[len(prefix):]

    return None, word


def extract_suffix(word: str) -> tuple[str | None, str]:
    """Extract suffix from an Arabic word.

    Returns (suffix, remaining_word) or (None, word).
    """
    # Check longer suffixes first
    for suffix in sorted(SUFFIXES.keys(), key=len, reverse=True):
        if word.endswith(suffix) and len(word) > len(suffix) + 1:
            return suffix, word[:-len(suffix)]

    return None, word


def tokenize(text: str) -> list[TokenInfo]:
    """Tokenize Arabic text into annotated tokens.

    Steps:
    1. Normalize the text
    2. Split on whitespace
    3. For each word: detect POS, extract prefixes/suffixes, compute stem
    """
    normalized = normalize_text(text)
    words = normalized.split()

    tokens = []
    for word in words:
        # Check for definite article
        has_article = word.startswith("ال")
        stem = word

        # Strip article for stem
        if has_article and len(word) > 2:
            stem = word[2:]

        # Extract prefix (from original word, not stem)
        prefix, after_prefix = extract_prefix(word)

        # Extract suffix
        suffix, after_suffix = extract_suffix(stem)
        if suffix:
            stem = after_suffix

        # Classify
        pos = classify_word(word)

        # Build features dict
        features = {}
        if prefix and prefix in PREFIXES:
            features["prefix_type"] = PREFIXES[prefix]["type"]
        if suffix and suffix in SUFFIXES:
            features["suffix_type"] = SUFFIXES[suffix]["type"]
        if has_article:
            features["definite"] = True
        if word in TIME_WORDS:
            features["time_expression"] = True
        if word in QUESTION_WORDS:
            features["question_word"] = True
        if word in NEGATION_WORDS:
            features["negation"] = True

        token = TokenInfo(
            token=word,
            pos=pos,
            lemma=stem,
            features=features,
            has_article=has_article,
            prefix=prefix,
            suffix=suffix,
            stem=stem,
        )
        tokens.append(token)

    return tokens
