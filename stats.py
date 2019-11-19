import os
import json
import random
import pandas
import argparse
import jsonlines
import statistics
import matplotlib
import numpy as np

from collections import Counter, defaultdict
from statistics import mode
from tqdm import tqdm

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


def AVGDIFF(reals, predictions):
    assert len(reals) == len(predictions)

    return sum([abs(real - pred) for real, pred in zip(reals, predictions)]) / len(reals)


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
        print('%s: %.3f(AVGDIFF)' %
              (key, AVGDIFF(ent_dict[key][0], ent_dict[key][1])))


CAT_STANDARD = {
    7: 3,
    6: 3,
    5: 3,
    4: 2,
    3: 1,
    2: 1,
    1: 1
}


def get_acc_label(lst):
    fltrd = filtered(lst)
    avg = sum(fltrd) / len(fltrd)
    return CAT_STANDARD[round(avg)]


def cat_ent_acc_relation(jsons):
    ent_dict = defaultdict(lambda: [list(), list()])
    for json in jsons:
        try:
            label = ENT_LABEL[mode(json['ent'])]
            ent_dict[label][0].append(get_acc_label(json['acc'][0]))
            ent_dict[label][1].append(get_acc_label(json['acc'][1]))
        except statistics.StatisticsError:
            continue
    print('\n===(Categorized)Entailment-Acceptability Relation===')
    for key in ENT_LABEL:
        print('%s: %.3f(AVGDIFF)' %
              (key, AVGDIFF(ent_dict[key][0], ent_dict[key][1])))


def machine_v_human(jsons, csv_map):
    # pred_dict[machine][human]
    preds = [[0 for _ in ENT_LABEL] for _ in ENT_LABEL]
    categorized_sents = defaultdict(lambda: defaultdict(list))
    for json in jsons:
        try:
            label = mode(json['ent'])
            preds[label][csv_map[json['no']]] += 1
            categorized_sents[label][csv_map[json['no']]].append(json)
        except statistics.StatisticsError:
            continue

    df = pandas.DataFrame(preds,
                          [l + '(h)' for l in ENT_LABEL],
                          [l + '(m)' for l in ENT_LABEL])

    print('\n===Machine-v-Human Prediction===')
    print(df)
    with open('res_mvh.txt', 'w') as f:
        for i in range(3):
            for j in range(3):
                f.write('%s(h)-%s(m):\n' % (ENT_LABEL[i], ENT_LABEL[j]))
                sample = random.choice(categorized_sents[i][j])
                f.write('sent1: %s\n' % sample['sent1'])
                f.write('sent2: %s\n\n' % sample['sent2'])


def filter_by_label(x):
    try:
        label = ENT_LABEL[mode(x['ent'])]
        return label
    except statistics.StatisticsError:
        return None


LA_DICT = {
    3: 'Accept',
    2: 'Hard',
    1: 'Reject'
}


def get_variant_matrix(jsons):
    for label in ENT_LABEL:
        labelled = list(filter(lambda x: filter_by_label(x) == label, jsons))
        classified = [[0 for _ in ENT_LABEL] for _ in ENT_LABEL]
        f = open('res_acc.txt', 'w')

        for ones in labelled:
            acc1 = get_acc_label(ones['acc'][0])
            acc2 = get_acc_label(ones['acc'][1])
            classified[acc1 - 1][acc2 - 1] += 1
            if acc1 != acc2:
                f.write('acc1: %s vs acc2: %s\n' %
                        (LA_DICT[acc1], LA_DICT[acc2]))
                f.write('sent1: %s\n' % ones['sent1'])
                f.write('sent2: %s\n\n' % ones['sent2'])
        print(classified)
        for i in range(3):
            s = sum(classified[i])
            if s == 0:
                continue
            for j in range(3):
                classified[i][j] /= s

        df = pandas.DataFrame(columns=['sent1', 'sent2', 'count'])
        for i in range(3):
            for j in range(3):
                df.loc[i * 3 + j] = [LA_DICT[i + 1],
                                     LA_DICT[j + 1], classified[i][j]]
        df = df.pivot('sent1', 'sent2', 'count').astype(float)
        print(df)

        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.pcolor(df, vmin=0, vmax=1)
        plt.title('%s heatmap' % label, fontsize=20)
        plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
        plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
        plt.xlabel('sent2', fontsize=14)
        plt.ylabel('sent1', fontsize=14)
        plt.colorbar()
        plt.savefig('heatmap_%s.png' % label)
        plt.clf()


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
    cat_ent_acc_relation(jsons)
    get_variant_matrix(jsons)
