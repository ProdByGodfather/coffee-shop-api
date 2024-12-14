import os
from dotenv import load_dotenv

load_dotenv()

# Initialize FastAPI app
db_conf = {
    'db_name': os.getenv('DB_NAME')
}
