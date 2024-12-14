import os

from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from coffee.models import Coffee
from coffee.schemas import *
from config.settings import UPLOAD_DIR

router = APIRouter()


# CRUD Endpoints
@router.post("/coffees/")
def create_coffee(
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
    image: UploadFile = File(...)
):
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
    }
    coffee_obj = Coffee(**coffee_data)
    coffee_obj.save()
    return coffee_obj

@router.get("/coffees/")
def list_coffees():
    coffees = Coffee.all() # Fetch all records
    
    return coffees.to_dict()

@router.get("/coffees/{coffee_id}")
def get_coffee(coffee_id: int):
    coffee = Coffee.get(id=coffee_id)
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")
    coffee_dict = coffee.__dict__
    coffee_dict["image"] = f"/uploads/{os.path.basename(coffee_dict['image'])}"
    return coffee_dict
@router.put("/coffees/{coffee_id}", response_model=CoffeeResponse)
def update_coffee(
    coffee_id: int,
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
):
    
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

@router.delete("/coffees/{coffee_id}", response_model=dict)
def delete_coffee(coffee_id: int):
    coffee = Coffee.get(id=coffee_id)
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    # Delete the image file
    if os.path.exists(coffee.image):
        os.remove(coffee.image)

    Coffee.delete(id = coffee_id)
    return {"detail": "Coffee deleted successfully"}