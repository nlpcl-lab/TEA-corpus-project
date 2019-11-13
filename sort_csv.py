import pandas
import argparse
import nltk

from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--csv', type=str,
                    default='./csvs/entail05.contra095.bert.csv')
args = parser.parse_args()


def excludeQuestion(data):
    for i, row in data.iterrows():
        if '?' in row['sent1'] or '?' in row['sent2']:
            data.drop(i, inplace=True)
        elif '!' in row['sent1'] or '!' in row['sent2']:
            data.drop(i, inplace=True)

    return data


def excludeParenthesis(data):
    for i, row in data.iterrows():
        if '(' in row['sent1'] or '(' in row['sent2']:
            data.drop(i, inplace=True)
        elif ')' in row['sent1'] or ')' in row['sent2']:
            data.drop(i, inplace=True)

    return data


def excludeSlash(data):
    for i, row in data.iterrows():
        if '/' in row['sent1'] or '/' in row['sent2']:
            data.drop(i, inplace=True)

    return data


def excludeAt(data):
    for i, row in data.iterrows():
        if '@' in row['sent1'] or '@' in row['sent2']:
            data.drop(i, inplace=True)

    return data


def excludeQuotes(data):
    for i, row in data.iterrows():
        if row['sent1'].count('"') % 2 == 1 or row['sent2'].count('"') % 2 == 1:
            data.drop(i, inplace=True)
        elif row['sent1'].count('“') != row['sent1'].count('”'):
            data.drop(i, inplace=True)
        elif row['sent2'].count('“') != row['sent2'].count('”'):
            data.drop(i, inplace=True)
        elif row['sent1'].find('“') < row['sent1'].find('”'):
            data.drop(i, inplace=True)
        elif row['sent2'].find('“') < row['sent2'].find('”'):
            data.drop(i, inplace=True)

    return data


if __name__ == '__main__':
    data = pandas.read_csv(args.csv, index_col=0).fillna('')
    data.rename(columns={'Unnamed: 0.1': 'no'}, inplace=True)
    data.drop_duplicates(subset='sent1', keep=False, inplace=True)
    data.drop_duplicates(subset='sent2', keep=False, inplace=True)
    data = data[data['sent2'] != False]

    maxlen = list()
    for i, row in tqdm(data.iterrows(), total=data.shape[0]):
        maxlen.append(max(len(row['sent1']), len(row['sent2'])))

    data['maxlen'] = maxlen
    data.sort_values(['maxlen'], inplace=True)
    data = excludeAt(excludeSlash(excludeParenthesis(excludeQuestion(data))))
    data = data.head(500)

    bleu_scores = list()
    for i, row in tqdm(data.iterrows(), total=data.shape[0]):
        sent1_words = nltk.word_tokenize(row['sent1'])
        sent2_words = nltk.word_tokenize(row['sent2'])
        bleu_scores.append(nltk.translate.bleu_score.sentence_bleu(
            [sent1_words], sent2_words))
    data['bleu_score'] = bleu_scores

    data.sort_values(['bleu_score'], inplace=True, ascending=False)
    data = excludeQuotes(data)
    data = data.head(140)

    data.to_csv('%s.sorted.csv' % args.csv[:-4], index=False)
