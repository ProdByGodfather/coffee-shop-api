from pydantic import BaseModel

class UserModel(BaseModel):
    username     : str
    password     : str
    first_name   : str
    last_name    : str
    is_superuser : bool = False
    
    
class UserModelUpfsyr(BaseModel):
    username     : str  = None
    password     : str  = None
    first_name   : str  = None
    last_name    : str  = None
    is_superuser : bool = None