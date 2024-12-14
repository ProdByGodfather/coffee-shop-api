from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
from abarorm import SQLiteModel
from abarorm.fields import sqlite

# Database configuration
db_conf = {
    'db_name': "coffee.db"
}

# SQLiteModel for Coffee
class Coffee(SQLiteModel):
    coffeeName = sqlite.CharField(max_length=200)
    coffeeType = sqlite.CharField(max_length=200)
    rate = sqlite.FloatField()
    commentCount = sqlite.IntegerField()
    image = sqlite.CharField(max_length=500)
    price = sqlite.FloatField()
    isLiked = sqlite.BooleanField()
    desc = sqlite.CharField()
    buyCount = sqlite.IntegerField()
    coffeeShopLocation = sqlite.CharField(max_length=1000)
    coffeeAddress = sqlite.CharField()

    class Meta:
        db_config = db_conf

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

# Initialize FastAPI app
app = FastAPI()

# Mount the uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Create the Coffee table if not exists
Coffee.create_table()

# CRUD Endpoints
@app.post("/coffees/")
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

@app.get("/coffees/")
def list_coffees():
    coffees = Coffee.all() # Fetch all records
    
    return coffees.to_dict()

@app.get("/coffees/{coffee_id}")
def get_coffee(coffee_id: int):
    coffee = Coffee.get(id=coffee_id)
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")
    coffee_dict = coffee.__dict__
    coffee_dict["image"] = f"/uploads/{os.path.basename(coffee_dict['image'])}"
    return coffee_dict
@app.put("/coffees/{coffee_id}", response_model=CoffeeResponse)
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

@app.delete("/coffees/{coffee_id}", response_model=dict)
def delete_coffee(coffee_id: int):
    coffee = Coffee.get(id=coffee_id)
    if not coffee:
        raise HTTPException(status_code=404, detail="Coffee not found")

    # Delete the image file
    if os.path.exists(coffee.image):
        os.remove(coffee.image)

    Coffee.delete(id = coffee_id)
    return {"detail": "Coffee deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, host="localhost", port=8513)