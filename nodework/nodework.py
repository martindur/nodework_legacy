import shutil as sh
import os
from pathlib import Path

class Content:

    def __init__(self, active_dir=None):
        self.active_dir = active_dir

    def __iter__(self):
        if Path(self.active_dir).exists():
            return iter(Path(self.active_dir).iterdir())

    def __contains__(self, file):
        return file in Path(self.active_dir).iterdir()


def node(func):
    def decorator():
        content = Content()
        return func(content)
    return decorator


class Node:

    def __init__(self, work=None):
        self.work = work
        self.next = None


class Graph:

    def __init__(self, input, output=None):
        self.input = input
        self.output = output
        self.content = Content(active_dir=self.input)
        self.head = None
        self.copy = True


    def node(self, func):
        def decorator(graph=None):
            return func(self.content)
        return decorator


    def connect(self, *workers):
        nodes = []
        for work in workers:
            nodes.append(Node(work=work))
        for i, node in enumerate(nodes):
            if i == 0:
                self.head = node

            if i == len(workers)-1:
                return
            node.next = nodes[i+1]


    def run(self):
        if not Path(self.input).exists():
            raise FileNotFoundError

        active_node = self.head
        while active_node is not None:
            active_node.work()
            active_node = active_node.next

        if self.output is not None:
            if not Path(self.output).exists():
                raise FileNotFoundError
            if self.copy:
                for f in Path(self.content.active_dir).iterdir():
                    sh.copyfile(f, Path(self.output) / f.name)

