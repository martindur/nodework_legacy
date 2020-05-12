import shutil as sh
from pathlib import Path

class Content:

    def __init__(self, active_dir=None):
        self.active_dir = active_dir

    def __iter__(self):
        if Path(self.active_dir).exists():
            return iter(Path(self.active_dir).iterdir())


def node(func):
    def decorator():
        content = Content()
        return func(content)
    return decorator


class Node:

    def __init__(self):
        self.input = None
        self.output = None
        self.work = None


class Graph():

    def __init__(self, input=None, output=None):
        self.input = input
        self.output = output
        self.nodes = []

        self.entryNode = Node()
        self.exitNode = Node()

        self.copy = True

        self.nodes.append(self.entryNode)
        self.nodes.append(self.exitNode)


    def connect(self, work):
        node = Node()
        node.work = work
        self.nodes.append(node)
        self.nodes.append(self.nodes.pop(self.nodes.index(self.entryNode)))


    def run(self):
        if self.input is None or self.output is None:
            raise TypeError

        if not Path(self.input).exists():
            print(Path(self.input))
            raise FileNotFoundError

        if self.copy:
            for f in Path(self.input).iterdir():
                sh.copyfile(f, Path(self.output) / f.name)

