# Limitations and Risks

This document outlines the known limitations, uncertainties, and risks associated with the ArSL Transcriber prototype. It is critical to recognize that this is a **research prototype** and not a production-ready sign language translator.

## 1. Linguistic Limitations

### Unified ArSL vs. Regional Variants
- **The "Unified" Myth:** Unified Arabic Sign Language (لغة الإشارة العربية الموحدة) is primarily a dictionary standardization project led by organizations like ALECSO. It standardizes vocabulary (signs) but does not enforce a rigid, universally accepted grammar.
- **Regional Variations:** Deaf communities in different Arab countries (e.g., Saudi Arabia, Egypt, Jordan) have their own rich, natural sign languages (LIU, ESL, JSL) with distinct grammatical features. This prototype attempts to synthesize a "standardized" grammar based on academic literature, which may feel unnatural or "academic" to native signers of regional languages.

### Grammar Uncertainties
- **Tense Markers:** While time expressions (e.g., "yesterday", "tomorrow") are fronted, it remains uncertain whether specific verbs require manual tense markers in Unified ArSL, or if the time expression alone is sufficient. The prototype currently assumes the time expression is sufficient (stripping Arabic tense prefixes).
- **Negation:** The prototype appends a single negation sign (`لا`) and requires a head shake. Whether specific negation particles (like `ليس` vs `لم`) require distinct manual signs in the Unified dictionary requires expert validation.
- **Implicit Pronouns:** The prototype adds implicit pronouns (e.g., `أنا` for first-person future verbs) because ArSL often drops pronouns if they are clear from context or spatial agreement. Our rule is inferred from NLP literature rather than native signer consensus.

## 2. Technical Limitations

### Morphological Analysis
- **Simplified NLP:** The prototype uses a lightweight, regex-based Python tokenizer and morphological analyzer (`backend/tokenizer.py` and `backend/analyzer.py`). It strips common prefixes (سـ, يـ) and suffixes, and handles the definite article (الـ).
- **Risk:** It does not use a robust Arabic NLP pipeline like CAMeL Tools or MADAMIRA (which were excluded to keep the prototype lightweight and easy to run without heavy ML dependencies). Consequently, complex morphological structures, broken plurals, or ambiguous words may be parsed incorrectly.

### Rule Engine Rigidity
- **Fixed Order:** The `TranscriptionEngine` applies rules in a strict priority order. Natural languages often have overlapping or context-dependent rules that a linear pipeline cannot capture perfectly.
- **No Spatial Grammar:** Sign languages make heavy use of spatial grammar (indexing, classifiers, directional verbs). A text-based gloss system inherently flattens this 3D spatial information into a 1D sequence of words, losing significant meaning.

### Dictionary Scope
- The included dictionary (`dictionary.yaml`) contains ~200 entries, focused on the test sentences and common vocabulary. It is a tiny subset of the ~3200 signs in the ALECSO dictionary.
- Many valid Arabic words will be flagged as "Not in dictionary — fingerspelled" simply due to the limited scope of this prototype.

## 3. Reviewability and Mitigation
To mitigate these risks, the system is designed around **Explainability**:
1. **No Black Boxes:** We do not use an LLM at runtime. Every transformation is executed by a specific, traceable rule.
2. **Confidence Scoring:** The UI explicitly flags the confidence level of the transcription based on the proportion of explicit vs. inferred rules applied and dictionary coverage.
3. **Expert Review Flags:** The system proactively generates questions for human experts (e.g., "Word X is not in the dictionary — does it have a standard sign?").
4. **Data Separation:** All rules and dictionary entries are stored in human-readable YAML files, making it trivial for domain experts to correct assumptions without modifying the codebase.
