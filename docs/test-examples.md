# Test Examples

These are the 5 test sentences required by the assignment, showing the expected transcription pipeline from original Arabic to Unified Arabic Sign Language (ArSL) gloss sequences.

## 1. Time, Preposition, Article, and Word Order

**Input**: `ذهب الطالب إلى المدرسة أمس` (The student went to school yesterday)

**Tokenization**:
- `ذهب` (VERB)
- `الطالب` (NOUN) - definite: true
- `إلى` (PREP)
- `المدرسة` (NOUN) - definite: true
- `أمس` (TIME)

**Applied Rules**:
1. **Time Fronting**: Moved `أمس` to the front of the utterance.
2. **Definite Article Dropping**: Removed `الـ` from `الطالب` and `المدرسة`.
3. **Preposition Omission**: Removed `إلى` (spatial relationship usually replaces explicit prepositions).
4. **Topic-Comment Word Order**: Moved the verb `ذهب` to the end.

**Resulting Gloss Sequence**:
> **أمس / طالب / مدرسة / ذهب**

---

## 2. Negation and Preposition

**Input**: `لم يذهب أحمد إلى المدرسة` (Ahmed did not go to school)

**Tokenization**:
- `لم` (NEG)
- `يذهب` (VERB)
- `أحمد` (NOUN)
- `إلى` (PREP)
- `المدرسة` (NOUN) - definite: true

**Applied Rules**:
1. **Negation Handling**: Removed `لم` and appended the negation sign `لا` to the end of the clause.
2. **Preposition Omission**: Removed `إلى`.
3. **Definite Article Dropping**: Removed `الـ` from `المدرسة`.
4. **Verb Tense**: Stripped imperfect prefix `يـ` to yield base form `ذهب`.
5. **Topic-Comment**: Moved verb `ذهب` before negation.
6. **Non-manual Markers**: Added head shake requirement.

**Resulting Gloss Sequence**:
> **أحمد / مدرسة / ذهب / لا** *(+ head shake)*

---

## 3. Questions and Tense

**Input**: `أين تعمل؟` (Where do you work?)

**Tokenization**:
- `أين` (QUESTION)
- `تعمل` (VERB)

**Applied Rules**:
1. **WH-Question Placement**: Moved question word `أين` to the end of the sentence.
2. **Verb Tense**: Stripped imperfect prefix `تـ` to yield base form `عمل`.
3. **Non-manual Markers**: Added raised eyebrows requirement for WH-question.

**Resulting Gloss Sequence**:
> **عمل / أين** *(+ raised eyebrows)*

---

## 4. Future Tense, Numbers, and Pronouns

**Input**: `سأشتري ثلاثة كتب غداً` (I will buy three books tomorrow)

**Tokenization**:
- `سأشتري` (VERB) - future prefix: `سأ`
- `ثلاثة` (NUM)
- `كتب` (NOUN)
- `غداً` (TIME)

**Applied Rules**:
1. **Time Fronting**: Moved `غداً` to the front.
2. **Verb Tense**: Stripped future prefix `سأ` to yield base form `شتري`.
3. **Implicit Pronoun Addition**: The `سأ` prefix implies 1st person singular. Since `أنا` was not in the sentence, it is inserted after the time word.
4. **Number Expression**: `ثلاثة` before `كتب` (maintained as in Arabic).
5. **Topic-Comment**: Verb `شتري` moved to the end.

**Resulting Gloss Sequence**:
> **غدا / أنا / ثلاثة / كتب / شتري**

---

## 5. Demonstratives and Adjectives

**Input**: `هذا الكتاب جميل جداً` (This book is very beautiful)

**Tokenization**:
- `هذا` (DEM)
- `الكتاب` (NOUN) - definite: true
- `جميل` (ADJ)
- `جداً` (ADV/INTENSIFIER)

**Applied Rules**:
1. **Definite Article Dropping**: Removed `الـ` from `الكتاب`.
2. **Noun Phrase Structure**: Demonstrative `هذا` remains before the noun.
3. **Adjective Placement**: Adjective `جميل` remains after the noun (matches Arabic).

**Resulting Gloss Sequence**:
> **هذا / كتاب / جميل / جدا**
