# -*- coding: utf-8 -*-

import math
import codecs
import glob
import jieba
from collections import Counter, defaultdict
from utils import vector_cos, dict_top_by_value

with codecs.open('stopwords_en_ch.txt', 'r', 'utf-8') as f:
    STOPWORD = {w.strip() for w in f.readlines() if w.strip() != ''}
with codecs.open('punctuations.txt', 'r', 'utf-8') as f:
    PUNCTUATION = {w.strip() for w in f.readlines() if w.strip() != ''}


class Article:
    def __init__(self, filename):
        with codecs.open(filename, 'r', 'utf-8') as f:
            self.filename = filename
            self.segmented_list = [w.strip() for w in jieba.cut(f.read()) if w.strip() != '']
            self.cleaned_list = [w for w in self.segmented_list if (w not in STOPWORD) and (w not in PUNCTUATION)]
            self.tf_dict = Counter(self.cleaned_list)
            # Normalize term frequency by total number of term occurrences
            for k in self.tf_dict:
                self.tf_dict[k] = float(self.tf_dict[k]) / len(self.cleaned_list)


def tf_idf(tf_dict, idf_dict):
    return {k: v * idf_dict[k] for k, v in tf_dict.items() if k in idf_dict}


def similarity(articles, num_top_term=0):
    # Gather terms to be used to calculate cosine similarity
    terms = set()
    for article in articles.values():
        tfidf_dict = tf_idf(article.tf_dict, idf_dict)
        top_list = dict_top_by_value(tfidf_dict, num_top_term)
        terms.update(top_list)

    # Calculate cosine similarity
    _sim_matrix = defaultdict(dict)
    other = articles.keys()
    for a1 in articles.values():
        other.remove(a1.filename)
        for filename in other:
            a2 = articles[filename]
            a1v = []
            a2v = []
            for term in terms:
                a1v.append(a1.tf_dict[term] if term in a1.tf_dict else 0)
                a2v.append(a2.tf_dict[term] if term in a2.tf_dict else 0)
            _sim_matrix[a1.filename][a2.filename] = vector_cos(a1v, a2v)
    return _sim_matrix


if __name__ == '__main__':
    # Initialize article objects and calculate term frequency (TF)
    articles = {}
    for filename in glob.glob("data/*.txt"):
        article = Article(filename)
        articles[article.filename] = article
        print ('File name: ' + article.filename)
        print ('Segmented list: ' + '/ '.join(article.segmented_list))
        print ('Cleaned list: ' + '/ '.join(article.cleaned_list))
        print 'Term frequency:',
        for term in sorted(article.tf_dict, key=article.tf_dict.get, reverse=True):
            print u'{}:{}/'.format(term, article.tf_dict[term]),
        print('\n')

    # Calculate inverse document frequency (IDF)
    idf_dict = {}
    for article in articles.values():
        for term in article.tf_dict:
            if term in idf_dict:
                idf_dict[term] += 1
            else:
                idf_dict[term] = 1

    num_doc = len(idf_dict)
    idf_dict = {k: math.log10(float(num_doc) / (v + 1)) for k, v in idf_dict.items()}

    print 'Inverse document frequency:',
    for w in sorted(idf_dict, key=idf_dict.get, reverse=True):
        print u'{}:{}/'.format(w, idf_dict[w]),
    print('\n')

    # Output TF-IDF values for articles
    for article in articles.values():
        tfidf_dict = tf_idf(article.tf_dict, idf_dict)
        top_list = dict_top_by_value(tfidf_dict, 20)
        print ('File name: ' + article.filename)
        print 'TF-IDF:',
        for w in sorted(tfidf_dict, key=tfidf_dict.get, reverse=True):
            print u'{}:{}/'.format(w, tfidf_dict[w]),
        print('\n')

    # Calculate pairwise document similarity
    sim = similarity(articles, 20)
    for a1 in sim.keys():
        for a2 in sim[a1].keys():
            print('similarity({}, {}) = {}'.format(a1, a2, sim[a1][a2]))
        print
