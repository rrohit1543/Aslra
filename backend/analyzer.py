"""
Morphological analyzer for Arabic text.
Provides a simplified analysis suitable for the ArSL transcription prototype.

NOTE: This is a pattern-based fallback analyzer. For production use,
CAMeL Tools or a similar NLP library would provide much better results.
The limitation is documented in docs/limitations.md.
"""
from __future__ import annotations

from .tokenizer import (
    TokenInfo,
    tokenize,
    detect_sentence_type,
    normalize_text,
    TIME_WORDS,
    QUESTION_WORDS,
    NEGATION_WORDS,
    PREPOSITIONS,
    DEMONSTRATIVES,
    NUMBER_WORDS,
)


class AnalysisResult:
    """Result of analyzing an Arabic sentence."""

    def __init__(self, original: str):
        self.original = original
        self.normalized = normalize_text(original)
        self.sentence_type = detect_sentence_type(original)
        self.tokens: list[TokenInfo] = []
        self.time_expressions: list[tuple[int, str]] = []  # (index, word)
        self.question_words: list[tuple[int, str]] = []
        self.negation_words: list[tuple[int, str]] = []
        self.prepositions: list[tuple[int, str]] = []
        self.demonstratives: list[tuple[int, str]] = []
        self.numbers: list[tuple[int, str]] = []
        self.has_future_prefix: bool = False
        self.has_negation: bool = False
        self.has_question: bool = False
        self.has_time_expression: bool = False


def analyze(text: str) -> AnalysisResult:
    """Analyze an Arabic sentence.

    Returns an AnalysisResult with:
    - Tokenization
    - Sentence type detection
    - Identified time expressions, question words, negation markers
    - Preposition locations
    - Demonstrative locations
    - Number locations
    """
    result = AnalysisResult(text)
    result.tokens = tokenize(text)

    for i, token in enumerate(result.tokens):
        word = token.token
        clean = normalize_text(word)

        # Detect time expressions
        if clean in TIME_WORDS or token.pos == "TIME":
            result.time_expressions.append((i, word))
            result.has_time_expression = True

        # Detect question words
        if clean in QUESTION_WORDS or token.pos == "QUESTION":
            result.question_words.append((i, word))
            result.has_question = True

        # Detect negation
        if clean in NEGATION_WORDS or token.pos == "NEG":
            result.negation_words.append((i, word))
            result.has_negation = True

        # Detect prepositions
        if clean in PREPOSITIONS or token.pos == "PREP":
            result.prepositions.append((i, word))

        # Detect demonstratives
        if clean in DEMONSTRATIVES or token.pos == "DEM":
            result.demonstratives.append((i, word))

        # Detect numbers
        if clean in NUMBER_WORDS or token.pos == "NUM":
            result.numbers.append((i, word))

        # Detect future prefix
        if token.prefix and token.prefix.startswith("س"):
            result.has_future_prefix = True

    # Override sentence type based on detected features
    if result.has_question and result.sentence_type == "declarative":
        result.sentence_type = "question"
    if result.has_negation and result.sentence_type == "declarative":
        result.sentence_type = "negation"

    return result
