from fastapi import APIRouter, Depends, HTTPException

from token_config.creator import retrive_user
from extensions.password_hasher import hash_password
from account.models import User
from account.schemas import UserModel, UserModelUpdate, DefaultBaseUserModel


router = APIRouter()


@router.get("/")
def list_users(user = Depends(retrive_user), page: int = 1, page_size: int = 20):
    if user['is_superuser'] == False:
        return HTTPException(status_code=403, detail="you can not access to this url")
    
    users = User.all().paginate(page=page, page_size=page_size)
    
    return HTTPException(status_code=200, detail=users)


@router.post("/")
def create_user(data: DefaultBaseUserModel = DefaultBaseUserModel):
    data = data.model_dump()
    try:
        User.create(username = data['username'],
                    password = hash_password(data['password']),
                    first_name = data['first_name'],
                    last_name = data['last_name'],
                    is_superuser = False)
    except Exception as e:
        return HTTPException(status_code=422 ,detail=f"Error: {e}")
    return HTTPException(status_code=201, detail=f"User {data['username']} successfully created.")

@router.get("/{id}")
def get_user(user = Depends(retrive_user), id = int):
    if user['is_superuser'] == False:
        return HTTPException(status_code=403, detail="you can not access to this url")
    
    users = User.get(id = id)
    if not users:
        return HTTPException(status_code=404, detail=f"User Not Found with id {id}")
    
    return HTTPException(status_code=200, detail=users)

@router.put("/{id}")
def update_user(user = Depends(retrive_user), id = int,data: UserModelUpdate = UserModelUpdate):
    data = data.model_dump(exclude_unset=True)
    user_data = User.get(id = id)
    
    if not int(user['id']) == int(id):
        if user['is_superuser'] == False:
            return HTTPException(status_code=403, detail=f"You cannot access to other users")
            
    
    if not user_data:
        return HTTPException(status_code=404, detail=f"User Not Found with id {id}")
    
    
    if 'username' in data:
        user_data.username = data['username']
    if 'first_name' in data:
        user_data.first_name = data['first_name']
    if 'last_name' in data:
        user_data.last_name = data['last_name']
    if 'password' in data:
        user_data.password = hash_password(data['password'])
    if 'is_superuser' in data:
        if user['is_superuser'] == True:
            user_data.is_superuser = data['is_superuser']
    
    user_data.save()
    
    return HTTPException(detail="user updated", status_code=200)

@router.delete("/{id}")
def delete_user(user = Depends(retrive_user), id = int):
    user_data = User.get(id = id)
    
    if user['is_superuser'] == False:
        return HTTPException(status_code=403, detail="you can not access to this url")

    if not user_data:
        return HTTPException(status_code=404, detail=f"User Not Found with id {id}")
    
    User.delete(id = id)
    return HTTPException(status_code=402, detail="User Deleted.")
    
    
        


@router.post("/create_superuser/", )
def create_super_user(user = Depends(retrive_user), data: DefaultBaseUserModel = DefaultBaseUserModel):
    """
        Only Superusers can create new superuser.
        
        you can create new superuser with default User.
        for more information going to `.env` file
    """
    data = data.model_dump()
    if user['is_superuser'] == False:
        return HTTPException(status_code=403, detail="you can not access to this url")
    try:
        User.create(username = data['username'],
                    password = hash_password(data['password']),
                    first_name = data['first_name'],
                    last_name = data['last_name'],
                    is_superuser = False)
    except Exception as e:
        return HTTPException(status_code=422 ,detail=f"Error: {e}")
    return HTTPException(status_code=201, detail=f"User {data['username']} successfully created.")

