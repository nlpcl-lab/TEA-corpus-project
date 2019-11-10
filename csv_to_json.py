import os
import argparse
import json
import pandas

from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--csv', type=str,
                    default='./csvs/entail05.contra095.bert.csv')
parser.add_argument('--out', type=str, default='./jsons')
args = parser.parse_args()

if __name__ == '__main__':
    data = pandas.read_csv(args.csv, index_col=False).fillna('')
    en_json = list()
    ac_json = list()

    for i, row in tqdm(data.iterrows(), total=data.shape[0]):
        if (row['sent2'] == 'False'):
            continue

        en_json.append({
            'no': i,
            'title': row['title'],
            'url': row['url'],
            'body': row['text'],
            'text': row['sent1'],
            'hypothesis': row['sent2']
        })

        ac_json.append({
            'no': i * 2,
            'title': row['title'],
            'url': row['url'],
            'body': row['text'],
            'sentence': row['sent1']
        })
        ac_json.append({
            'no': i * 2 + 1,
            'title': row['title'],
            'url': row['url'],
            'body': row['text'],
            'sentence': row['sent2']
        })

    en_fname = '%s.en.json' % args.csv.split('/')[-1][:-4]
    ac_fname = '%s.ac.json' % args.csv.split('/')[-1][:-4]

    with open(os.path.join(args.out, en_fname), 'w', encoding='utf8') as f:
        json.dump(en_json, f)
        print('Written entailment data at %s' %
              os.path.join(args.out, en_fname))
    with open(os.path.join(args.out, ac_fname), 'w', encoding='utf8') as f:
        json.dump(ac_json, f)
        print('Written acceptability data at %s' %
              os.path.join(args.out, en_fname))
