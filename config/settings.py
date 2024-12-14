import os
import dotenv

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


# Initialize FastAPI app
db_conf = {
    'db_name': "coffee.db"
}

# Application 
app = FastAPI(title="Coffee Shop")


# Mount uploads file for coffee images
UPLOAD_DIR = os.getenv("UPLOAD_DIR")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")