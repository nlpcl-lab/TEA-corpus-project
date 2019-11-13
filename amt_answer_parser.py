import os
import csv
import json
import base64
import pandas
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
        no = int(row['no'])
        if self.no < 0:
            self.no = no // 2
        if no % 2 == 0:
            if self.sent1 is None:
                self.sent1 = text_map[no // 2]['sent1']
            self.acc[0].append(get_label(row['answer']))
        else:
            if self.sent2 is None:
                self.sent2 = text_map[no // 2]['sent2']
            self.ann[1].append(get_label(row['answer']))

    def update_ent(self, text_map, row):
        self.ent.append(get_label(row['answer']))

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

    acc = pandas.read_csv(args.acc, index_col=False)
    text_map = dict()

    for i, row in origin.iterrows():
        text_map[int(row['no'])] = row

    tea_map = defaultdict(AcceptabilityAndEntailment)
    for i, row in tqdm(acc.iterrows(), total=acc.shape[0]):
        doc_id = int(row['no']) // 2
        tea_map[doc_id].update(text_map, row)

    writer = jsonlines.open(os.path.join(args.out, 'TEA.jsonl'), mode='w')
    for key in sorted(tea_map.keys()):
        writer.write(tea_map[key].jsonform())
