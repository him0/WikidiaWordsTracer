#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import bs4
import re
import xml.sax.saxutils
import os


class WikiAccess(object):
    def __init__(self, query=None):
        WikiAccess.WIKI_API = "https://ja.wikipedia.org/wiki/%(special)s/%(keyword)s"
        WikiAccess.CACHE_PATH = "./cache"

        self.word = query.replace(" ", "_")

        special = urllib.parse.quote_plus("特別:データ書き出し")
        self.word_key = urllib.parse.quote_plus(self.word)

        self.url = WikiAccess.WIKI_API % {
            "special": special,
            "keyword": self.word_key
        }

        self.reachable_words = []
        self.__setup_reachable_words()

    def __setup_reachable_words(self):
        file_name = self.word_key[0:50]  # 長すぎる文字列対策
        if file_name in os.listdir(WikiAccess.CACHE_PATH):
            with open(WikiAccess.CACHE_PATH + "/" + file_name, "r") as content:
                self.reachable_words = content.read()
        else:
            self.reachable_words = self.__get_words_via_http()

            with open(WikiAccess.CACHE_PATH + "/" + file_name, "w") as content:
                content.write(json.dumps(self.reachable_words))

    def __get_words_via_http(self):
        try:
            with urllib.request.urlopen(self.url) as response:
                xml_strings = response.read().decode("utf-8")
        except urllib.error.HTTPError:
            print(self.word)

        soup = bs4.BeautifulSoup(xml_strings)
        contents = soup.findAll("text")

        pattern = re.compile("(?<=\[\[)([^\[\]:]+)(?=\]\])")

        for content in contents:
            matches = pattern.findall(str(content))

            # wikiのエイリアス表記に対応
            for match in matches:
                link_word = self.__word_fix(match)
                if "|" in link_word:
                    self.reachable_words.extend(link_word.split("|"))
                else:
                    self.reachable_words.append(link_word)

        unique_words = []
        for word in self.reachable_words:
            if word not in unique_words:
                unique_words.append(word)

        return unique_words

    def __word_fix(self, complex_word):
        # 表記が文字列参照の文字列参照なので2回やらないとダメ
        complex_word = xml.sax.saxutils.unescape(complex_word)
        complex_word = xml.sax.saxutils.unescape(complex_word)

        complex_word = complex_word.replace("km&sup2", "平方キロメートル")
        complex_word = complex_word.replace("m&sup2", "平方メートル")
        complex_word = complex_word.replace("mi&sup2", "平方マイル")
        complex_word = complex_word.replace("}}", "")  # 謎 }}lang 対策
        complex_word = complex_word.replace("{{", "")  # 謎 {{IPA 対策
        # 謎 ナノアーケウム<br_/>・エクインタンス 対策
        # 謎 '''アーケ<br_/>プラスチダ''' 対策
        complex_word = complex_word.replace("'''", "")
        complex_word = complex_word.replace("<br_/>", "")
        complex_word = complex_word.replace("<br_/>", "")  # 1回でやりきれないとき？用
        # 謎 ビタミンB<sub>6</sub> 対策
        complex_word = complex_word.replace("<sub>6</sub>", "6")
        complex_word = complex_word.replace("<nowiki>C#</nowiki>", "C#")
        simple_word = complex_word.replace(" ", "_")

        return simple_word

"""
if __name__ == "__main__":
    word = input(">>")
    access = WikiAccess(word)
    print(access.url)
    words = access.reachable_words
    print(words)
"""