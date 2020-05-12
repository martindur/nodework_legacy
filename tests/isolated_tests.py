import unittest
import sys
import os
from pathlib import Path


TEST_INPUTS = Path(__file__).parent / 'test_inputs'
TEST_OUTPUTS = Path(__file__).parent / 'test_outputs'


class TestNodeCreation(unittest.TestCase):


    def setUp(self):
        module_path = Path(__file__).parent.parent
        sys.path.append(str(module_path.absolute()))


    def tearDown(self):
        module_path = Path(__file__).parent.parent
        sys.path.remove(str(module_path.absolute()))

        for f in Path(TEST_INPUTS).iterdir():
            print(f'Removing "{f}"')
            os.remove(f)

        for f in Path(TEST_OUTPUTS).iterdir():
            print(f'Removing "{f}"')
            os.remove(f)


    def create_file(self, path):
        with open(path, 'w') as f:
            print(f'file "{path}" created.')


    def get_graph_object(self):
        from nodework import Graph
        return Graph(input=TEST_INPUTS, output=TEST_OUTPUTS)


    def test_content_is_Content_class_with_node_decorator(self):
        from nodework import Content, node

        @node
        def test_node(content):
            self.assertIsInstance(content, Content)

        test_node()


    def test_node_returns_Content_object(self):
        from nodework import Content, node

        @node
        def test_node(content):
            return content

        get_content = test_node()

        self.assertIsInstance(get_content, Content)


    def test_input_path_is_not_none_when_graph_run(self):
        from nodework import Graph
        graph = Graph()
        graph.output = TEST_OUTPUTS

        with self.assertRaises(TypeError):
            graph.run()


    def test_output_path_is_not_none_when_graph_run(self):
        from nodework import Graph
        graph = Graph()
        graph.input = TEST_INPUTS

        with self.assertRaises(TypeError):
            graph.run()


    def test_input_path_exists_when_graph_run(self):
        from nodework import Graph
        graph = Graph()
        graph.output = TEST_OUTPUTS
        graph.input = 'testsss_inputz'

        with self.assertRaises(FileNotFoundError):
            graph.run()


    def test_output_node_copies_file_from_input_path(self):
        from nodework import Graph
        graph = Graph()
        graph.input = TEST_INPUTS
        graph.output = TEST_OUTPUTS


        self.create_file(f'{TEST_INPUTS}/file')

        graph.run()
        self.assertTrue(os.path.exists(f'{TEST_OUTPUTS}/file'))


    def test_entry_node_is_first_element_in_nodes(self):
        from nodework import Graph
        graph = self.get_graph_object()

        self.assertEqual(graph.entryNode, graph.nodes[0])


    def test_exit_node_is_last_element_in_nodes(self):
        from nodework import Graph
        graph = self.get_graph_object()

        self.assertEqual(graph.exitNode, graph.nodes[-1])


    def test_can_connect_node_to_input_and_output(self):
        from nodework import Graph, node
        graph = self.get_graph_object()

        @node
        def some_node(content):
            return content

        graph.connect(some_node)
        graph.run()
        self.assertEqual(some_node, graph.nodes[1].work)


    def test_content_is_iterable(self):
        from nodework import Content

        self.create_file(TEST_INPUTS / 'file')

        content = Content()
        content.active_dir = TEST_INPUTS
        self.assertEqual(content.active_dir, TEST_INPUTS)
        print("Content is iterable")

        for f in content:
            self.assertEqual(f.name, 'file')


    def test_content_files_have_stem(self):
        from nodework import Content

        self.create_file(TEST_INPUTS / 'file.txt')

        content = Content()
        content.active_dir = TEST_INPUTS

        for f in content:
            self.assertEqual(f.stem, 'file')


    def test_content_files_can_rename(self):
        from nodework import Content

        self.create_file(TEST_INPUTS / 'file.txt')

        content = Content()
        content.active_dir = TEST_INPUTS

        for f in content:
            f.rename(f.parent / f'{f.stem}_hello{f.suffix}')

        for f in content:
            self.assertEqual(f.name, 'file_hello.txt')


    # This will probably be useful
    @unittest.skip
    def test_output_path_created_if_not_existing(self):
        pass


    # Need to find a good way of writing this test isolated.
    @unittest.skip
    def test_run_can_copy_file_from_input_to_output(self):
        graph = self.get_graph_object()

        @graph.node
        def test_node(content):
            content.copy = True
            return content



if __name__ == '__main__':
    unittest.main()
