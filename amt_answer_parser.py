import os
import json
import base64
import pandas
import argparse
import jsonlines

from tqdm import tqdm
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('--origin', type=str,
                    default='./csvs/entail05.contra095.bert.sorted.csv')
parser.add_argument('--acc', type=str, default='')
parser.add_argument('--ent', type=str, default='')
parser.add_argument('--out', type=str, default='./jsonls')
args = parser.parse_args()


def get_label(enc):
    dec = base64.b64decode(enc).decode('utf-8')
    return json.loads(dec)['label']


class AcceptabilityAndEntailment:
    def __init__(self):
        self.no = -1
        self.sent1 = None
        self.sent2 = None
        self.acc = [list(), list()]
        self.ent = list()

    def update_acc(self, text_map, row):
        no = int(row['Input.no'])
        if self.no < 0:
            self.no = no // 2

        if row['Answer.answer'][-2:] != '==':
            row['Answer.answer'] += '=='
        if no % 2 == 0:
            if self.sent1 is None:
                self.sent1 = text_map[no // 2]['sent1']
            self.acc[0].append(get_label(row['Answer.answer']))
        else:
            if self.sent2 is None:
                self.sent2 = text_map[no // 2]['sent2']
            self.acc[1].append(get_label(row['Answer.answer']))

    def update_ent(self, text_map, row):
        no = int(row['Input.no'])
        if self.no < 0:
            self.no = no
        if self.sent1 is None:
            self.sent1 = text_map[no]['sent1']
        if self.sent2 is None:
            self.sent2 = text_map[no]['sent2']
        self.ent.append(get_label(row['Answer.answer']))

    def valid(self):
        if self.no < 0:
            return False
        if self.sent1 is None:
            return False
        if self.sent2 is None:
            return False
        if len(self.acc[0]) < 1:
            return False
        if len(self.acc[1]) < 1:
            return False
        if len(self.ent) < 1:
            return False
        return True

    def jsonform(self):
        return {
            'no': self.no,
            'sent1': self.sent1,
            'sent2': self.sent2,
            'acc': self.acc,
            'ent': self.ent
        }


if __name__ == '__main__':
    origin = pandas.read_csv(args.origin, index_col=False)

    text_map = dict()
    for i, row in origin.iterrows():
        text_map[int(row['no'])] = row

    tea_map = defaultdict(AcceptabilityAndEntailment)

    acc = pandas.read_csv(args.acc, index_col=False)
    for i, row in tqdm(acc.iterrows(), total=acc.shape[0]):
        doc_id = int(row['Input.no']) // 2
        tea_map[doc_id].update_acc(text_map, row)
    ent = pandas.read_csv(args.ent, index_col=False)
    for i, row in tqdm(ent.iterrows(), total=ent.shape[0]):
        doc_id = int(row['Input.no'])
        tea_map[doc_id].update_ent(text_map, row)

    writer = jsonlines.open(os.path.join(args.out, 'TEA.jsonl'), mode='w')
    for key in sorted(tea_map.keys()):
        if not tea_map[key].valid():
            continue
        writer.write(tea_map[key].jsonform())
