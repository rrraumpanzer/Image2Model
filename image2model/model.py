"""
from PIL import Image
from refiners.solutions import BoxSegmenter

input_image = Image.open("input.png") 

# Downloads the weights from finegrain/finegrain-box-segmenter
segmenter = BoxSegmenter()
# box_prompt is (x_min, y_min, x_max, y_max)
mask = segmenter(input_image, box_prompt=(24, 133, 588, 531))
# Or without box_prompt as a background remover
# mask = segmenter(input_image.convert("RGB"))
mask.save("output.png")



Заменил брию, лицензия не позволяет её коммерческое использование

РАЗОБРАТЬСЯ С ПОДКЛЮЧЕНИЕМ REFINERS
https://github.com/finegrain-ai/refiners/
https://rye.astral.sh/
"""
