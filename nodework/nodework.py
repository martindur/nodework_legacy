import shutil as sh
import os
from pathlib import Path

class Content:

    def __init__(self, active_dir=None):
        if active_dir is not None:
            self._active_dir = Path(active_dir)
        else:
            self._active_dir = None

    def __iter__(self):
        if self.active_dir.exists():
            return iter(self.active_dir.iterdir())
        else:
            raise FileExistsError

    def __contains__(self, file):
        return file in self.active_dir.iterdir()


    @property
    def active_dir(self):
        return Path(self._active_dir)


    @active_dir.setter
    def active_dir(self, new_dir):
        self._active_dir = Path(new_dir)


    @staticmethod
    def copy(*args, **kwargs):
        sh.copy(*args, **kwargs)


    def types(self, *suffixes):
        files = []
        for ext in suffixes:
            files.extend(self.active_dir.glob(f'*.{ext}'))
        return iter(files)


    def mkdir(self, dir_name):
        if Path(self.active_dir / dir_name).exists():
            return self.active_dir / dir_name
        relative_dir = self.active_dir / dir_name
        relative_dir.mkdir(parents=True)
        return relative_dir



class Node:

    def __init__(self, work=None):
        self.work = work
        self.next = None


class Graph:

    def __init__(self, input, output=None):
        self._input = Path(input)
        if output is not None:
            self._output = Path(output)
        self.content = Content(active_dir=self.input)
        self.head = None


    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, new_input):
        self._input = Path(new_input)

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, new_output):
        self._output = Path(new_output)


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
        if not self.input.exists():
            raise FileExistsError

        active_node = self.head
        while active_node is not None:
            active_node.work()
            active_node = active_node.next

        if self.output is not None:
            if not self.output.exists():
                raise FileExistsError
            for f in self.content.active_dir.iterdir():
                if f.is_dir():
                    sh.copytree(f, self.output / f.name)
                else:
                    sh.copy(f, self.output / f.name)
