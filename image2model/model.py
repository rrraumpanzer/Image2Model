from PIL import Image
from refiners.solutions import BoxSegmenter

input_image = Image.open("bg_remove_image.jpg") 

# Downloads the weights from finegrain/finegrain-box-segmenter
segmenter = BoxSegmenter()
# box_prompt is (x_min, y_min, x_max, y_max)
mask = segmenter(input_image, box_prompt=(337, 279, 973, 1024))
# Or without box_prompt as a background remover
# mask = segmenter(input_image.convert("RGB"))
mask = mask.convert("L")
transparent_image = Image.new("RGBA", input_image.size, (0, 0, 0, 0))
result_image = Image.composite(input_image, transparent_image, mask)
result_image.save("output.png")

