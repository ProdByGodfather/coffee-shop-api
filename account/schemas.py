from pydantic import BaseModel


class DefaultBaseUserModel(BaseModel):
    username     : str
    password     : str
    first_name   : str
    last_name    : str

class UserModel(BaseModel):
    username     : str
    password     : str
    first_name   : str
    last_name    : str
    is_superuser : bool = False
    
    
class UserModelUpdate(BaseModel):
    username     : str  = None
    password     : str  = None
    first_name   : str  = None
    last_name    : str  = None
    is_superuser : bool = None