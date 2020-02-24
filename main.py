import spacy
import nltk
#nltk.download('punkt')
#nlp = spacy.load('el_core_news_sm')


# Part 1 - Preprocessing
import outofspacy as oos
pr = oos.preprocessing("sentences", 100, r'outofspacy\data\gd.csv','result')
pr.create_json()
#pr.create_json()

#Part 2
#subprocess.call('python -m prodigy ner.make-gold result_gold el_core_news_sm result.jsonl')


# Part 2 - Improving model


# 2.1. Improving existing Categories

# Starting the server to begin annotating
#a = 'python -m prodigy ner.teach d el_core_web_sm result.jsonl --label "ORG, PERSON, LOC, GPE, EVENT, PRODUCT"'
#subprocess.call(a)

#key = None
#while key != "y":
    #key = input("Continue? ")

# Training the model
#b = 'python -m prodigy ner.batch-train ds el_core_web_sm --label ORG, PERSON, LOC, GPE, EVENT, PRODUCT --output /tmp/model --n-iter 10 --eval-split 0.2 --dropout 0.2'
#subprocess.call(b)

# 2.2. Labeling Spans in text

#Starting the server to begin labeling
#subprocess.call('python -m prodigy ner.manual data_set /tmp/model result.jsonl --label "THESMIKI_IDIOTITA"')

#Exporting the data
#subprocess.call('python -m prodigy db-out your_dataset_3 > /annotations.jsonl')

# 2.3. Adding new category

# 2.2. Improving existing Categories






