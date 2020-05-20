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
