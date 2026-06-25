# Methodology

This document details the methodology used for discovering sources, extracting grammar rules, and building the explainable transcription prototype for Unified Arabic Sign Language (ArSL).

## 1. How did you discover the source materials?
Source materials were discovered through a systematic search using both English and Arabic queries. We prioritized institutional sources (like the Arab League/ALECSO and World Federation of the Deaf), academic repositories (King Saud University, Cairo University), and peer-reviewed journals (Springer, Oxford UP) to ensure credibility. A total of 18 search queries were executed to cast a wide net across linguistics, NLP, and teaching materials.

## 2. What search queries did you use?
**English Queries:**
1. `"Unified Arabic Sign Language" grammar rules`
2. `"Arabic Sign Language" sentence structure gloss`
3. `ArSL word order syntax morphology`
4. `"Arabic Sign Language" dictionary PDF`
5. `"Arabic Sign Language" linguistic analysis`
*(Plus 7 additional variations focusing on NLP and automatic translation systems)*

**Arabic Queries:**
6. `قواعد لغة الإشارة العربية الموحدة`
7. `ترتيب الجملة في لغة الإشارة العربية`
8. `معجم لغة الإشارة العربية الموحدة`
9. `تعليم لغة الإشارة للصم العرب`
10. `نحو لغة الإشارة العربية بنية الجملة`
*(Plus targeted searches on ALECSO and regional deaf association sites)*

## 3. How did you evaluate whether a source was credible?
Sources were classified into three tiers of credibility:
- **High:** Peer-reviewed academic papers on ArSL linguistics (e.g., Abdel-Fattah 2005) or official institutional publications (e.g., ALECSO dictionary).
- **Medium:** NLP papers describing translation systems. These are credible but may simplify linguistic rules for computational convenience.
- **Low (avoided):** Unsourced community blogs or generic articles without clear authorship.

## 4. How did you handle scanned PDFs or images?
For materials that were not directly machine-readable (such as older printed dictionary pages or scanned PDFs), we prioritized finding academic papers that referenced those materials, as the papers provided machine-readable text and structured summaries of the rules contained within the older materials.

## 5. How did you extract rules from the source materials?
Rules were extracted by analyzing the sources for two types of information:
1. Direct linguistic statements (e.g., "ArSL follows a Topic-Comment structure").
2. Before-and-after examples in NLP papers (e.g., Arabic `ذهب الولد` becoming Gloss `ولد ذهب`).
These were then mapped into a structured YAML format consisting of a trigger (when to apply it) and an action (how to transform the gloss).

## 6. Which rules came directly from explicit statements, and which were inferred?
We implemented a strict tracking system for evidence types:
- **Explicit (6 rules):** Directly stated in the source text (e.g., Time fronting, WH-question placement).
- **Inferred (10 rules):** Deduced from observing translation examples or cross-referencing multiple NLP papers (e.g., exact handling of prepositions and implicit pronouns).
- **Speculative (0 rules):** We avoided adding completely speculative rules to maintain the integrity of the prototype.

## 7. Did you use RAG? If so, how did you use it?
**We did not use RAG for the runtime transcription engine.**
While LLM capabilities were used during the *research phase* to discover sources and extract the YAML rules, the actual transcription prototype is a **pure rule-based engine** written in Python (FastAPI).
*Why?* The assignment prioritized **explainability and traceability**. A rule engine guarantees that every output transformation can be traced back to a specific `rule_id`, which links to specific `evidence` and a `source`. This prevents hallucinations and makes it easy for experts to review and override specific rules.

## 8. How did you prevent the model from inventing grammar rules?
By separating the research phase from the runtime phase. The runtime transcription engine (Python) only executes rules that exist in `rules.yaml`. If a pattern is not in the YAML file (which requires source evidence), it will not be applied. There is no LLM "guessing" the grammar at runtime.

## 9. How did you handle words that were missing from the dictionary?
When a word is not found in `dictionary.yaml` (after attempting to normalize diacritics and strip definite articles), it is added to the gloss sequence but flagged in the output UI.
The system displays: `❌ غير موجود في القاموس — يُهجّأ بالأصابع` (Not in dictionary — fingerspelled). It also generates a specific "Expert Review" item asking if the word should have a standard sign.

## 10. How would you update the rule base with expert feedback?
The rule base and dictionary are entirely decoupled from the code and stored as plain YAML files (`rules.yaml` and `dictionary.yaml`).
If an expert reviews the prototype, they do not need to read Python code. They can simply edit the YAML files to:
- Change a rule's `confidence` level
- Add new `regional_variants` to a dictionary entry
- Modify a rule's `action`
- Add new rules with explicit evidence
The backend loads these files dynamically at startup, so updates are instantly reflected in the system.
