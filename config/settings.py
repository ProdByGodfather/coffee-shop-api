import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config.events import lifespan

load_dotenv()


# Application 
app = FastAPI(title="Coffee Shop", lifespan=lifespan)


# Mount uploads file for coffee images
UPLOAD_DIR = os.getenv("UPLOAD_DIR")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")