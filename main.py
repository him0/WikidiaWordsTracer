#!/usr/bin/env python
# -*- coding: utf-8 -*-

from WikiAccess import *
from Node import *

if __name__ == "__main__":

    print("----------------------")
    print("  WikipediaWordsTracer  ")
    print("----------------------")

    startWord = input("スタート地点となる ワード >> ")
    startWord = startWord.replace(" ", "_")
    goalWord = input("ゴール地点となる ワード >> ")
    goalWord = goalWord.replace(" ", "_")

    print("スタート地点を" + startWord + "に")
    print("ゴール地点を" + goalWord + "に設定しました。")
    print("探索を開始します。")

    nodes = []
    pickedupedWords = []
    startNode = Node(startWord)
    nodes.append(startNode)

    minCostNode = startNode
    for x in range(0, 100):
        print("最短経路確定済み ノード数 : " + str(x))
        print("現在の総ノード数 : " + str(len(nodes)))

        # todo 同じwordについてのノード2回めに作成された際の処理
        pickedupedWords.append(minCostNode.word)
        minCostNode.isPickuped = True
        # for node in nodes:
        #    print("ノード : " + node.word + " (距離 : " + str(node.getCost()) + ")")

        print("確定 : " + minCostNode.word + " (距離 : " + str(
            minCostNode.getCost) + ")")

        additionalNodes = minCostNode.getNodes(showMessage=True)
        for additionalNode in additionalNodes:
            for node in nodes:
                if additionalNode.word == node.word:
                    if additionalNode.getCost < node.getCost:
                        nodes.remove(node)
                    else:
                        additionalNodes.remove(additionalNode)
                        break
        nodes += additionalNodes

        if minCostNode.word == goalWord:
            print("ゴール 発見")
            links = minCostNode.searchNode(goalWord).getWordsChaneList()
            linksString = links[0]
            for link in links[1:]:
                linksString += " -> "
                linksString += link
            print(linksString)
            print("距離 : " + str(minCostNode.getCost))
            break

        minCostNode = None
        for node in nodes:
            if minCostNode is None:
                if node.isPickuped is False:
                    minCostNode = node
            else:
                if (node.getCost < minCostNode.getCost) and (
                            node.isPickuped is False):
                    minCostNode = node

    if x == 100:
        print("探索を諦めました")
    print("探索を了しました")
