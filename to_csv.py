import os
import glob
import argparse
import pandas

import xml.etree.ElementTree as elemTree

from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str,
                    default='../../Downloads/buzzfeed/articles')
args = parser.parse_args()

if __name__ == '__main__':
    df = pandas.DataFrame(
        columns=['title', 'url', 'text', 'sent1', 'sent2', 'entailment', 'accp1', 'accp2'])

    articles = os.path.join(args.path, '*.xml')
    for article in tqdm(sorted(glob.glob(articles))):
        xml = elemTree.parse(article)
        df = df.append({
            'title': xml.find('./title').text,
            'url': xml.find('./uri').text,
            'text': xml.find('./mainText').text},
            ignore_index=True)

    df.to_csv('buzzfeed.csv', na_rep='')
