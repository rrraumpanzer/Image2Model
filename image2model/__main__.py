from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
from image2model.model import ImageSegmenter
app = FastAPI()



class Coordinates(BaseModel):
    ul_x: int #Координаты левой верхней точки bounding box объекта
    ul_y: int
    lr_x: int #Координаты правой нижней точки bounding box объекта
    lr_y: int

class Storage: #Хранение координат и изображения 
    def __init__(self):
        self.coordinates = [0, 0, 1024, 1024]
        self.image = None
        self.processed_image = None

    def set_coords(self, coords: Coordinates):
        self.coordinates = [coords.ul_x, coords.ul_y, coords.lr_x, coords.lr_y]
    def get_coords(self):
        return self.coordinates
    
    def set_image(self, image: Image):
        self.image = image
    def get_image(self):
        return self.image
    
    def set_processed_image(self, image: Image):
        self.processed_image = image
        
    def get_processed_image(self):
        return self.processed_image

img_coord_storage = Storage()
segmenter = ImageSegmenter()

@app.post('/image')
async def post_image(image: UploadFile = File(...)):
    try:        
        image_bytes = await image.read()
        im = Image.open(BytesIO(image_bytes))
        if im.mode in ("RGBA", "P"): 
            im = im.convert("RGB")
        
        #im.save('image.jpg', 'JPEG') если надо сохранить на диск
        img_coord_storage.set_image(im)

        return 'Successfully read an image'
    except Exception as err:
        return f'Error: {err}'

@app.get('/image')
async def read_image():
    try:
        image = img_coord_storage.get_image()
        if image is None:
            return JSONResponse(status_code=404)
        
        #Нельзя отправлять PIL напрямую, только через BytesIO и StreamingResponse, не знаю почему
        img_bytes = BytesIO()
        image.save(img_bytes, format="JPEG")
        img_bytes.seek(0)

        return Response(content=img_bytes.read(), media_type="image/jpeg")
    except Exception as err:
        return f'Error: {err}'

@app.post('/coords')
async def read_coords(coords: Coordinates):
    img_coord_storage.set_coords(coords)
    return {"coordinates": img_coord_storage.get_coords()}

@app.get('/coords')
async def get_coords():
    return {"coordinates": img_coord_storage.get_coords()}

@app.get('/test')
def greet():
 return "Hello World!"

@app.post('/process')
async def process_image():
    try:
        image = img_coord_storage.get_image()
        coords = img_coord_storage.get_coords()
        
        if image is None:
            return JSONResponse(status_code=400, content={"message": "No image uploaded"})
            
        processed_image = segmenter.process_image(image=image, box_prompt=tuple(coords))
        
        img_coord_storage.set_processed_image(processed_image)
        
        return {"message": "Image processed successfully"}
        
    except Exception as err:
        return JSONResponse(status_code=500, content={"message": f"Processing error: {str(err)}"})

@app.get('/processed-image')
async def get_processed_image():
    try:
        image = img_coord_storage.get_processed_image()
        if image is None:
            return JSONResponse(status_code=404, content={"message": "No processed image available"})
        
        #Всё ещё помню что нельзя передавать просто PIL
        img_bytes = BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        
        return Response(content=img_bytes.read(), media_type="image/png")
    except Exception as err:
        return JSONResponse(status_code=500, content={"message": f"Error: {str(err)}"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", reload=True)