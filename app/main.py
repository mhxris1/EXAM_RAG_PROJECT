from typing import List
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()

@app.get("/")
def check():
  return {"Server is working"}

@app.post("/uploadfiles_test")
async def upload_files(file: UploadFile = File(...)):
  return {"filenames": file.filename}
