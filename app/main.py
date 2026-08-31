from fastapi import FastAPI, File, UploadFile
from database import init_db, reset_db, save_file




app = FastAPI()



@app.on_event("startup")
def startup():
    reset_db()

@app.get("/")
def check():
   return{"status": "Server is working"}



@app.post("/uploadfiles_test")
async def upload_files(file: UploadFile = File(...)):

  file_content = await file.read()

  file_id = save_file(
      filename=file.filename,
      content_type=file.content_type,
      file_data=file_content
  )

  return {
        "status": "success",
        "file_id": file_id,
        "filename": file.filename,
        "size_bytes": len(file_content)
    }

  
