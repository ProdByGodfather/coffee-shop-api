from typing import List, Optional
from pydantic import BaseModel

# Pydantic models for validation
class CoffeeBase(BaseModel):
    coffeeName: str
    coffeeType: str
    rate: float
    commentCount: int
    price: float
    isLiked: bool
    desc: Optional[str]
    buyCount: int
    coffeeShopLocation: str
    coffeeAddress: str

class CoffeeCreate(CoffeeBase):
    pass

class CoffeeUpdate(BaseModel):
    coffeeName: Optional[str]
    coffeeType: Optional[str]
    rate: Optional[float]
    commentCount: Optional[int]
    price: Optional[float]
    isLiked: Optional[bool]
    desc: Optional[str]
    buyCount: Optional[int]
    coffeeShopLocation: Optional[str]
    coffeeAddress: Optional[str]

class CoffeeResponse(CoffeeBase):
    id: int
    image: str

    class Config:
        orm_mode = True