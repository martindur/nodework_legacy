import unittest
import shutil
import sys
import os
from pathlib import Path


TEST_INPUTS = Path(__file__).parent / 'test_inputs'
TEST_OUTPUTS = Path(__file__).parent / 'test_outputs'


class TestNodeCreation(unittest.TestCase):


    def setUp(self):
        module_path = Path(__file__).parent.parent
        sys.path.append(str(module_path.absolute()))
        TEST_INPUTS.mkdir()
        TEST_OUTPUTS.mkdir()


    def tearDown(self):
        module_path = Path(__file__).parent.parent
        sys.path.remove(str(module_path.absolute()))
        shutil.rmtree(TEST_INPUTS)
        shutil.rmtree(TEST_OUTPUTS)



    def create_file(self, path):
        with open(path, 'w') as f:
            pass


    def get_graph_object(self):
        from nodework import Graph
        return Graph(input=TEST_INPUTS, output=TEST_OUTPUTS)


    def test_content_is_Content_class_with_node_decorator(self):
        from nodework import Content, Graph
        graph = self.get_graph_object()

        @graph.node
        def test_node(content):
            self.assertIsInstance(content, Content)

        test_node(graph)


    def test_node_returns_Content_object(self):
        from nodework import Content, Graph
        graph = self.get_graph_object()

        @graph.node
        def test_node(content):
            return content

        get_content = test_node(graph)

        self.assertIsInstance(get_content, Content)


    def test_input_path_exists_when_graph_run(self):
        from nodework import Graph
        graph = Graph(input='testsss_inputz')
        graph.output = TEST_OUTPUTS

        with self.assertRaises(FileExistsError):
            graph.run()


    def test_output_node_copies_file_from_input_path(self):
        from nodework import Graph
        graph = Graph(input=TEST_INPUTS)
        graph.output = TEST_OUTPUTS


        self.create_file(f'{TEST_INPUTS}/file')

        graph.run()
        self.assertTrue(os.path.exists(f'{TEST_OUTPUTS}/file'))


    def test_can_connect_node_to_input_and_output(self):
        from nodework import Graph
        graph = self.get_graph_object()

        @graph.node
        def some_node(content):
            return content

        graph.connect(some_node)
        graph.run()
        self.assertEqual(some_node, graph.head.work)


    def test_content_is_iterable(self):
        from nodework import Content

        self.create_file(TEST_INPUTS / 'file')

        content = Content()
        content.active_dir = TEST_INPUTS
        self.assertEqual(content.active_dir, TEST_INPUTS)

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


    def test_content_class_can_copy_file(self):
        from nodework import Content

        self.create_file(TEST_INPUTS / 'file.txt')
        new_dir = TEST_INPUTS / 'copy_here'
        new_dir.mkdir()

        content = Content()
        content.active_dir = TEST_INPUTS
        content.copy(TEST_INPUTS / 'file.txt', new_dir)

        self.assertTrue(os.path.exists(TEST_INPUTS / 'copy_here' / 'file.txt'))


    def test_node_connection_receives_correct_content(self):
        from nodework import Graph
        graph = self.get_graph_object()

        self.create_file(TEST_INPUTS / 'file.txt')

        @graph.node
        def node_a(content):
            for f in content:
                f.rename(f.parent / f'{f.stem}.py')

        @graph.node
        def node_b(content):
            self.assertIn(TEST_INPUTS / 'file.py', content)


        graph.connect(node_a, node_b)
        self.assertEqual(node_a, graph.head.work)
        self.assertEqual(node_b, graph.head.next.work)
        graph.run()


    def test_content_only_iterates_certain_file_types(self):
        from nodework import Graph
        graph = self.get_graph_object()

        self.create_file(TEST_INPUTS / 'file.txt')
        self.create_file(TEST_INPUTS / 'image.png')

        @graph.node
        def rename_img(content):
            for img in content.types('png'):
                img.rename(img.parent / f'{img.stem}_newname{img.suffix}')

        graph.connect(rename_img)
        graph.run()

        self.assertTrue(os.path.exists(TEST_OUTPUTS / 'image_newname.png'))
        self.assertFalse(os.path.exists(TEST_OUTPUTS / 'file_newname.txt'))


    def test_imagehandler_can_open_image_and_returns_imagehandler_type(self):
        from nodework.handlers import ImageHandler
        from PIL import Image

        image = Image.new('RGB', (256, 256), color=(0,0,0))
        image.save(TEST_INPUTS / 'image.png')

        img = ImageHandler.open(TEST_INPUTS / 'image.png')

        self.assertIsInstance(img, ImageHandler)


    def test_imagehandler_can_scale_square_image(self):
        from nodework.handlers import ImageHandler
        from PIL import Image

        image = Image.new('RGB', (256, 256), color=(0,0,0))
        image.save(TEST_INPUTS / 'image.png')

        img = ImageHandler.open(TEST_INPUTS / 'image.png')

        img.scale((128, 128))


        self.assertEqual(img.pil_image.size, (128, 128))


    def test_imagehandler_can_scale_rect_image(self):
        from nodework.handlers import ImageHandler
        from PIL import Image

        image = Image.new('RGB', (800, 300), color=(0,0,0))
        image.save(TEST_INPUTS / 'image.png')

        img = ImageHandler.open(TEST_INPUTS / 'image.png')

        img.scale((256, 256))


        self.assertEqual(img.pil_image.size, (256, 256))


    def test_imagehandler_can_save_image(self):
        from nodework.handlers import ImageHandler
        from PIL import Image

        image = Image.new('RGB', (256, 256), color=(0,0,0))
        image.save(TEST_INPUTS / 'image.png')

        img = ImageHandler.open(TEST_INPUTS / 'image.png')

        img.save(TEST_OUTPUTS / 'new_image.png')

        self.assertTrue(os.path.exists(TEST_OUTPUTS / 'new_image.png'))



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
