from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from database import reset_db, save_file
from pipeline import process_document_pipeline


app = FastAPI()

#run reset function when the server is started up
@app.on_event("startup")
def startup():
    reset_db()


@app.get("/")
def check():
   return{"status": "Server is working"}


#REST api to allow users to uplaod file
@app.post("/uploadfiles_test")
async def upload_files(
   background_tasks: BackgroundTasks,
   file: UploadFile = File(...)):

# This assigns file binary to variable
  file_content = await file.read()

# We run the save_file function passing in the said parameters and it evaluates the last row assigning it as the id
  file_id = save_file(
      filename=file.filename,
      content_type=file.content_type,
      file_data=file_content
  )

  background_tasks.add_task(
        process_document_pipeline,
        file_id=file_id,
        file_bytes=file_content,
        filename=file.filename
    )

#returns the following json to the server
  return {
        "status": "success",
        "file_id": file_id,
        "filename": file.filename,
        "size_bytes": len(file_content)
    }

  
