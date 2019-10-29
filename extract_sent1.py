'Extract first sentences from each news article.'

import pandas
import argparse
import spacy

from tqdm import tqdm

NLP = spacy.load('en_core_web_sm')

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, default='./buzzfeed.csv')
args = parser.parse_args()

if __name__ == '__main__':
    data = pandas.read_csv(args.path).fillna('')
    sents = list()

    for idx, row in tqdm(data.iterrows(), total=data.shape[0]):
        if len(row['text']) < 1:
            data.drop(idx, inplace=True)
            continue
        doc = NLP(row['text'])
        sents.append(list(doc.sents)[0].string.strip())

    data['sent1'] = sents
    data.to_csv('buzzfeed_sent1.csv', na_rep='')
