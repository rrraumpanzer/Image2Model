from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
app = FastAPI()

class Coordinates(BaseModel):
    x: int
    y: int

class Storage: #Хранение координат и изображения 
    def __init__(self):
        self.coordinates = [512, 512]
        self.image = None

    def set_coords(self, coords: Coordinates):
        self.coordinates = [coords.x, coords.y]
    def get_coords(self):
        return self.coordinates
    
    def set_image(self, image: Image):
        self.image = image
    def get_image(self):
        return self.image
    

img_coord_storage = Storage()

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
    img_coord_storage.update(coords)
    return {"coordinates": img_coord_storage.get()}

@app.get('/coords')
async def get_coords():
    return {"coordinates": img_coord_storage.get()}

@app.get('/test')
def greet():
 return "Hello World!"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("__main__:app", reload=True)