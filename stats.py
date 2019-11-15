import os
import json
import pandas
import argparse
import jsonlines
import statistics

from tqdm import tqdm
from statistics import mode
from collections import Counter, defaultdict

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
        except statistics.StatisticsError:
            uncounted += 1

    ent_counter = Counter(ent_labels)

    print('===Entailment label distribution===')
    print('Uncounted: %d/%d' % (uncounted, len(jsons)))
    print(['%s: %d(%.2f%%)' % (i,
                               ent_counter[i],
                               ent_counter[i] / sum(ent_counter.values()) * 100)
           for i in ent_counter])


def MSE(reals, predictions):
    assert len(reals) == len(predictions)

    return sum([(real - pred) ** 2 for real, pred in zip(reals, predictions)]) / len(reals)


def MAPE(reals, predictions):
    assert len(reals) == len(predictions)

    return 100 / len(reals) * sum(
        [abs(real - pred) / real for real, pred in zip(reals, predictions)])


def filtered(lst):
    return list(filter(lambda x: x > 0, lst))


def ent_acc_relation(jsons):
    ent_dict = defaultdict(lambda: [list(), list()])
    for json in jsons:
        try:
            label = ENT_LABEL[mode(json['ent'])]
            ent_dict[label][0].append(
                sum(filtered(json['acc'][0])) /
                len(filtered(json['acc'][0])))
            ent_dict[label][1].append(
                sum(filtered(json['acc'][1])) /
                len(filtered(json['acc'][1])))
        except statistics.StatisticsError:
            continue

    print('\n===Entailment-Acceptability Relation===')
    for key in ENT_LABEL:
        print('%s: %.3f, %.3f%%' % (key, MSE(ent_dict[key][0], ent_dict[key][1]),
                                    MAPE(ent_dict[key][0], ent_dict[key][1])))


def machine_v_human(jsons, csv_map):
    # pred_dict[machine][human]
    preds = [[0 for _ in ENT_LABEL] for _ in ENT_LABEL]
    for json in jsons:
        try:
            label = mode(json['ent'])
            preds[label][csv_map[json['no']]] += 1
        except statistics.StatisticsError:
            continue

    df = pandas.DataFrame(preds,
                          [l + '(h)' for l in ENT_LABEL],
                          [l + '(m)' for l in ENT_LABEL])

    print('\n===Machine-v-Human Prediction===')
    print(df)


if __name__ == '__main__':
    reader = jsonlines.open(args.jsonl)
    jsons = [x for x in reader]
    csv = pandas.read_csv(args.csv, index_col=False)
    csv_map = dict()
    for i, row in csv.iterrows():
        csv_map[int(row['no'])] = ENT_LABEL.index(
            row['machine_label'].split('(')[0])

    get_ent_label_distribution(jsons)
    ent_acc_relation(jsons)
    machine_v_human(jsons, csv_map)
