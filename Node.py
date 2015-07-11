#!/usr/bin/env python
# -*- coding: utf-8 -*-

from WikiAccess import *
import threading
import queue
import time


class Node(object):
    def __init__(self, node_name, pre_node=None):
        self.name = node_name
        self.__pre_node = pre_node
        self.isPicked = False

        self.nodes = []
        self.__threads = queue.Queue()
        self.__done_thread_count = 0

        wikipedia_access = WikiAccess(node_name)
        self.reachable_node_names = wikipedia_access.reachable_words

    def setup_nodes(self, show_message=False):
        num_of_words = len(self.reachable_node_names)

        if 0 != num_of_words and show_message:
            print(self.name + " から参照されるノードの数 " + str(num_of_words))

        for name in self.reachable_node_names:
            thread = threading.Thread(target=self.makeNode, args=(name,))
            thread.setDaemon(False)
            self.__threads.put(thread)

        while not self.__threads.empty():
            thread = self.__threads.get()
            thread.start()

        # すべてのスレッドの終了を確認する
        while num_of_words != self.__done_thread_count:
            time.sleep(1)

    def makeNode(self, node_name):  # Thread関係なので命名規則が違う
        self.nodes += [Node(node_name, self)]
        self.__done_thread_count += 1

    @property
    def total_cost(self):
        if self.__pre_node is None:
            cost = 0
        else:
            cost = self.__pre_node.total_cost + \
                list(self.__pre_node.reachable_node_names).index(self.name) + 1
        return cost

    @property
    def words_chane(self):
        if self.__pre_node is None:
            return [self.name]
        else:
            word_chane = self.__pre_node.words_chane
            word_chane += [self.name]
            return word_chane

"""
if __name__ == "__main__":
    word = word(">>")
    n = Node(word)
    n.setup_nodes(True)
    print(n.reachable_node_names)
    nodes = n.nodes
    print(nodes[0].total_cost)
    print(nodes[0].WordsChane)
"""