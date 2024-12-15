from pydantic import BaseModel


class CartModel(BaseModel):
    coffee : int
    count  : int = 1
    
class CartUpdateModel(BaseModel):
    count  : int = None