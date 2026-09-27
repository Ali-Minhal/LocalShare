from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
import threading
import os
from pathlib import Path

app = FastAPI()
@app.get("/")

def home():
    return "Hello LocalShare"

file_lock = threading.Lock()

@app.post("/files")
def upload(file: UploadFile):
    file_name = file.filename
    
    downloads_folder = (Path.home() / "Downloads").resolve()
    destination_path = downloads_folder / file_name

    
    
    with file_lock:
        if os.path.exists(destination_path):
            number = 1
            name, extension = os.path.splitext(file_name)
            candidate_filename = f"{name} ({number}){extension}" 
            candidate_path =  downloads_folder / candidate_filename

            while os.path.exists(candidate_path):
                number += 1
                candidate_filename = f"{name} ({number}){extension}"
                candidate_path = downloads_folder / candidate_filename
            file_name = candidate_filename

            destination_path = candidate_path
        destination_path = destination_path.resolve()
        if not destination_path.is_relative_to(downloads_folder):
            raise HTTPException(status_code=403, detail="Access to the requested file is forbidden.")
            
        destination_file =  open(destination_path, "xb")  # Open the file in binary write mode

    transfer_successful = False
    #From here we make use of file handling methods to save the file to disk or process it as needed.
    try:
        #FastAPI has already parsed the multipart upload and exposed the uploaded file as a file-like object, so we can read until there are no more bytes.
        while True:
            chunk = file.file.read(2048)  # Read in chunks of 2048 bytes
            if not chunk:
                break
            # An empty read means there are no more uploaded bytes to copy.
            
            destination_file.write(chunk)
        transfer_successful = True
    except Exception:
        pass
    finally:    
        destination_file.close()

    if not transfer_successful:
        if os.path.exists(destination_path):
            os.remove(destination_path)
        raise HTTPException(status_code=500, detail="An error occurred while processing the file.")

    
    return {
            "message": "Success",
            "filename": file_name
        }


@app.get("/files")

def list_files():
    downloads_folder = (Path.home() / "Downloads").resolve()
    file_data = []

    for item in downloads_folder.iterdir():
        if item.is_file():
            file_data.append ({
                "filename": item.name,
                "filetype": item.suffix,
                "filesize": item.stat().st_size
            })
    return {
        "message": "Success",
        "files": file_data
    }

@app.get("/files/{file_name}")
def download(file_name: str):
    downloads_folder = (Path.home() / "Downloads").resolve()
    candidate_path = downloads_folder / file_name

    resolved_path = candidate_path.resolve()

    if not resolved_path.is_relative_to(downloads_folder):
        raise HTTPException(status_code=403, detail="Access to the requested file is forbidden.")
    
    if not resolved_path.is_file(): #Removed the os.path.exists check because this checks if the path exists and is a file both simultaneously.
        raise HTTPException(status_code=404, detail="File not found.")

    return FileResponse(resolved_path, filename=file_name)