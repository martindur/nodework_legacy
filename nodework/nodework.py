import shutil as sh
import os
from pathlib import Path

class Content:

    def __init__(self, active_dir=None):
        if active_dir is not None:
            self._active_dir = Path(active_dir)
        else:
            self._active_dir = None
        self.file_types = []

    def __iter__(self):
        if self.active_dir.exists():
            if len(self.file_types) > 0:
                files = []
                for ext in self.file_types:
                    files.extend(self.active_dir.glob(f'*.{ext}'))
                return iter(files)
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
                if len(self.content.file_types) == 0:
                    for f in self.content.active_dir.iterdir():
                        sh.copyfile(f, Path(self.output) / f.name)
                else:
                    for ext in self.content.file_types:
                        for f in self.content.active_dir.glob(f'*.{ext}'):
                            sh.copyfile(f, Path(self.output) / f.name)

