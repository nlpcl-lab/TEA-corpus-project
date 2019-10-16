# TEA -- Textual Entailment & Acceptability Corpus Project

The making files of TEA Corpus.

## Introduction

The corpus will consist:

- The pairs of sentences from news article, from Buzzfeed Fake News Corpus.
- Labels of textual entailment, for each pair.
- Labels of acceptability, for each sentences.

## Setup

Requires Python 3 or higher.
Uses `pandas`, `spaCy`, and `pytorch` as core libraries.

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
