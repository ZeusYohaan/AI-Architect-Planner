from fastapi import FastAPI,UploadFile,Depends,File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse,FileResponse
from pydantic import BaseModel
from shutil import copyfileobj,rmtree
from background_tasks import cleanup
from werkzeug.utils import secure_filename
from pathlib import Path
from PIL import Image
from starlette.background import BackgroundTask

from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
    user_id: str

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# updload files
@app.post("/export2glb")
async def export2glb(item:Item = Depends(),up_file:UploadFile = File(...)):
    args = jsonable_encoder(item)
    # copy uploaded file object to local
    filename = secure_filename(up_file.filename)
    with open(filename, "wb") as uploaded_file:
        copyfileobj(up_file.file,uploaded_file)
    
    #check file extenision: 
    if Path(filename).suffix in [".jpg",".jpeg",".png",".pdf"]:
        # check if it's a valid img:
        print(f"file is a image format:{Path(filename).suffix}")
        try:
            img = Image.open(filename)
        except Exception as e:
            # what to retun in case of failure to read img 
            pass
            # what to do to check if pdf is valid or not
        
        # do the conversion for image files
    
    elif Path(filename).suffix == ".dxf":
        print(f"file is a dxf format:{Path(filename).suffix}")
        # call the dxf to glb conversion function
        pass
        
    elif Path(filename).suffix == ".xls":
        print(f"file is a xls format:{Path(filename).suffix}")
        # call the xls to glb conversion function
        pass
        
    return FileResponse(filename,background=BackgroundTask(cleanup,[filename]))