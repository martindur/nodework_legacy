import shutil as sh
from pathlib import Path

class Content:
    pass


def node(func):
    def decorator():
        content = Content()
        return func(content)
    return decorator


class Node:

    def __init__(self):
        self.input = None
        self.output = None
        self.node = None


class Graph():

    def __init__(self, input_=None, output=None):
        self.input = input_
        self.output = output

        self.entryNode = Node()
        self.exitNode = Node()

        self.copy = True


    def run(self):
        if self.input is None or self.output is None:
            raise TypeError

        if not Path(self.input).exists():
            print(Path(self.input))
            raise FileNotFoundError

        if self.copy:
            for f in Path(self.input).iterdir():
                print('Hi')
                sh.copyfile(f, Path(self.output) / f.name)

