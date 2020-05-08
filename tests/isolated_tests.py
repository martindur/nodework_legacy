import unittest
import sys
from pathlib import Path



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
        from nodework import Content
        graph = self.get_graph_object()

        @graph.node
        def test_node(content):
            self.assertIsInstance(content, Content)

        test_node(graph)


    def test_content_has_copy_attribute(self):
        graph = self.get_graph_object()

        @graph.node
        def test_node(content):
            self.assertTrue(hasattr(content, 'copy'))

        test_node(graph)


    def test_content_copy_is_bool_type(self):
        graph = self.get_graph_object()

        @graph.node
        def test_node(content):
            self.assertIsInstance(content.copy, bool)

        test_node(graph)


    def test_content_returns_Content_object(self):
        from nodework import Content
        graph = self.get_graph_object()

        @graph.node
        def test_node(content):
            return content

        self.assertIsInstance(get_content, Content)


    @unittest.skip
    def test_content_nodein_is_Nodein_class(self):
        from nodework import Nodein
        graph = self.get_graph_object()

        @graph.node
        def test_node(content):
            self.assertTrue(isinstance(content.nodein, Nodein))

        test_node(graph)


    @unittest.skip
    def test_content_nodeout_can_add(self):
        graph = self.get_graph_object()

        some_path = 'test_inputs/my_file'

        @graph.node
        def test_node(content):
            content.nodeout.add(some_path)
            self.assertEqual(Path('test_inputs/my_file'), content.nodeout[0])

        test_node(graph)


    @unittest.skip
    def test_content_nodeout_does_not_take_a_string(self):
        graph = self.get_graph_object()

        @graph.node
        def test_node(content):
            with self.assertRaises(TypeError):
                content.nodeout.add('Here is a string!')

        test_node(graph)

if __name__ == '__main__':
    unittest.main()
