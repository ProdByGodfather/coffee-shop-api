import os
from dotenv import load_dotenv
from fastapi import FastAPI
from contextlib import asynccontextmanager
from extensions.password_hasher import hash_password
from account.models import User

load_dotenv()

'''
    this life span meked for managing default datas in database.
    some actions in this lifespan: (more actions run for first time and other times dont use)
    - create default user
'''
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Of Application
    create_default_user()
    
    
    yield
    
    
    # End Of Application
    print("Application Shutting down")
    
    
    
# ----------------------------------------------------------------


'''
    the default user have all access and permissions so to setup the application you must using that.
    default user username and password:
    - username : hoopad
    - password : KBNA!@#P!@84
'''
def create_default_user():
    default_user = User.get(username = 'hoopad')
    if not default_user:
        print("Auto configure Default User")
        User.create(username = os.getenv("USERNAME"),
                    password = hash_password(os.getenv("PASSWORD")),
                    first_name = "Admin",
                    last_name = "admin",
                    is_superuser = True)
    return