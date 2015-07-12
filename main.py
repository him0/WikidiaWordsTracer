#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Node import *


class WikipediaWordTracer(object):

    def __init__(self, start_word, goal_word):
        self.start_word = start_word
        self.goal_word = goal_word
        self.nodes = []
        self.picked_words = []

        self.start_node = Node(self.start_word)

    def trace_on(self, try_times=100, show_message=False):
        additional_nodes = [self.start_node]
        for x in range(0, try_times):
            self.__update_nodes(additional_nodes)
            self.__update_minimal_cost_node()

            if show_message:
                print("最短経路確定済み ノード数 : " + str(len(self.picked_words)))
                print("現在の総ノード数 : " + str(len(self.nodes)))
                print("確定 : " + self.minimal_cost_node.name + " (距離 : " + str(
                    self.minimal_cost_node.total_cost) + ")")

            if self.goal_word in self.minimal_cost_node.name:
                return self.minimal_cost_node.words_chane

            self.minimal_cost_node.setup_nodes(show_message)
            additional_nodes = self.minimal_cost_node.nodes

        return None

    def __update_nodes(self, additional_nodes):
        for additional_node in additional_nodes:
            for node in self.nodes:
                if additional_node.name == node.name:
                    if additional_node.total_cost < node.total_cost:
                        self.nodes.remove(node)
                    else:
                        additional_nodes.remove(additional_node)
                        break
        self.nodes += additional_nodes

    def __update_minimal_cost_node(self):
        self.minimal_cost_node = None
        for node in self.nodes:
            if self.minimal_cost_node is None:
                if node.isPicked is False:
                    self.minimal_cost_node = node
            else:
                if node.total_cost < self.minimal_cost_node.total_cost:
                    if node.isPicked is False:
                        self.minimal_cost_node = node
        self.picked_words.append(self.minimal_cost_node.name)
        self.minimal_cost_node.isPicked = True

"""
if __name__ == "__main__":
    print("------------------------")
    print("  WikipediaWordsTracer  ")
    print("------------------------")

    start = input("スタート地点となる ワード >> ")
    start = start.replace(" ", "_")
    goal = input("ゴール地点となる ワード >> ")
    goal = goal.replace(" ", "_")

    print("スタート地点を" + start + "に")
    print("ゴール地点を" + goal + "に設定しました。")
    print("探索を開始します。")

    wwt = WikipediaWordTracer(start, goal)

    result = wwt.trace_on(show_message=True)
    if result is None:
        print("探索を諦めました")
    else:
        print("ゴールを発見しました")
        links_string = result[0]
        for word in result[1:]:
            links_string += " -> "
            links_string += word
        print(links_string)
        print("距離 : " + str(wwt.minimal_cost_node.total_cost))

    print("探索を終了します")
"""