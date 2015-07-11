#!/usr/bin/env python
# -*- coding: utf-8 -*-

from WikiAccess import *
from Node import *

if __name__ == "__main__":

    print("------------------------")
    print("  WikipediaWordsTracer  ")
    print("------------------------")

    start_word = input("スタート地点となる ワード >> ")
    start_word = start_word.replace(" ", "_")
    goal_word = input("ゴール地点となる ワード >> ")
    goal_word = goal_word.replace(" ", "_")

    print("スタート地点を" + start_word + "に")
    print("ゴール地点を" + goal_word + "に設定しました。")
    print("探索を開始します。")

    nodes = []
    picked_words = []
    start_node = Node(start_word)
    nodes.append(start_node)

    minimal_cost_node = start_node
    for x in range(0, 100):
        print("最短経路確定済み ノード数 : " + str(x))
        print("現在の総ノード数 : " + str(len(nodes)))

        picked_words.append(minimal_cost_node.name)
        minimal_cost_node.isPicked = True

        print("確定 : " + minimal_cost_node.name + " (距離 : " + str(
            minimal_cost_node.total_cost) + ")")

        if goal_word in minimal_cost_node.name:
            print("ゴール 発見")
            words = minimal_cost_node.words_chane
            links_string = words[0]
            for word in words[1:]:
                links_string += " -> "
                links_string += word
            print(links_string)
            print("距離 : " + str(minimal_cost_node.total_cost))
            break

        minimal_cost_node.setup_nodes(True)
        additional_nodes = minimal_cost_node.nodes

        for additional_node in additional_nodes:
            for node in nodes:
                if additional_node.name == node.name:
                    if additional_node.total_cost < node.total_cost:
                        nodes.remove(node)
                    else:
                        additional_nodes.remove(additional_node)
                        break
        nodes += additional_nodes

        minimal_cost_node = None
        for node in nodes:
            if minimal_cost_node is None:
                if node.isPicked is False:
                    minimal_cost_node = node
            else:
                if node.total_cost < minimal_cost_node.total_cost:
                    if node.isPicked is False:
                        minimal_cost_node = node

    print("探索を終了します")
