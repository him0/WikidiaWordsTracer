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
        numOfWords = len(self.reachableWords)

        if numOfWords != 0 and showMessage:
            # progressBar = ProgressBar(numOfWords) #作ってみたものの微妙な感じ
            print(self.word + " から参照されるノードの数 " + str(numOfWords))

        for word in self.reachableWords:
            thread = threading.Thread(target=self.makeNode, args=(word,))
            self.__threads.put(thread)

        startedThreadCount = 0
        numOfParallelThread = 50

        while not self.__threads.empty():
            for x in range(0, numOfParallelThread):
                if self.__threads.empty():
                    break
                thread = self.__threads.get()
                thread.start()
                startedThreadCount = startedThreadCount + 1

            while startedThreadCount != len(self.nodes):
                time.sleep(1)

        return (self.nodes)

    def makeNode(self, word):
        self.nodes += [Node(word, self)]

    def searchNode(self, word):
        for node in self.nodes:
            if node.word == word:
                return (node)

        return (None)

    @property
    def getCost(self):
        if self.__preNode is None:
            cost = 0
        else:
            cost = self.__preNode.getCost + \
                   list(self.__preNode.nodes).index(self) + 1
        return (cost)

    def getWordsChane(self, chaneString=""):
        if self.__preNode is None:
            print(self.word + chaneString)
        else:
            nextChaneString = " -> " + self.word + chaneString
            self.__preNode.getWordsChane(nextChaneString)

    def getWordsChaneList(self):
        if self.__preNode is None:
            return ([self.word])
        else:
            list = self.__preNode.getWordsChaneList()
            list += [self.word]
            return (list)


if __name__ == "__main__":
    word = input(">>")
    n = Node(word)
    print(n.reachableWords)
    nodes = n.getNodes()
    print(nodes[0].getCost)
    print(nodes[0].getWordsChane())
