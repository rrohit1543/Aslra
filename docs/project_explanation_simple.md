# Project ArSL Transcriber: A Simple Explanation

## The Problem We Wanted to Solve
Arabic Sign Language (ArSL) is a beautiful and complex language used by deaf communities across the Arab world. While spoken and written Arabic follow specific grammar rules (like usually putting the verb at the beginning of a sentence), Sign Language has a completely different structure! 

For example, if you say in Arabic *"The student went to the school yesterday,"* in Sign Language, you would sign it as *"Yesterday, the student, school, went."* 

Our mission was to figure out: **Are there clear, reusable rules we can extract from books and research to automatically translate written Arabic into the correct sequence of signs?** And importantly, can we prove *why* the computer made its translation?

## How We Approached It

### Step 1: Becoming Researchers First
Instead of just guessing or using an AI that acts like a "black box," we first searched for credible sources across the web. We collected Arabic Sign Language dictionaries, academic papers, and institutional guidelines to find out exactly how real people sign.

### Step 2: Extracting the "Golden Rules"
From our research, we pulled out a series of clear grammar rules. For example:
- **The "Time First" Rule:** Time words (like "yesterday" or "tomorrow") are always moved to the very beginning of the sentence to set the stage.
- **The "Action Last" Rule:** The main action (the verb) is usually moved to the end of the sentence.
- **Simplifying Words:** Sign language doesn't use little filler words like "to" or "the" in the same way, so we created rules to safely drop them.

### Step 3: Building a Smart Dictionary
We built a custom dictionary containing hundreds of common words. Each word was carefully verified against our sources to ensure that when we translate an Arabic word, we are pointing to a real, documented sign.

### Step 4: Building the "Explainable" Engine
We wrote a computer program (the engine) that reads an Arabic sentence and applies our golden rules one by one. 

**Why this is special:** Most modern translators use AI that magically gives you an answer, but can't tell you *why*. Our system is designed to be **100% explainable**. Every time it translates a sentence, it shows you exactly which grammar rules it applied and points you to the exact book or research paper where that rule was found!

## The Result
We successfully built a prototype! You can type in an Arabic sentence, and the system instantly translates it into the correct sequence of sign language words (called "glosses"). Best of all, it acts like a transparent math equation, showing its work step-by-step so that language experts can audit, trust, and improve it.
