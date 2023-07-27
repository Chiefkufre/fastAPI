from typing import Optional, List
from fastapi import Response, status, HTTPException, Depends, APIRouter


# Internal import
from models import Event, User
from schemas import *
from database import engine, get_db
from utils import generate_hash

from oauth2 import get_current_user

# Sqlalchemy import
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    email = db.query(User).filter(User.email == user.email).first()
    if email:
        return {"detail": f"user with this email: {email}, already exist"}
    try:
        hash_password = generate_hash(user.password)
        user.password = hash_password

        # cleanedd email address

        # cleaned_email = user.email.strip().replace(" ", "")
        # user.email = cleaned_email
        new_user = User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"user": new_user}
    except:
        return HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="user cannot be created, please try again",
        )


# Retrive user data from db


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserGrab])
def retrive_user(user: UserGrab, db: Session = Depends(get_db), current_user:int=Depends(get_current_user)):
    users = db.query(User).all()
    return users


# Retrive users by id
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserRead)
def get_user_by_id(id: int, db: Session = Depends(get_db), current_user: int=Depends(get_current_user)):
    query = db.query(User).filter(User.id == id).first()

    if query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id: {id}, was not found",
        )
    else:
        return query

@router.put("/{id}", status_code=status.HTTP_205_RESET_CONTENT)
def update_user_detail(id:int, _user: UserUpdate, db:Session= Depends(get_db), current_user: int=Depends(get_current_user)):

    update_user = db.query(User).filter(User.id == id)
    
    
    user = update_user.first()

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="user with this id does not exit"
        )
    
    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
            detail="You are not permitted to perform this operation"
        )
    

    update_user.update(
        _user.dict(), synchronize_session=False

    )
    db.commit()

    return user
    


# Delete users by id


@router.delete("/{id}", response_model=UserRead)
def delete_users_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    query = db.query(User).filter(User.id == id)
    
    user = query.first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with the id: {id}, was not found",
        )
    
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this operation"
            )
    else:
        db.delete(query)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
