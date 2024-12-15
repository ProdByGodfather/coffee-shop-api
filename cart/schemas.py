from pydantic import BaseModel


class CartModel(BaseModel):
    coffee : int
    count  : int = 1
    
class CartUpdateModel(BaseModel):
    coffee : int = None
    count  : int = None