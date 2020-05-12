import os
import sys
from pathlib import Path
import unittest


TEST_INPUTS = Path(__file__).parent / 'test_inputs'
TEST_OUTPUTS = Path(__file__).parent / 'test_outputs'


class TestGraphsAndNodes(unittest.TestCase):

    def setUp(self):
        module_path = Path(__file__).parent.parent
        sys.path.append(str(module_path.absolute()))
        with open(f'{TEST_INPUTS}/file', 'w') as f:
            print("File created.")

    def tearDown(self):
        module_path = Path(__file__).parent.parent
        sys.path.remove(str(module_path.absolute()))
        for f in TEST_INPUTS.rglob('*'):
            os.remove(f)
        for f in TEST_OUTPUTS.rglob('*'):
            os.remove(f)


    def add_test_images(self):
        from PIL import Image

        for i in range(5):
            r = 128 * i+1
            im = Image().new('RGBA', (r, r), color=(140, 140, 120, 255))
            im.save(f'{TEST_INPUTS}/{i}', "PNG")


    def remove_test_images(self):
        for im in Path().glob(f'{TEST_INPUTS}/*.png'):
            im.unlink()

        for im in Path().glob(f'{TEST_OUTPUTS}/*.png'):
            im.unlink()


    def test_create_node_that_can_copy_a_file(self):
        # Gwen heard about this really cool framework
        # that handles common pipeline and automation
        # tasks for game development

        # She decides to try it out. 
        from nodework import Graph

        # Then she initialises a Graph
        graph = Graph()


        # She wants to make a simple node that copies
        # a file from one folder to another. However
        # this can simply be done through the graph.
        graph.copy = True
        self.assertTrue(graph.copy)


        # Now she tries to run the graph, but it raises
        # an error because she hasn't set inputs/outputs
        with self.assertRaises(TypeError):
            graph.run()

        # So she sets an output and tries again
        graph.output = TEST_OUTPUTS

        # The error is persistent because she needs to set
        # an input as well
        with self.assertRaises(TypeError):
            graph.run()

        # So she sets an input and tries again, unfortunately
        # She has a typo in her path and it does not exist.
        graph.input = 'tests_inputz'
        with self.assertRaises(FileNotFoundError):
            graph.run()

        # She corrects her typo
        graph.input = TEST_INPUTS

        # Now it runs
        graph.run()


        # And it all seems to work!
        self.assertTrue(os.path.exists(f'{TEST_OUTPUTS}/file'))


    def test_create_node_that_adds_suffix_to_files(self):
        # Gwen has an idea for handling images, but
        # before that, she wants to try out how
        # manipulating files with nodes works first.

        from nodework import Graph, node

        # She initialises a Graph with input/output
        graph = Graph(input=TEST_INPUTS, output=TEST_OUTPUTS)

        # She creates a node that adds a 'hello' suffix to the
        # name of all input files.
        @node
        def suffix(content):
            for f in content:
                f.rename(f.parent / f'{f.stem}_hello')

            return content

        # She connects the node
        graph.connect(suffix)

        # And runs the graph
        graph.run()

        self.assertTrue(os.path.exists(f'{TEST_OUTPUTS}/file_hello'))


    @unittest.skip
    def test_create_node_that_adds_suffix_to_image_files(self):
        # Gwen thinks she's ready for an adventure.
        # More specifically, a suffixicated adventure!
        # She begins with importing dependencies
        from nodework import Graph

        # She initialises a Graph with input/output
        graph = Graph(input_=TEST_INPUTS, output=TEST_OUTPUTS)

        # She has an idea, that she will create a node which
        # handles 'png' image files, and adds a suffix to the
        # filename, which describes the resolution of the image.

        # She will need an image manipulation library, and decides
        # to use pillow's Image module.
        from PIL import Image

        # She adds some images to use for testing
        self.add_test_images()

        # Now she gets cracking on writing the node function
        @graph.node(input=['png'])
        def resolution_suffix(content):
            for f in content:
                width, height = Image(f).size
                new_stem = f'{f.stem}_{width}x{height}'
                f.stem = new_stem
                f.save()

            return content




    @unittest.skip
    def test_create_node_that_handles_image_scaling_and_run_it(self):
        # Gwen heard about this really cool framework
        # that handles common pipeline and automation
        # tasks for game development

        # She decides to try it out. 
        from nodework import Graph, Nodes
        # She figures out that she also needs some
        # helper methods
        from nodework.image import Image


        # She initialises a Graph with a common
        # name. She doesn't know which kind of graph 
        # she is building yet, so she'll let it be
        # a generic graph for now. Alternatively she
        # could use a name that encapsulates what
        # kind of nodes exist in the graph.
        graph = Graph()
        nodes = Nodes()


        # Now she decides to make an initial simple
        # node that takes an image of a certain size,
        # and outputs 3 variants at different sizes,
        # with different names. 
        @nodes.node(nodein=['png'], nodeout=['png'])
        def create_img_variants():
            for img in nodein.content:
                square, thumbnail, icon = Image(img)
                square.scale((512, 512), no_stretch=True)
                thumbnail.scale((1024, 800), no_stretch=True)
                icon.scale((64, 64), no_stretch=True)
                nodeout.add(square)
                nodeout.add(thumbnail)
                nodeout.add(icon)


        # After having created her node, she
        # wants to give it a spin through the
        # graph
        graph.input = f'{TEST_INPUTS}'
        graph.output = f'{TEST_OUTPUTS}'

        graph.run()

        images_dir = Path().glob(f'{TEST_OUTPUTS}/*.png')
        images = [im for im in images_dir]
        self.assertEqual(15, len(images))


if __name__ == '__main__':
    unittest.main()
