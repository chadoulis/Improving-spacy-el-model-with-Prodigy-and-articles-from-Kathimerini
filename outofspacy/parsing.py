import feedparser
import pandas as pd
import datetime
import json


class parsing:

    def __init__(self, filename = r'outofspacy/data/greeknews.jsonl', csv_dir = r'outofspacy/data/gd.csv'):
        self.filename = filename
        self.csv_dir = csv_dir

    def construct_list(self):

        with open(self.filename, 'r') as fp:
            dictionary = json.load(fp)
            lista = []
            for k in dictionary.keys():
                lista.append(dictionary[k])
        return lista

    def parse_from_rss_list(self, rss_list):
        """
        Parses rss links
        :param rss_list:
        :return:
        """

        df = pd.DataFrame(columns=['title', 'Date', 'url'])
        frames = []
        for url in rss_list:
            frames.append(self.parse_rss(url))
        df = pd.concat(frames)
        df = df.reset_index(drop=True)
        df.to_csv(self.csv_dir)
        return df

    def parse_rss(self, url):
        """

        :param url:
        :return:
        """
        feed = feedparser.parse(url)
        posts = []
        for post in feed.entries:
            date_time_str = post.published
            try:
                date_time_obj = datetime.datetime.strptime(date_time_str, '%a, %d %b %Y %H:%M:%S %z')
            except:
                date_time_obj = datetime.datetime.strptime(date_time_str, '%a, %d %b %Y %H:%M:%S %Z')
            posts.append((post.title, date_time_obj.date(), post.link))

        df = pd.DataFrame(posts, columns=['title', 'Date', 'url'])
        return df
