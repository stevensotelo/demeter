import os
import spacy
import pandas

#print(os.path.dirname(spacy.__file__))

nlp = spacy.load('es_core_news_sm')

l = "Nuevos detalles sobre la investigación de la muerte de Juliana Giraldo, la mujer que falleció luego de ser impactada por un disparo de un soldado del Ejército en Miranda, Cauca, se dieron a conocer en las últimas horas."
doc = nlp(l)
[print(token.text, token.pos_, token.tag_, token.lemma_, token.is_stop) for token in doc]


'''
# BERT

import pandas as pd

# Parameters
root = "G:\\Me\\Code\\UOC\\TFM\\demeter\\src\\"
inputs = root + "data\\english\\yelp_review_polarity_csv\\"
outputs = root + "test\\src\\outputs"

# test vars
train_file = inputs + "train.csv"
test_file = inputs + "test.csv"

# Preprocessing data
train_df = pd.read_csv(train_file, header=None)
train_df.head()

test_df = pd.read_csv(test_file, header=None)
test_df.head()

train_df[0] = (train_df[0] == 2).astype(int)
test_df[0] = (test_df[0] == 2).astype(int)

# Formatting for bert

train_df_bert = pd.DataFrame({
    'id':range(len(train_df)),
    'label':train_df[0],
    'alpha':['a']*train_df.shape[0],
    'text': train_df[1].replace(r'\n', ' ', regex=True)
})
train_df_bert.head()

dev_df_bert = pd.DataFrame({
    'id':range(len(test_df)),
    'label':test_df[0],
    'alpha':['a']*test_df.shape[0],
    'text': test_df[1].replace(r'\n', ' ', regex=True)
})
dev_df_bert.head()

train_df_bert.to_csv('data/train.tsv', sep='\t', index=False, header=False)
dev_df_bert.to_csv('data/dev.tsv', sep='\t', index=False, header=False)
'''