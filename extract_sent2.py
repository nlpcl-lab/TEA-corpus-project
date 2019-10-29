'''
Extract second sentences from news articles.
They are extracted based on the entailment score,
judged by MNLI-pretrained XLNet model.
'''

import random
import pandas
import spacy
import argparse
import torch
import numpy as np

from tqdm import tqdm
from transformers import (
    XLNetForSequenceClassification,
    XLNetTokenizer,
    BertForSequenceClassification,
    BertTokenizer)
from torch import nn

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, default='./buzzfeed.csv')
parser.add_argument('--pretrained', type=str, default='./pretrained')
parser.add_argument('--device', type=str, default='cuda')
parser.add_argument('--reverse', action='store_true')
parser.add_argument('--output', type=str, default='buzzfeed_sent2.csv')
parser.add_argument('--model_type', type=str, default='xlnet')
args = parser.parse_args()

NLP = spacy.load('en_core_web_sm')
MAX_LENGTH = 128
BATCH_SIZE = 8

MODEL_DICT = {
    'xlnet': (XLNetForSequenceClassification, XLNetTokenizer),
    'bert': (BertForSequenceClassification, BertTokenizer)
}


def list2tensor(item):
    return torch.tensor([item]).to(args.device)


class Input:
    def __init__(self,
                 sentence,
                 input_ids,
                 attention_mask,
                 token_type_ids):
        self.sentence = sentence
        self.input_ids = input_ids
        self.attention_mask = attention_mask
        self.token_type_ids = token_type_ids
        self.score = None

    def get(self):
        return {
            'input_ids': list2tensor(self.input_ids),
            'attention_mask': list2tensor(self.attention_mask),
            'token_type_ids': list2tensor(self.token_type_ids)
        }


def choose_sentence(row, model, tokenizer):
    # random choice from (entailment, neutral, contradiction)
    doc = NLP(row['text'])
    sentences = list(
        filter(lambda x: len(x) > 40, [x.string.strip() for x in doc.sents]))
    pivot_sentence = sentences[0]
    inputs = list()
    for sentence in sentences[1:]:
        input_dict = tokenizer.encode_plus(
            sentence,
            pivot_sentence,
            add_special_tokens=True,
            max_length=MAX_LENGTH) \
            if args.reverse else tokenizer.encode_plus(
            pivot_sentence,
            sentence,
            add_special_tokens=True,
            max_length=MAX_LENGTH
        )
        input_ids, token_type_ids = input_dict['input_ids'], input_dict['token_type_ids']
        attention_mask = [1] * len(input_ids)
        padding_length = MAX_LENGTH - len(input_ids)

        input_ids += [0] * padding_length
        attention_mask += [0] * padding_length
        token_type_ids += [0] * padding_length

        inputs.append(Input(sentence,
                            input_ids,
                            attention_mask,
                            token_type_ids))

    softmax = nn.Softmax(dim=1)
    results = list()
    for feat in tqdm(inputs, desc='Calculating Entailment'):
        model.eval()
        with torch.no_grad():
            output = model(**feat.get())
            results.append(softmax(output[0]).squeeze().cpu().tolist())

    argmaxres = np.argmax(np.asarray(results), axis=0) \
        if len(results) > 0 else [-1, -1, -1]
    maxres = np.max(np.asarray(results), axis=0) \
        if len(results) > 0 else [0, 0, 0]
    maxscoreidx = np.argmax(maxres)
    sentence = inputs[argmaxres[maxscoreidx]].sentence \
        if argmaxres[maxscoreidx] >= 0 else 'False'
    label = '%s(%s)' % (['contradiction', 'entailment',
                         'neutral'][maxscoreidx], str(maxres))
    return pivot_sentence, sentence, label


if __name__ == '__main__':
    data = pandas.read_csv(args.path, index_col=False).fillna('')
    model = MODEL_DICT[args.model_type][0].from_pretrained(args.pretrained)
    tokenizer = MODEL_DICT[args.model_type][1].from_pretrained(args.pretrained)
    model.to(args.device)

    for idx, row in tqdm(data.iterrows(), total=data.shape[0]):
        if len(row['text'].strip()) < 1:
            data.drop(idx, inplace=True)
            continue

    pivot_sentences = list()
    second_sentences = list()
    labels = list()
    for idx, row in tqdm(data.iterrows(), total=data.shape[0], desc='Row'):
        pivot_sentence, chosen_sentence, label = choose_sentence(
            row, model, tokenizer)
        pivot_sentences.append(pivot_sentence)
        second_sentences.append(chosen_sentence)
        labels.append(label)
    data['sent1'] = pivot_sentences
    data['sent2'] = second_sentences
    data['machine_label'] = labels
    data.to_csv(args.output, na_rep='')
