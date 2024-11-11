from PIL import Image
from refiners.solutions import BoxSegmenter
from typing import Tuple, Optional

class ImageSegmenter:
    def __init__(self):
        # Downloads the weights from finegrain/finegrain-box-segmenter
        self.segmenter = BoxSegmenter()
    
    # box_prompt is (x_min, y_min, x_max, y_max)
    def process_image(self, 
                     image: Image.Image, 
                     box_prompt: Optional[Tuple[int, int, int, int]] = None) -> Image.Image:

        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
            
        mask = self.segmenter(image, box_prompt=box_prompt) if box_prompt else self.segmenter(image)
        mask = mask.convert("L")
        transparent_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
        result_image = Image.composite(image, transparent_image, mask)
        
        return result_image



#input_image = Image.open("bg_remove_image.jpg") 
#segmenter = BoxSegmenter()
#mask = segmenter(input_image, box_prompt=(337, 279, 973, 1024))
# Or without box_prompt as a background remover
# mask = segmenter(input_image.convert("RGB"))
#mask = mask.convert("L")
#transparent_image = Image.new("RGBA", input_image.size, (0, 0, 0, 0))
#result_image = Image.composite(input_image, transparent_image, mask)
#result_image.save("output.png")

