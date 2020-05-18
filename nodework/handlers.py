from PIL import Image
from pathlib import Path

class ImageHandler:

    def __init__(self, pil_image=None):
        self.pil_image = Image.open(pil_image)
        self.file = Path(pil_image)

    @classmethod
    def open(cls, image):
        return ImageHandler(image)


    def scale(self, size):
        w, h = size
        cur_w, cur_h = self.pil_image.size
        scalar = max(w/cur_w, h/cur_h)
        self.pil_image.thumbnail((cur_w*scalar, cur_h*scalar))
        cur_w, cur_h = self.pil_image.size
        box = ((cur_w/2) - (w/2), (cur_h/2) + (h/2),
               (cur_w/2) + (w/2), (cur_h/2) - (h/2))
        self.pil_image.crop(box)


    def save(self, *args, **kwargs):
        if len(args) == 0:
            print("No filepath given.")
            return

        path = Path(args[0])

        if path.is_dir():
            new_file = Path(path) / self.file.name
            new_args = (new_file, *args[1:])
            self.pil_image.save(*new_args, **kwargs)
        else:
            self.pil_image.save(*args, **kwargs)
