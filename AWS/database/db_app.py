from fastapi import FastAPI,UploadFile,Depends,File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from shutil import copyfileobj,rmtree
from werkzeug.utils import secure_filename
from pathlib import Path
from PIL import Image
from obj_handler import get_collection

from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
    user_id: str
    input_file : str
    output_file : str
    status: str
    error : str

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/postReqData")
async def postReqData(item:Item = Depends()):
    args = jsonable_encoder(item)
    col = get_collection()
    data_dic = {"$set":{"input_file": args["input_file"],"output_file":args["output_file"],"status": args["status"],"error" : args["error"]}}
    try:
        col.update_one({"user_id":args["user_id"]},data_dic,upsert=True)
        response = {"user_id":args["user_id"],
                    "status":"success",
                    "error":None}
    except Exception as e:
        response = {"user_id":args["user_id"],
                    "status":"failure",
                    "error":e}
    finally:
        return JSONResponse(content=response)