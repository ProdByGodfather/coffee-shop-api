import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

load_dotenv()

# Initialize FastAPI app
db_conf = {
    'db_name': "coffee.db"
}

# Application 
app = FastAPI(title="Coffee Shop")


# Mount uploads file for coffee images
UPLOAD_DIR = os.getenv("UPLOAD_DIR")
print("IDJLKKDSFJ", UPLOAD_DIR)
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")