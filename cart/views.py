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

@router.get("/")
def list_cart(user = Depends(retrive_user)):
    carts = Cart.filter(user = user['id'])
    cart_dict = carts.to_dict()
    price = 0
    for i in cart_dict:
        try:
            coffee = Coffee.get(id = i['coffee'])
            price += coffee.price
            
        except Exception as e:
            print(f"ERROR: {e}")
    context = {
        "data" : cart_dict,
        "price" : price
    }
    return HTTPException(status_code=200, detail=context)


@router.put("/{id}")
def update_cart_count(user = Depends(retrive_user), id = int, data : CartUpdateModel = CartUpdateModel):
    data = data.model_dump(exclude_unset=True)
    cart = Cart.get(id = id, user = user['id'])
    if not cart:
        return HTTPException(status_code=404, detail="This Cart Does not exists.")
    
    if 'count' in data:
        cart.count = data['count']
    cart.save()
    return HTTPException(status_code=200, detail="Data Successfully updated.")
    
@router.delete('/{id}')
def delete_cart(user = Depends(retrive_user), id = int):
    cart = Cart.get(id = id, user = user['id'])
    if not cart:
        return HTTPException(status_code=404, detail="This Cart Does not exists.")
    Cart.delete(id = cart.id)
    return HTTPException(status_code=402, detail="Cart Deleted.")