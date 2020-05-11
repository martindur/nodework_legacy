import shutil as sh
from pathlib import Path

class Content:

    def __init__(self):
        self.copy = True



def node(func):
    def decorator():
        content = Content()
        return func(content)
    return decorator


class Node:

    def __init__(self):
        self.nodes = []
        self.node = None


class Graph():

    def __init__(self, input_=None, output=None):
        self.entryNode = Node()
        self.exitNode = Node()

        self.input = input_
        self.output = output

        self.nodes = []


    def connect(self, *nodes):
        prev_node = self.entryNode
        for i, n in enumerate(nodes):
            node = Node()
            node.node = n
            prev_node.nodes.append(node)
            prev_node = node

            self.nodes.append(node)

            if i == len(nodes)-1:
                node.nodes.append(self.exitNode)



    def run(self):
        if self.input is None or self.output is None:
            raise TypeError

        if not Path(self.input).exists():
            raise FileNotFoundError

