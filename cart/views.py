from fastapi import APIRouter, Depends, HTTPException


from cart.models import Cart, Coffee
from cart.schemas import CartUpdateModel, CartModel
from token_config.creator import retrive_user


router = APIRouter()


@router.post("/")
def create_cart(user = Depends(retrive_user), data : CartModel = CartModel):
    data = data.model_dump()
    coffee = Coffee.get(id = data['coffee'])
    
    if not coffee:
        return HTTPException(status_code=404, detail=f"Coffee with id {data['coffee']} not found")
    try:
        from_last = Cart.get(coffee = coffee.id, user = user['id'])
        if from_last:
            from_last.count = from_last.count + data['count']
            from_last.save()
            
        else:
            Cart.create(user = user['id'], coffee = coffee.id, count = data['count'])
    except Exception as e:
        return HTTPException(status_code=422, detail=f"Error: {e}")
    
    return HTTPException(status_code=201, detail="Cart Item Created")