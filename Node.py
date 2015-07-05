#!/usr/bin/env python
# -*- coding: utf-8 -*-

from WikiAccess import *
from ProgressBar import *

class Node(object):
    
    def __init__(self, word, preNode=None):
        self.word = word
        self.__preNode = preNode
        
        wikiAccess = WikiAccess(word)
        self.reachableWords = wikiAccess.getReachableWords()
        self.isPickuped = False

    def getNodes(self, showMessage=False):
        self.nodes = []
        numOfWords = len(self.reachableWords)

        if numOfWords != 0 and showMessage:
            #progressBar = ProgressBar(numOfWords) #作ってみたものの微妙な感じ
            print(self.word + " から参照されるノードの数 " + str(numOfWords))

        for word in self.reachableWords:
            self.nodes += [Node(word, self)]
            timing = 50 #50語ノード化するたびにメッセージ
            if self.reachableWords.index(word) % timing == 0 and self.reachableWords.index(word) != 0 and showMessage:
                print(str(self.reachableWords.index(word)) + " ワード ノード化 完了")
            #if numOfWords != 0:
                #progressBar.update() #作ってみたものの微妙な感じ
            #if self.__preNode is None:
            #    print(word)
            #else:
            #    print(self.word + " -> " + word)
        return(self.nodes)
    
    def searchNode(self, word):
        for node in self.nodes:
            if node.word == word:
                return(node)
        
        return(None)
    
    def getCost(self):
        if self.__preNode is None:
            cost = 0
        else:
            cost = self.__preNode.getCost() + list(self.__preNode.nodes).index(self) + 1
    
        return(cost)
    
    def getWordsChane(self, chaneString=""):
        
        if self.__preNode is None:
            print (self.word + chaneString)
        else:
            nextChaneString = " -> " + self.word + chaneString
            self.__preNode.getWordsChane(nextChaneString)
    
    def getWordsChaneList(self):
        
        if self.__preNode is None:
            return([self.word])
        else:
            list = self.__preNode.getWordsChaneList()
            list += [self.word]
            return(list)
    
if __name__=="__main__":
    word = input(">>")
    n = Node(word)
    print(n.reachableWords)
    nodes = n.getNodes()
    print(nodes[0].getCost())
    print(nodes[0].getWordsChane())