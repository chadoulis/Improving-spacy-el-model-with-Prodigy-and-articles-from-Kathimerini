import spacy
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import json
from urllib.request import urlopen
import sys
import os

# Loading gsoc2018-spacy
nlp = spacy.load('el_core_news_sm')

class preprocessing:

    def __init__(self, elements="articles", n_elements=10, csv_filename=r'outofspacy/data/datakathimerinh.csv', filename = 'result'):
        self.n_elements = n_elements
        self.elements = elements
        self.csv_filename = csv_filename
        self.filename = filename

    def parsing_n_elements(self):
        '''
        Parses either n articles or n sentences.

        Returns:
            df2: pd.DataFrame with the Body of each article and the number of sentences it consists of.

        '''
        file = pd.read_csv(self.csv_filename)
        df = pd.DataFrame(file)
        df2 = pd.DataFrame()
        df2 = pd.DataFrame(columns=['Article Body'])
        if self.elements == "articles":
            numberofsentences = []
            totalnumberofsentences = 0
            for i in range(self.n_elements):
                url = df.url[i]
                try:
                    html = urlopen(url)
                    soup = BeautifulSoup(html, "html.parser")
                    text = soup.find('div', attrs={'class':'freetext'}).text
                except:
                    pass

                b = text.split("\nΠηγή:")[0]
                df2.loc[i] = b
                totalnumberofsentences += len(sent_tokenize(b))
                numberofsentences.append(len(sent_tokenize(b)))
                sys.stdout.write("\r {}-th out of {} articles parsed.".format(i+1, self.n_elements))
            preprocessing.print_pr_results(self, totalnumberofsentences)
            df2['Number of Sentences'] = numberofsentences
        if self.elements == "sentences":
            i = 0
            totalnumberofsentences = 0
            numberofsentences = []
            while sum(numberofsentences) < self.n_elements:
                url = df.url[i]
                try:
                    html = urlopen(url)
                    soup = BeautifulSoup(html, "html.parser")
                    text = soup.find('div', attrs={'class': 'freetext'}).text
                except:
                    pass

                b = text.split("\nΠηγή:")[0]
                df2.loc[i] = b
                totalnumberofsentences += len(sent_tokenize(b))
                numberofsentences.append(len(sent_tokenize(b)))
                i += 1
                sys.stdout.write("\r{} sentences out of {} sentences parsed.".format(totalnumberofsentences, self.n_elements))
            print(" The last {} sentences from the last article were omitted.\n".format(totalnumberofsentences - self.n_elements))
            preprocessing.print_pr_results(self, i)
            df2['Number of Sentences'] = numberofsentences
            lastarticle = str(df2.iloc[-1, 0]).split(".")[:(numberofsentences[-1] - totalnumberofsentences + self.n_elements)]
            lastarticle2 = '-'.join(lastarticle)
            df2.iloc[-1, 0] = lastarticle2
            df2.iloc[-1, 1] = numberofsentences[-1] - totalnumberofsentences + self.n_elements
        return df2


    def final_text(self, df2):
        '''
        Creates the string variable of the final text

        Args:
            df2: pd.Dataframe

        '''
        ft = ""
        for i in range(len(df2)):
            ft += ' ' + df2.iloc[i, 0]
        return ft

    def remove_nobreakspace(self, ft):
        '''
        Removes the no-break character from the final text string variable.
        
        Args:
            ft: The final text string variable.

        '''
        ft = ft.replace(u'\xa0', u' ')
        ft = ft.replace(u'\n', u' ')
        return ft


    def print_pr_results(self, noem):
        """
        Prints the event log during parsing
        :param noem: The number of elements (either articles or sentences) collected.
        :return:
        """
        message_1 = "Collected {} sentences from {} articles!\n"
        message_2 = "Average number of sentences per article: {}\n"

        if self.elements == "articles":
            print(message_1.format(noem, self.n_elements))
            print(message_2.format(noem/self.n_elements))

        elif self.elements == "sentences":
            print(message_1.format(self.n_elements, noem))
            print(message_2.format(self.n_elements/noem))


    def preprocess(self):
        dataframe = preprocessing.parsing_n_elements(self)
        keimeno = preprocessing.final_text(self, dataframe)
        keimeno = preprocessing.remove_nobreakspace(self, keimeno)
        return keimeno

    def save_as_txt(self, name):

        with open(self.filename + "_pure_text.txt", "w", encoding="utf-8") as text_file:
            text_file.write(preprocessing.preprocess(self))

    def create_json(self):
        """
        Creates a json file which can be then used by prodigy in order to further train the greek spacy model.
        :return:
        """
        final = preprocessing.preprocess(self)

        #final = ' '.join(keimeno)
        if len(final) < 1000000:
            doc = nlp(final)
            jsonfile = doc.to_json()
            with open(self.filename + '.jsonl', 'w') as fp:
                json.dump(jsonfile, fp)
        else:
            print("""Text of length {} exceeds maximum of 1000000. The v2.x parser and NER models require roughly 
            1GB of temporary memory per 100,000 characters in the input. This means long texts may cause memory 
            allocation errors.""".format(len(final)))
            limit = 999998
            k = len(final)//limit+1
            final_list = final.split(".")
            chunks = list(np.array_split(np.array(final_list), k))
            d = {}
            for z in range(k):
                doc = nlp(' '.join(chunks[z]))
                print(len(' '.join(chunks[z])))
                jsonfile = doc.to_json()
                with open(self.filename + str(z+1) + '.jsonl' , 'w') as fp:
                    json.dump(jsonfile, fp)

    def load_json(self):
        """
        Loads a json file, saved from a previous session.
        :return:
        """
        with open('json_files/result.jsonl', 'r') as fp:
            jsonfile = json.load(fp)
        return jsonfile
