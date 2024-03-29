from fastapi import FastAPI,UploadFile,Depends,File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from shutil import copyfileobj,rmtree
from werkzeug.utils import secure_filename
from pathlib import Path
from PIL import Image
from file_handler import save_file

from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
    user_id: str
    file_des: str #input_file or output_file

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadFile2s3 ")
async def upload_file(item:Item = Depends(),up_file:UploadFile = File(...)):
    args = jsonable_encoder(item)
    # copy uploaded file object to local
    filename = secure_filename(up_file.filename)
    with open(filename, "wb") as uploaded_file:
        copyfileobj(up_file.file,uploaded_file)
    file_path_s3,err = save_file(args,filepath=filename)
    if file_path_s3 is not None and err is None:
        response = {"file_path_s3" : file_path_s3,
                    "user_id" : args['user_id'],
                    "status" : "success",
                    "error" : err}
    elif file_path_s3 is None:
        response = {"file_path_s3" : file_path_s3,
                    "user_id" : args['user_id'],
                    "status" : "failure",
                    "error" : err}
        
    return JSONResponse(content=response)