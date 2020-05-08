
class Content:

    def __init__(self):
        self.copy = True



class Graph():

    def __init__(self, input_=None, output=None):
        self.input = input_
        self.output = output


    def node(self, func):
        def decorator(self):
            content = Content()
            return func(content)
        return decorator

    def run(self):
        if self.input is None or self.output is None:
            raise RuntimeError


