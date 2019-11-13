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

## Usage

### Python part

You need webis-buzzfeed corpus & pretrained transformers model for MNLI.

1. `python to_csv --path=<path-to-corpus>`
2. `python extract_sent2.py --pretrained=<pretrained-config-folder> --model_type=<xlnet-or-bert>`
3. `python sort_csv.py --csv=<path-to-csv>`
4. `python csv_to_json.py --csv=<path-to-csv> --out=<output-folder>`

### Web part

Uses Vue.js and Firebase.

```bash
cd amt-front
npm install # or yarn
npm run-script build
```
