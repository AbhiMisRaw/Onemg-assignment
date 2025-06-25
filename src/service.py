from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .schema import UserRegsiter, User, UserLogin, UserUpdate
from .model import User as UserModel
from .util import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    get_user_by_email, 
    convert_user_model_to_schema
    )

database = []


def create_user(user : UserRegsiter, db:Session):
    """
    creates the user.
    """
    user_object = {**user.model_dump()}
    is_email_exist = get_user_by_email(user.email, db)
    if is_email_exist:
        raise Exception("Email is already in use."
        )
    
    user_object["password"] = str(get_password_hash(user.password))
    # database.append(user_object)
    new_user = UserModel(**user_object)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return User(id=new_user.id ,**user_object)


def login_user(user: UserLogin, db: Session):
    db_user = get_user_by_email(user.email, db)
    if not db_user:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail="User not found.")
    
    result = verify_password(user.password, db_user.password)
    if result:
        response = {}
        payload = {"sub":db_user.email}
        token = create_access_token(payload)
        response["token"] = str(token)
        response["user"] = convert_user_model_to_schema(user=db_user)
        return response
    
    else:
        raise Exception("Email or Password is incorrect.") 
    

def fetch_user_by_id(id: int, db: Session):
    """
    fetch the user by User Id
    """
    user = db.query(UserModel).filter(UserModel.id == id).first()
    if user:
        return convert_user_model_to_schema(user)
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found.")


def update_user_by_id(user_id: int, user_update: UserUpdate, db: Session):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    new_email = user_update.email
    if new_email:
        check_email_duplicate = db.query(UserModel).filter(UserModel.email == new_email).first()
        if check_email_duplicate:
            raise HTTPException(status_code=404, detail="Email already exist.")
        db_user.email = user_update.email
    
    # Update other optional fields
    if user_update.name is not None:
        db_user.name = user_update.name
    if user_update.age is not None:
        db_user.age = user_update.age
    if user_update.city is not None:
        db_user.city = user_update.city

    db.commit()
    db.refresh(db_user)
    return convert_user_model_to_schema(db_user)

