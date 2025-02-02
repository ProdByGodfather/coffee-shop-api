import os

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends

from coffee.models import Coffee
from coffee.schemas import *
from config.settings import UPLOAD_DIR
from token_config.creator import retrive_user

router = APIRouter()


# CRUD Endpoints
@router.post("/")
def create_coffee(user = Depends(retrive_user), 
    coffeeName: str = Form(...),
    coffeeType: str = Form(...),
    rate: float = Form(...),
    commentCount: int = Form(...),
    price: float = Form(...),
    isLiked: bool = Form(...),
    desc: str = Form(...),
    buyCount: int = Form(...),
    coffeeShopLocation: str = Form(...),
    coffeeAddress: str = Form(...),
    image: UploadFile = File(...),
    coffeeSize: str = Form(...)
):
    if user['is_superuser'] == False:
        return HTTPException(status_code=403, detail="you can not access to this url")
    
    # Save the uploaded image
    image_path = os.path.join(UPLOAD_DIR, image.filename)
    with open(image_path, "wb") as f:
        f.write(image.file.read())

    # Create coffee object
    coffee_data = {
        "coffeeName": coffeeName,
        "coffeeType": coffeeType,
        "rate": rate,
        "commentCount": commentCount,
        "price": price,
        "isLiked": isLiked,
        "desc": desc,
        "buyCount": buyCount,
        "coffeeShopLocation": coffeeShopLocation,
        "coffeeAddress": coffeeAddress,
        "image": image_path,
        "coffeeSize": coffeeSize
    }
    coffee_obj = Coffee(**coffee_data)
    coffee_obj.save()
    return coffee_obj

@router.get("/")
def list_coffees():
    coffees = Coffee.all() # Fetch all records
    
    return coffees.to_dict()

@router.get("/{coffee_id}")
def get_coffee(coffee_id: int):
    coffee = Coffee.get(id=coffee_id)
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")
    coffee_dict = coffee.__dict__
    coffee_dict["image"] = f"/uploads/{os.path.basename(coffee_dict['image'])}"
    return coffee_dict
@router.put("/{coffee_id}", response_model=CoffeeResponse)
def update_coffee(
    coffee_id: int,
    user = Depends(retrive_user),
    coffeeName: Optional[str] = None,
    coffeeType: Optional[str] = None,
    rate: Optional[float] = None,
    commentCount: Optional[int] = None,
    price: Optional[float] = None,
    isLiked: Optional[bool] = None,
    desc: Optional[str] = None,
    buyCount: Optional[int] = None,
    coffeeShopLocation: Optional[str] = None,
    coffeeAddress: Optional[str] = None,
    image: Optional[UploadFile] = None,
    coffeeSize: Optional[str] = None
    
):
    if user['is_superuser'] == False:
        return HTTPException(status_code=403, detail="you can not access to this url")
    
    # Fetch coffee instance
    coffee = Coffee.get(id=coffee_id)
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    # Update fields if provided
    if coffeeName is not None:
        coffee.coffeeName = coffeeName
    if coffeeType is not None:
        coffee.coffeeType = coffeeType
    if rate is not None:
        coffee.rate = rate
    if commentCount is not None:
        coffee.commentCount = commentCount
    if price is not None:
        coffee.price = price
    if isLiked is not None:
        coffee.isLiked = isLiked
    if desc is not None:
        coffee.desc = desc
    if buyCount is not None:
        coffee.buyCount = buyCount
    if coffeeShopLocation is not None:
        coffee.coffeeShopLocation = coffeeShopLocation
    if coffeeAddress is not None:
        coffee.coffeeAddress = coffeeAddress
    if coffeeSize is not None:
        coffee.coffeeSize = coffeeSize

    # Handle image if provided
    if image:
        image_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(image_path, "wb") as f:
            f.write(image.file.read())
        coffee.image = image_path

    # Save changes
    coffee.save()

    # Convert to dictionary and prepare response
    coffee_dict = coffee.__dict__
    coffee_dict["image"] = f"/uploads/{os.path.basename(coffee_dict.get('image', ''))}"
    return CoffeeResponse(**coffee_dict)

@router.delete("/{coffee_id}", response_model=dict)
def delete_coffee(coffee_id: int, user = Depends(retrive_user)):
    coffee = Coffee.get(id=coffee_id)
    
    if user['is_superuser'] == False:
        return HTTPException(status_code=403, detail="you can not access to this url")
    
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    # Delete the image file
    if os.path.exists(coffee.image):
        os.remove(coffee.image)

    Coffee.delete(id = coffee_id)
    return {"detail": "Coffee deleted successfully"}

@router.post("/like/{coffee_id}")
def like_coffee(coffee_id: int, user = Depends(retrive_user)):
    coffee = Coffee.get(id=coffee_id)
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")
    
    if coffee.isLiked == True:
        coffee.isLiked = False
        coffee.save()
        return {"detail": "isLiked is False"}   
    else:
        coffee.isLiked = True
        coffee.save()
        return {"detail": "isLiked is True"}   