from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
from abarorm import SQLiteModel
from abarorm.fields import sqlite







if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, host="localhost", port=8513)