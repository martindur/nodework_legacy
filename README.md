# nodework

Proof of concept for working with common pipeline/file operations.

## example

```python
from nodework import Graph
from nodework.handlers import ImageHandler

graph = Graph(input='your/input/dir', output='your/optional/output/dir')


@graph.node
def copy_images(content):
    im_dir = content.mkdir('images')
    for im in content.types('png'):
        content.copy(im, img_dir)
    
    content.active_dir = im_dir
    

@graph.node
def rename_images(content):
    for im in content:
        image = ImageHandler.open(im)
        f.replace(im.with_name(f'{im.stem}_{image.size[0]}x{image.size[1]}{im.suffix}')
        
graph.connect(copy_images, rename_images)

if __name__ == '__main__':
    graph.run()
```

In this example I created a graph with a node that iterates over '.png' files from the Graph input folder and copies those files to a newly created 'images' folder. The next node then gets the resolution from each image with the ImageHandler, and adds the resolution to the file name. Lastly they are connected in the graph, and run.

## In-depth description

using the node decorator gives a function access to the content object. That object is essentially what gets passed around in a graph, between nodes. The content is essentially a pathlib Path object wrapped with some extended functionalities. One of the key uses is to change the active_dir. Any node that is currently running, will process the active_dir. In the example above, the rename_images node is processing the newly made 'images' dir, which is a subdirectory to the previous active_dir. When you create a new directory, it is by default relative to the current active_dir. This increases modularity, and you could fit multiple graphs together, or move a network of graphs to a whole other system.
