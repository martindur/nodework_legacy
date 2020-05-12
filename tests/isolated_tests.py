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


    def get_graph_object(self):
        from nodework import Graph
        return Graph(input_='test_inputs', output='test_outputs')


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

        with open(f'{TEST_INPUTS}/file', 'w') as f:
            print("file created.")

        graph.run()
        self.assertTrue(os.path.exists(f'{TEST_OUTPUTS}/file'))

        if os.path.exists(f'{TEST_OUTPUTS}/file'):
            os.remove(f'{TEST_OUTPUTS}/file')

        os.remove(f'{TEST_INPUTS}/file')



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
