from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
from pydantic import BaseModel
from PIL import Image
app = FastAPI()

class Coordinates(BaseModel):
    x: int
    y: int

class Storage: #Хранение координат и (добавить?) изображения 
    def __init__(self):
        self.coordinates = [512, 512]

    def update(self, coords: Coordinates):
        self.coordinates = [coords.x, coords.y]

    def get(self):
        return self.coordinates

img_coord_storage = Storage()

@app.post('/image')
def read_image(image: UploadFile = File(...)):
  try:        
      im = Image.open(image.file)
      if im.mode in ("RGBA", "P"): 
          im = im.convert("RGB")
      im.save('image.jpg', 'JPEG')
      return JSONResponse({'Successfully read an image'}, status_code=200)
  except Exception:
      return JSONResponse({'Something went wrong'}, status_code=500)
  finally:
      image.file.close()
      im.close()

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