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
        from nodework import Content, node

        @node
        def test_node(content):
            self.assertIsInstance(content, Content)

        test_node()


    def test_content_has_copy_attribute(self):
        from nodework import node

        @node
        def test_node(content):
            self.assertTrue(hasattr(content, 'copy'))

        test_node()


    def test_content_copy_is_bool_type(self):
        from nodework import node

        @node
        def test_node(content):
            self.assertIsInstance(content.copy, bool)

        test_node()


    def test_content_returns_Content_object(self):
        from nodework import Content, node

        @node
        def test_node(content):
            return content

        get_content = test_node()

        self.assertIsInstance(get_content, Content)


    def test_input_path_is_not_none_when_graph_run(self):
        from nodework import Graph
        graph = Graph()
        graph.output = 'test_outputs'

        with self.assertRaises(TypeError):
            graph.run()


    def test_output_path_is_not_none_when_graph_run(self):
        from nodework import Graph
        graph = Graph()
        graph.input = 'test_inputs'

        with self.assertRaises(TypeError):
            graph.run()


    def test_input_path_exists_when_graph_run(self):
        from nodework import Graph
        graph = Graph()
        graph.output = 'test_outputs'
        graph.input = 'testsss_inputz'

        with self.assertRaises(FileNotFoundError):
            graph.run()



    def test_graph_can_connect_input_and_output_to_node(self):
        from nodework import Graph, node
        graph = self.get_graph_object()

        @node
        def test_node(content):
            return content

        graph.connect(test_node)

        self.assertEqual(test_node, graph.entryNode.nodes[0].node)
        self.assertEqual(test_node, graph.nodes[0].node)
        self.assertEqual(graph.exitNode, graph.nodes[0].nodes[0])


    def test_graph_can_connect_multiple_nodes(self):
        from nodework import Graph, node
        graph = self.get_graph_object()

        @node
        def node_one(content):
            return content

        @node
        def node_two(content):
            return content

        graph.connect(node_one, node_two)

        self.assertEqual(node_one, graph.entryNode.nodes[0].node)
        self.assertEqual(node_one, graph.nodes[0].node)
        self.assertEqual(node_two, graph.nodes[1].node)
        self.assertEqual(node_two, graph.nodes[0].nodes[0].node)
        self.assertEqual(graph.exitNode, graph.nodes[1].nodes[0])


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
