import os
import json
import pandas
import argparse
import jsonlines

from tqdm import tqdm
from statistics import mode
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument('--jsonl', type=str, default='./jsonls/TEA.jsonl')
parser.add_argument('--csv', type=str,
                    default='./csvs/entail05.contra095.bert.sorted.csv')
args = parser.parse_args()

ENT_LABEL = ['contradiction', 'entailment', 'neutral']


def get_ent_label_distribution(jsons):
    ent_labels = list()
    uncounted = 0

    for json in jsons:
        try:
            ent_labels.append(ENT_LABEL[mode(json['ent'])])
        except:
            uncounted += 1

    ent_counter = Counter(ent_labels)

    print('===Entailment label distribution===')
    print('Uncounted: %d/%d' % (uncounted, len(jsons)))
    print(['%s: %d(%.2f%%)' % (i,
                               ent_counter[i],
                               ent_counter[i] / sum(ent_counter.values()) * 100)
           for i in ent_counter])


if __name__ == '__main__':
    reader = jsonlines.open(args.jsonl)
    jsons = [x for x in reader]

    get_ent_label_distribution(jsons)