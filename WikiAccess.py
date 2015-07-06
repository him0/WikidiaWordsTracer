#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import urllib.request
import urllib.parse
import bs4
import re
import xml.sax.saxutils
import os

class WikiAccess:

    def __init__(self, word=None):
        wikiAPI = "https://ja.wikipedia.org/wiki/%(speclial)s/%(keyword)s"
        self.cachePath = "./cache"
        
        if word is None:
            self.word = None #なんか処理する
        else:
            self.word = word.replace(" ", "_")
        
        #wiki独特の記法に対応する処理
        #word = word.split("|")[0]
        
        speclial = urllib.parse.quote_plus("特別:データ書き出し")
        self.keyword = urllib.parse.quote_plus(self.word)
        
        self.url = wikiAPI % {
            "speclial" : speclial,
            "keyword" : self.keyword
        }

    def getReachableWords(self):
        words = []
        fileName = self.keyword[0:50]#長すぎる文字列対策
        if fileName in os.listdir(self.cachePath):
            with open(self.cachePath + "/" + fileName, "r") as content:
                wordsJson = content.read()

            words = json.loads(wordsJson)

        else:
            try:
                with urllib.request.urlopen(self.url) as response:
                    xmlStrings = response.read().decode("utf-8")
            except urllib.error.HTTPError:
                print(self.word)
                

            self.soup = bs4.BeautifulSoup(xmlStrings)
            self.contents = self.soup.findAll("text")

            pattern = re.compile("(?<=\[\[)([^\[\]:]+)(?=\]\])")

            for content in self.contents :
                matchs = pattern.findall(str(content))
                for match in matchs:
                    word = xml.sax.saxutils.unescape(match)
                    word = xml.sax.saxutils.unescape(word)#表記が文字列参照の文字列参照なので2回やらないとダメ
                    word = word.replace(" ", "_")
                    if "|" in word:
                        words.extend(word.split("|")) #wikiのエイリアス表記に対応
                    else:
                        words.append(word)
            words = list(set(words)) #重複消去

            with open(self.cachePath + "/" + fileName, "w") as content:
                content.write(json.dumps(words))

        return words
    

if __name__=="__main__":
    input = input(">>")
    access = WikiAccess(input)
    print(access.url)
    words = access.getReachableWords()
    print(words)