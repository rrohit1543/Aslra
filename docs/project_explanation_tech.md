# Project ArSL Transcriber: A Technical Breakdown

## The Architecture Challenge
The objective was to determine whether Unified Arabic Sign Language (UASL/ArSL) possesses productizable, deterministic grammar rules that can be codified into an automated transcription pipeline, moving away from black-box LLM translation towards an explainable, auditable, rule-based expert system.

The core challenge was parsing standard Arabic (VSO order, heavily affixed, rich morphology) into ArSL gloss sequences (typically Topic-Comment/SOV order, temporal fronting, isolated morphemes), while ensuring that every transformation is strictly traceable back to cited linguistic research.

## The Implementation Strategy

### 1. Source Discovery & Rule Extraction (Subagent Research)
We utilized a dedicated autonomous subagent to crawl both Arabic and English academic literature, institutional guidelines (e.g., ALECSO dictionaries), and community materials. 
The agent compiled a formalized YAML database of 14 high-credibility sources and distilled them into 16 distinct, executable grammar rules. Each rule requires explicit triggers, transformations, and evidence linkages to prevent algorithmic hallucination.

### 2. Lexical & Morphological Pipeline
We developed a deterministic NLP pipeline in Python (FastAPI):
- **Tokenizer & Normalizer:** Handles Arabic script complexities (orthographic variations, diacritics removal, unified alef/tah-marbuta conversion).
- **Morphological Analyzer:** A lightweight POS tagger and entity detector. It identifies temporal expressions, question words, negations, prepositions, and verb tenses by matching common Arabic prefixes/suffixes (e.g., extracting the future tense prefix `سأ` to isolate the verb root).

### 3. The Explainable Rule Engine
At the core of the backend is the `TranscriptionEngine`, a sequential state machine that mutates an array of `GlossItem` objects based on prioritized triggers. 
Rather than utilizing an LLM at runtime, the engine iterates through the YAML-defined rules (ordered by application priority):
1. **Time Fronting (Priority 1):** Extracts identified temporal adverbs and unshifts them to the 0th index.
2. **Definite Article & Preposition Stripping:** Aggressively drops functional words and affixes not expressed manually in ArSL.
3. **Negation Handling:** Removes inline Arabic negators (`لم`, `لن`) and appends the ArSL negation gloss (`لا/NEG`) to the end of the clause.
4. **Topic-Comment Reordering (Priority 5):** If a VSO structure is detected, it pops the root verb and appends it to the end of the clause, enforcing the SOV standard.

### 4. Dictionary Mapping & Fallback
Post-restructuring, tokens are queried against a curated 200+ entry YAML dictionary mapping Arabic lemmas to standardized ArSL sign glosses. If a token misses the dictionary, the engine triggers a `Fingerspelling Fallback` rule (`fs(word)`), accurately mirroring real-world sign language behavior for proper nouns or unknown vocabulary.

### 5. Transparent Execution & UI
The frontend (Vanilla JS/CSS) communicates with the FastAPI endpoint. The API response returns not just the final gloss string, but an ordered array of `applied_rules`. The UI maps these back to the UI, providing the user with a step-by-step trace of exactly which linguistic rule fired, in what order, and *why*.

This architecture yields a 100% deterministic, highly performant, and fully explainable transcription prototype ideal for academic audit and specialized enterprise adoption.
