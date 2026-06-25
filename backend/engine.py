"""
Rule engine for Arabic-to-ArSL gloss transcription.

Takes an analyzed Arabic sentence and applies grammar rules
to produce a gloss sequence with full traceability.
"""
from __future__ import annotations

from .models import (
    GrammarRule,
    AppliedRule,
    GlossItem,
    SourceReference,
    ConfidenceAssessment,
    TranscribeResponse,
    TokenInfo,
)
from .analyzer import AnalysisResult
from .dictionary import SignDictionary
from .sources import get_source_by_id
from .models import Source


class TranscriptionEngine:
    """Engine that applies grammar rules to produce ArSL gloss sequences."""

    def __init__(
        self,
        rules: list[GrammarRule],
        dictionary: SignDictionary,
        sources: list[Source],
    ):
        self.rules = sorted(rules, key=lambda r: r.priority)
        self.dictionary = dictionary
        self.sources = sources

    def transcribe(self, analysis: AnalysisResult) -> TranscribeResponse:
        """Apply rules to an analyzed sentence and produce a full transcription response."""

        # Start with token words as initial gloss order
        gloss_words: list[str] = [t.token for t in analysis.tokens]
        applied_rules: list[AppliedRule] = []
        expert_review_items: list[str] = []

        # Track which rule categories we've applied
        applied_categories: set[str] = set()

        # Apply each rule in priority order
        for rule in self.rules:
            result = self._try_apply_rule(rule, analysis, gloss_words, expert_review_items)
            if result is not None:
                gloss_words, applied_rule = result
                applied_rules.append(applied_rule)
                applied_categories.add(rule.category)

        # Build gloss items with dictionary lookup
        gloss_items = self._build_gloss_items(gloss_words)

        # Build gloss string
        gloss_string = " / ".join(item.gloss for item in gloss_items)

        # Calculate overall confidence
        confidence = self._calculate_confidence(applied_rules, gloss_items)

        # Add expert review items for unverified dictionary entries
        for item in gloss_items:
            if not item.in_dictionary:
                expert_review_items.append(
                    f"الكلمة \"{item.gloss}\" غير موجودة في القاموس — هل لها إشارة معيارية؟ "
                    f"(Word \"{item.gloss}\" not found in dictionary — does it have a standard sign?)"
                )

        return TranscribeResponse(
            input={
                "original": analysis.original,
                "normalized": analysis.normalized,
            },
            tokenization=analysis.tokens,
            applied_rules=applied_rules,
            gloss_sequence=gloss_items,
            gloss_string=gloss_string,
            confidence=confidence,
            expert_review_items=expert_review_items,
        )

    def _try_apply_rule(
        self,
        rule: GrammarRule,
        analysis: AnalysisResult,
        gloss_words: list[str],
        expert_review_items: list[str],
    ) -> tuple[list[str], AppliedRule] | None:
        """Try to apply a single rule. Returns (new_gloss_words, applied_rule) or None."""

        triggered = False
        description = ""

        # ─── Time expression fronting ─────────────────────────
        if rule.category == "time":
            if analysis.has_time_expression:
                triggered = True
                # Move time expressions to front
                time_words = [w for _, w in analysis.time_expressions]
                remaining = [w for w in gloss_words if w not in time_words]
                gloss_words = time_words + remaining
                description = f"نقل التعبير الزمني ({', '.join(time_words)}) إلى بداية الجملة — Time expression moved to front"

        # ─── Article dropping ─────────────────────────────────
        elif rule.category == "article":
            new_words = []
            dropped = False
            
            # Helper to check POS
            def is_noun_or_adj(w_str):
                for t in analysis.tokens:
                    if t.token == w_str or t.lemma == w_str:
                        return t.pos in {"NOUN", "ADJ", "UNKNOWN"}
                return True
                
            for w in gloss_words:
                if w.startswith("ال") and len(w) > 2 and is_noun_or_adj(w):
                    # Keep if exact match is in dictionary (e.g. الطالب)
                    if self.dictionary.lookup(w) and self.dictionary.lookup(w).word == w:
                        new_words.append(w)
                    else:
                        new_words.append(w[2:])
                        dropped = True
                else:
                    new_words.append(w)
            if dropped:
                triggered = True
                gloss_words = new_words
                description = "حذف أداة التعريف (ال) — Definite article (ال) dropped"

        # ─── Preposition omission ─────────────────────────────
        elif rule.category == "preposition":
            if analysis.prepositions:
                triggered = True
                prep_words = {w for _, w in analysis.prepositions}
                gloss_words = [w for w in gloss_words if w not in prep_words]
                description = f"حذف حروف الجر ({', '.join(prep_words)}) — Prepositions omitted"

        # ─── Negation handling ────────────────────────────────
        elif rule.category == "negation":
            if analysis.has_negation:
                triggered = True
                # Remove Arabic negation particles, add single negation marker at end
                neg_words = {w for _, w in analysis.negation_words}
                gloss_words = [w for w in gloss_words if w not in neg_words]
                # Check if we should add negation sign
                if "لا" not in gloss_words:
                    gloss_words.append("لا")
                description = "معالجة النفي: إزالة أداة النفي وإضافة إشارة النفي في النهاية — Negation: particle removed, negation sign added at end"
                expert_review_items.append(
                    "هل يحتاج النفي إلى علامة يدوية أم تعبير وجهي فقط؟ "
                    "(Does negation require a manual sign or only a facial expression?)"
                )

        # ─── Question handling ────────────────────────────────
        elif rule.category == "question":
            if analysis.has_question:
                triggered = True
                if analysis.question_words:
                    # WH-questions: move question word to end (or keep at end)
                    q_words = {w for _, w in analysis.question_words}
                    remaining = [w for w in gloss_words if w not in q_words]
                    gloss_words = remaining + list(q_words)
                    description = f"سؤال استفهامي: نقل أداة الاستفهام ({', '.join(q_words)}) إلى النهاية — WH-question word moved to end"
                else:
                    description = "سؤال نعم/لا: يُعبَّر عنه بتعبير وجهي (رفع الحاجبين) — Yes/no question: expressed through facial expression (raised eyebrows)"

        # ─── Verb tense handling ──────────────────────────────
        elif rule.category == "tense":
            # Strip future prefix and use base form
            new_words = []
            modified = False
            for w in gloss_words:
                if w.startswith("سأ") or w.startswith("سن") or w.startswith("ست") or w.startswith("سي") or w.startswith("سا"):
                    new_words.append(w[2:])
                    modified = True
                elif w.startswith("ي") and len(w) > 3:
                    # Imperfect prefix — use stem
                    new_words.append(w[1:])
                    modified = True
                else:
                    new_words.append(w)
            if modified or analysis.has_future_prefix:
                triggered = True
                gloss_words = new_words
                description = "تصريف الفعل: استخدام الشكل الأساسي — Verb tense: use base form (tense indicated by time word)"
                expert_review_items.append(
                    "هل يكفي التعبير الزمني وحده أم يحتاج الفعل إلى إشارة زمنية إضافية؟ "
                    "(Is the time expression alone sufficient, or does the verb need an additional tense marker?)"
                )

        # ─── Pronoun handling ─────────────────────────────────
        elif rule.category == "pronoun":
            # Pronouns are often implicit in ArSL but we add them when needed
            if analysis.has_future_prefix:
                # Future prefix implies first person — add أنا if not present
                has_pronoun = any(t.token in {"أنا", "نحن", "أنت", "هو", "هي"} for t in analysis.tokens)
                if not has_pronoun:
                    triggered = True
                    # Insert pronoun after time word (or at start)
                    insert_pos = 0
                    for i, w in enumerate(gloss_words):
                        if w in {tw for _, tw in analysis.time_expressions}:
                            insert_pos = i + 1
                            break
                    gloss_words.insert(insert_pos, "أنا")
                    description = "إضافة ضمير ضمني (أنا) — Implicit pronoun (أنا/I) added"

        # ─── Word order (Topic-Comment) ───────────────────────
        elif rule.category == "word_order":
            # ArSL tends toward Topic-Comment / SOV
            # Find the verb and move it to the end
            verb_idx = -1
            for i, w in enumerate(gloss_words):
                entry = self.dictionary.lookup(w)
                if entry and entry.category == "verb":
                    verb_idx = i
                    break
            
            if verb_idx == -1:
                # Fallback to token POS
                for i, w in enumerate(gloss_words):
                    for t in analysis.tokens:
                        if (t.token == w or t.lemma == w) and t.pos == "VERB":
                            verb_idx = i
                            break
                    if verb_idx != -1:
                        break
            
            if verb_idx != -1:
                # Only move it if it's not already at the end, and we have multiple words
                if len(gloss_words) > 1 and verb_idx < len(gloss_words) - 1:
                    triggered = True
                    verb = gloss_words.pop(verb_idx)
                    gloss_words.append(verb)
                    description = "ترتيب الكلمات: نقل الفعل إلى النهاية (موضوع-خبر) — Word order: verb moved to end (Topic-Comment)"

        # ─── Adjective placement ──────────────────────────────
        elif rule.category == "adjective":
            # In ArSL, adjective typically follows the noun (same as Arabic)
            # This is a no-op confirmation rule
            triggered = False  # Only trigger if we detect out-of-order adjectives

        # ─── Number expressions ───────────────────────────────
        elif rule.category == "number":
            if analysis.numbers:
                triggered = True
                description = "التعبيرات العددية: العدد قبل المعدود — Number expressions: number before noun (ArSL standard)"

        # ─── Non-manual markers ───────────────────────────────
        elif rule.category == "non_manual":
            if analysis.sentence_type == "question":
                triggered = True
                description = "علامات غير يدوية: رفع الحاجبين للأسئلة — Non-manual markers: raised eyebrows for questions"
            elif analysis.sentence_type == "negation":
                triggered = True
                description = "علامات غير يدوية: هز الرأس للنفي — Non-manual markers: head shake for negation"

        # ─── Fallback for unknown words ───────────────────────
        elif rule.category == "fallback":
            # Check dictionary for each word
            has_unknown = False
            for w in gloss_words:
                if self.dictionary.lookup(w) is None:
                    has_unknown = True
                    break
            if has_unknown:
                triggered = True
                description = "احتياطي: الكلمات غير الموجودة في القاموس يتم تهجئتها بالأصابع — Fallback: words not in dictionary are fingerspelled"

        if not triggered:
            return None

        # Build the AppliedRule record
        source_refs = []
        for ev in rule.evidence:
            src = get_source_by_id(self.sources, ev.source_id)
            if src:
                source_refs.append(SourceReference(
                    source_id=ev.source_id,
                    title=src.title,
                    page_or_section=ev.page_or_section,
                    quote_or_summary=ev.quote_or_summary,
                    url=src.url,
                ))

        # Add review questions
        if rule.requires_expert_review and rule.review_questions:
            for q in rule.review_questions:
                if q not in expert_review_items:
                    expert_review_items.append(q)

        applied_rule = AppliedRule(
            rule_id=rule.id,
            rule_name=rule.name,
            category=rule.category,
            description=description,
            evidence_type=rule.evidence_type,
            confidence=rule.confidence,
            sources=source_refs,
        )

        return gloss_words, applied_rule

    def _build_gloss_items(self, gloss_words: list[str]) -> list[GlossItem]:
        """Build GlossItem list with dictionary lookup for each word."""
        items = []
        for word in gloss_words:
            entry = self.dictionary.lookup(word)
            if entry:
                items.append(GlossItem(
                    gloss=entry.sign_gloss,
                    original_word=word,
                    in_dictionary=True,
                    dictionary_note=f"{'✅ موثّق' if entry.verified else '⚠️ غير موثّق'} — {entry.notes}" if entry.notes else (
                        "✅ موثّق (Verified)" if entry.verified else "⚠️ غير موثّق (Unverified)"
                    ),
                ))
            else:
                items.append(GlossItem(
                    gloss=word,
                    original_word=word,
                    in_dictionary=False,
                    dictionary_note="❌ غير موجود في القاموس — يُهجّأ بالأصابع (Not in dictionary — fingerspelled)",
                ))
        return items

    def _calculate_confidence(
        self,
        applied_rules: list[AppliedRule],
        gloss_items: list[GlossItem],
    ) -> ConfidenceAssessment:
        """Calculate overall confidence based on rules and dictionary coverage."""

        if not applied_rules:
            return ConfidenceAssessment(
                level="low",
                explanation="لم يتم تطبيق أي قواعد — No rules were applied to this sentence",
            )

        # Count evidence types
        explicit_count = sum(1 for r in applied_rules if r.evidence_type == "explicit")
        inferred_count = sum(1 for r in applied_rules if r.evidence_type == "inferred")
        speculative_count = sum(1 for r in applied_rules if r.evidence_type == "speculative")

        # Count dictionary coverage
        total_gloss = len(gloss_items)
        in_dict = sum(1 for g in gloss_items if g.in_dictionary)
        dict_coverage = in_dict / total_gloss if total_gloss > 0 else 0

        # Calculate level
        if explicit_count >= len(applied_rules) * 0.6 and dict_coverage >= 0.8:
            level = "high"
        elif speculative_count >= len(applied_rules) * 0.5 or dict_coverage < 0.4:
            level = "low"
        else:
            level = "medium"

        parts = []
        if explicit_count > 0:
            parts.append(f"قواعد صريحة: {explicit_count} (Explicit rules: {explicit_count})")
        if inferred_count > 0:
            parts.append(f"قواعد مستنتجة: {inferred_count} (Inferred rules: {inferred_count})")
        if speculative_count > 0:
            parts.append(f"قواعد تخمينية: {speculative_count} (Speculative rules: {speculative_count})")
        parts.append(f"تغطية القاموس: {in_dict}/{total_gloss} (Dictionary coverage: {in_dict}/{total_gloss})")

        return ConfidenceAssessment(
            level=level,
            explanation=" | ".join(parts),
        )
