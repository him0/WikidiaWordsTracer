#!/usr/bin/env python
# -*- coding: utf-8 -*-

from WikiAccess import *
from ProgressBar import *
import threading
import queue
import time


class Node(object):
    def __init__(self, word, preNode=None):
        self.word = word
        self.__preNode = preNode

        wikiAccess = WikiAccess(word)
        self.reachableWords = wikiAccess.getReachableWords()
        self.isPickuped = False

        self.__threads = queue.Queue()

    def getNodes(self, showMessage=False):
        self.nodes = []
        self.doneThreadCount = 0
        numOfWords = len(self.reachableWords)

        if numOfWords != 0 and showMessage:
            print(self.word + " から参照されるノードの数 " + str(numOfWords))

        for word in self.reachableWords:
            thread = threading.Thread(target=self.makeNode, args=(word,))
            thread.setDaemon(False)
            self.__threads.put(thread)

        while not self.__threads.empty():
            thread = self.__threads.get()
            thread.start()

        #すべてのスレッドの終了を確認する
        while self.doneThreadCount != numOfWords:
            time.sleep(1)

        return (self.nodes)

    def makeNode(self, word):
        self.nodes += [Node(word, self)]
        self.doneThreadCount = self.doneThreadCount + 1

    def searchNode(self, word):
        for node in self.nodes:
            if word in node.word:
                return (node)

        return None

    @property
    def totalCost(self):
        if self.__preNode is None:
            cost = 0
        else:
            cost = self.__preNode.totalCost + \
                   list(self.__preNode.reachableWords).index(self.word) + 1
        return cost

    @property
    def wordsChaneList(self):
        if self.__preNode is None:
            return ([self.word])
        else:
            list = self.__preNode.wordsChaneList
            list += [self.word]
            return list


if __name__ == "__main__":
    word = input(">>")
    n = Node(word)
    print(n.reachableWords)
    nodes = n.getNodes()
    print(nodes[0].totalCost)
    print(nodes[0].getWordsChane())
