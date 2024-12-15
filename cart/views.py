from fastapi import APIRouter, Depends


from cart.models import Cart
from cart.schemas import CartUpdateModel, CartModel
from token_config.creator import retrive_user


router = APIRouter()


@router.post("/")
def create_cart(user = Depends(retrive_user), data : CartModel = CartModel):
    pass