"""
Pydantic models for the ArSL Transcriber API.
Defines all request/response schemas used across the application.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ─── Request Models ───────────────────────────────────────────────

class TranscribeRequest(BaseModel):
    """Request body for the POST /api/transcribe endpoint."""
    text: str = Field(
        ...,
        description="Arabic sentence to transcribe into ArSL gloss sequence",
        min_length=1,
        max_length=1000,
        examples=["ذهب الطالب إلى المدرسة أمس"],
    )


# ─── Data Models (internal representations) ──────────────────────

class SourceReference(BaseModel):
    """A reference to a source that supports a rule or claim."""
    source_id: str
    title: str = ""
    page_or_section: str = ""
    quote_or_summary: str = ""
    url: str = ""


class EvidenceEntry(BaseModel):
    """Evidence linking a rule to a source."""
    source_id: str
    page_or_section: str = ""
    quote_or_summary: str = ""


class RuleExample(BaseModel):
    """An example demonstrating a rule's application."""
    input: str
    output: str
    explanation: str = ""


class GrammarRule(BaseModel):
    """A single grammar rule for Arabic-to-ArSL transcription."""
    id: str
    name: str
    category: str
    description: str
    trigger: str
    action: str
    evidence_type: str = "speculative"  # explicit | inferred | speculative
    evidence: list[EvidenceEntry] = []
    confidence: str = "low"  # high | medium | low
    priority: int = 50
    examples: list[RuleExample] = []
    notes: str = ""
    requires_expert_review: bool = True
    review_questions: list[str] = []


class DictionaryEntry(BaseModel):
    """A single entry in the sign dictionary."""
    word: str
    sign_gloss: str
    category: str = "other"
    verified: bool = False
    source_id: str = ""
    notes: str = ""
    regional_variants: list[str] = []


class Source(BaseModel):
    """A source document used in the research."""
    id: str
    title: str
    language: str = "en"
    url: str = ""
    acquisition_method: str = ""
    type: str = ""  # dictionary | grammar | teaching | academic | institutional | community
    credibility: str = "medium"
    credibility_reason: str = ""
    rules_supported: list[str] = []
    limitations: str = ""
    year: str = ""
    author: str = ""


# ─── Response Models ─────────────────────────────────────────────

class TokenInfo(BaseModel):
    """Information about a single token from the input sentence."""
    token: str
    pos: str = "UNKNOWN"
    lemma: str = ""
    features: dict = {}
    has_article: bool = False
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    stem: str = ""


class AppliedRule(BaseModel):
    """Record of a rule that was applied during transcription."""
    rule_id: str
    rule_name: str
    category: str = ""
    description: str
    evidence_type: str = "speculative"
    confidence: str = "low"
    sources: list[SourceReference] = []


class GlossItem(BaseModel):
    """A single item in the output gloss sequence."""
    gloss: str
    original_word: str = ""
    in_dictionary: bool = False
    dictionary_note: str = ""


class ConfidenceAssessment(BaseModel):
    """Overall confidence assessment for the transcription."""
    level: str = "low"  # high | medium | low
    explanation: str = ""


class TranscribeResponse(BaseModel):
    """Full response from the POST /api/transcribe endpoint."""
    input: dict = Field(
        default_factory=dict,
        description="Original and normalized input text",
    )
    tokenization: list[TokenInfo] = []
    applied_rules: list[AppliedRule] = []
    gloss_sequence: list[GlossItem] = []
    gloss_string: str = ""
    confidence: ConfidenceAssessment = ConfidenceAssessment()
    expert_review_items: list[str] = []


class RuleListResponse(BaseModel):
    """Response for GET /api/rules."""
    count: int = 0
    rules: list[GrammarRule] = []


class SourceListResponse(BaseModel):
    """Response for GET /api/sources."""
    count: int = 0
    sources: list[Source] = []


class DictionaryListResponse(BaseModel):
    """Response for GET /api/dictionary."""
    count: int = 0
    entries: list[DictionaryEntry] = []


class HealthResponse(BaseModel):
    """Response for GET /api/health."""
    status: str = "ok"
    rules_loaded: int = 0
    sources_loaded: int = 0
    dictionary_loaded: int = 0
