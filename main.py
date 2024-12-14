import os
from dotenv import load_dotenv

from config.urls import app

load_dotenv()





if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, host=os.getenv('HOST'), port=int(os.getenv('PORT')))