import os
import sys
import shutil
from pathlib import Path
import unittest


TEST_INPUTS = Path(__file__).parent / 'test_inputs'
TEST_OUTPUTS = Path(__file__).parent / 'test_outputs'


class TestGraphsAndNodes(unittest.TestCase):

    def setUp(self):
        module_path = Path(__file__).parent.parent
        sys.path.append(str(module_path.absolute()))
        TEST_INPUTS.mkdir(parents=True)
        TEST_OUTPUTS.mkdir(parents=True)
        with open(f'{TEST_INPUTS}/file', 'w') as f:
            print("File created.")

    def tearDown(self):
        module_path = Path(__file__).parent.parent
        sys.path.remove(str(module_path.absolute()))
        shutil.rmtree(TEST_INPUTS)
        shutil.rmtree(TEST_OUTPUTS)



    def add_test_images(self):
        from PIL import Image

        for i in range(5):
            r = 64 * (i+1)
            im = Image.new('RGBA', (r, r), color=(140, 140, 120, 255))
            im.save(f'{TEST_INPUTS}/{i+1}.png', "PNG")


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
        graph = Graph(input=TEST_INPUTS)


        # She wants to make a simple node that copies
        # a file from one folder to another. However
        # this can simply be done through the graph.
        graph.copy = True
        self.assertTrue(graph.copy)


        # So she sets an output and tries again
        graph.output = TEST_OUTPUTS


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

        from nodework import Graph

        # She initialises a Graph with input/output
        graph = Graph(input=TEST_INPUTS, output=TEST_OUTPUTS)

        # She creates a node that adds a 'hello' suffix to the
        # name of all input files.
        @graph.node
        def suffix(content):
            for f in content:
                if f.is_file():
                    f.rename(f.parent / f'{f.stem}_hello')

        # She connects the node
        graph.connect(suffix)

        # And runs the graph
        graph.run()

        self.assertTrue(os.path.exists(f'{TEST_OUTPUTS}/file_hello'))


    def test_create_node_that_adds_suffix_to_image_files(self):
        # Gwen thinks she's ready for an adventure.
        # More specifically, a suffixicated adventure!
        # She begins with importing dependencies
        from nodework import Graph

        # She initialises a Graph with input/output
        graph = Graph(input=TEST_INPUTS, output=TEST_OUTPUTS)

        # She has an idea, that she will create a node which
        # handles 'png' image files, and adds a suffix to the
        # filename, which describes the resolution of the image.

        # She will need an image manipulation library, and decides
        # to use pillow's Image module.
        from PIL import Image

        # She adds some images to use for testing
        # 5 images of variating size
        self.add_test_images()

        # Now she gets cracking on writing the node function
        @graph.node
        def resolution_suffix(content):
            for f in content:
                if f.suffix == '.png':
                    im = Image.open(f)
                    width, height = im.size
                    f.rename(f.parent / f'{f.stem}_{width}x{height}{f.suffix}')

        # Connects the node, and runs
        graph.connect(resolution_suffix)
        graph.run()


        self.assertTrue(os.path.exists(f'{TEST_OUTPUTS}/1_64x64.png'))
        self.assertTrue(os.path.exists(f'{TEST_OUTPUTS}/2_128x128.png'))
        self.assertTrue(os.path.exists(f'{TEST_OUTPUTS}/3_192x192.png'))
        self.assertTrue(os.path.exists(f'{TEST_OUTPUTS}/4_256x256.png'))
        self.assertTrue(os.path.exists(f'{TEST_OUTPUTS}/5_320x320.png'))






    def test_create_node_that_handles_image_scaling_and_run_it(self):
        from nodework import Graph
        # She figures out that she also needs the
        # ImageHandler to simplify operations with
        # images.
        from nodework.handlers import ImageHandler


        # She initialises a Graph
        graph = Graph(input=TEST_INPUTS, output=TEST_OUTPUTS)
        self.add_test_images()

        # Now she decides to make a node that takes 
        # an image of a certain size,
        # and outputs 3 variants at different sizes,
        # with different names. 
        @graph.node
        def create_img_variants(content):
            new_dir = content.mkdir('scaled_images')
            for img in content.types('png'):
                square = ImageHandler.open(img)
                thumbnail = ImageHandler.open(img)
                icon = ImageHandler.open(img)

                square.scale((512, 512))
                thumbnail.scale((256, 128))
                icon.scale((64, 64))

                square.save(new_dir / f'{img.stem}_square{img.suffix}')
                thumbnail.save(new_dir / f'{img.stem}_thumbnail{img.suffix}')
                icon.save(new_dir / f'{img.stem}_icon{img.suffix}')

            content.active_dir = new_dir


        # She connects and runs it
        graph.connect(create_img_variants)
        graph.run()


        # Expecting to see a total of 15 images in the output
        images_dir = Path().glob(f'{TEST_OUTPUTS}/*.png')
        images = [im for im in images_dir]
        for im in images:
            print(im)
        self.assertEqual(15, len(images))


if __name__ == '__main__':
    unittest.main()
