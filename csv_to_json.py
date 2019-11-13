import os
import argparse
import json
import pandas

from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--csv', type=str,
                    default='./csvs/entail05.contra095.bert.sorted.csv')
parser.add_argument('--out', type=str, default='./jsons')
args = parser.parse_args()

if __name__ == '__main__':
    data = pandas.read_csv(args.csv, index_col=False).fillna('')
    en_json = dict()
    ac_json = dict()

    en_idxs = list()
    ac_idxs = list()

    for i, row in tqdm(data.iterrows(), total=data.shape[0]):
        if (row['sent2'] == 'False'):
            continue

        en_json[int(row['no'])] = {
            'no': row['no'],
            'title': row['title'],
            'url': row['url'],
            'body': row['text'],
            'text': row['sent1'],
            'hypothesis': row['sent2']
        }
        en_idxs.append(int(row['no']))

        ac_json[int(row['no']) * 2] = {
            'no': int(row['no']) * 2,
            'title': row['title'],
            'url': row['url'],
            'body': row['text'],
            'sentence': row['sent1']
        }
        ac_json[int(row['no']) * 2 + 1] = {
            'no': int(row['no']) * 2 + 1,
            'title': row['title'],
            'url': row['url'],
            'body': row['text'],
            'sentence': row['sent2']
        }
        ac_idxs.append(int(row['no']) * 2)
        ac_idxs.append(int(row['no']) * 2 + 1)

    en_df = pandas.DataFrame(data=en_idxs, columns=['no'])
    ac_df = pandas.DataFrame(data=ac_idxs, columns=['no'])

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
    en_df.to_csv(os.path.join(args.out, en_fname + '.csv'), index=False)
    ac_df.to_csv(os.path.join(args.out, ac_fname + '.csv'), index=False)
