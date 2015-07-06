#!/usr/bin/env python
# -*- coding: utf-8 -*-

from WikiAccess import *
from Node import *

if __name__=="__main__":
    
    print("----------------------")
    print("  WikidiaWordsTracer  ")
    print("----------------------")
    
    
    startWord = input("スタート地点となる ワード >> ")
    startWord = startWord.replace(" ", "_")
    goalWord = input("ゴール地点となる ワード >> ")
    goalWord = goalWord.replace(" ", "_")

    print("スタート地点を" + startWord + "に")
    print("ゴール地点を" + goalWord + "に設定しました。")
    print("探索を開始します。")
    
    nodes = []
    startNode = Node(startWord)
    nodes.append(startNode)

    minCostNode = startNode
    for x in range(0, 100):
        print("最短経路確定済み ノード数 : " + str(x))

        print("現在の総ノード数 : " + str(len(nodes)))

        minCostNode.isPickuped = True
        print("確定 : " + minCostNode.word + " (距離 : " + str(minCostNode.getCost()) + ")")
        nodes.extend(minCostNode.getNodes(showMessage=True))

        if minCostNode.searchNode(goalWord) is not None:
            print("ゴール 発見")
            print(minCostNode.searchNode(goalWord).getWordsChaneList())
            break

        minCostNode = None
        for node in nodes:
            if minCostNode is None:
                if node.isPickuped is False:
                    minCostNode = node
            else:
                if (node.getCost() < minCostNode.getCost()) and (node.isPickuped is False):
                    minCostNode = node

    if x == 100:
        print("探索を諦めました")
    print("探索を終了しました")
