from fastapi import APIRouter, Depends, Response, HTTPException, status

from sqlalchemy.orm import Session

from database import engine, get_db
from schemas import UserLogin, Token
from models import User
from utils import verify_password_hash
from oauth2 import generate_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
def login(
    user_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    query = db.query(User).filter(User.email == user_details.username)

    user = query.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Invalid credentials"
        )
    verify_password = verify_password_hash(user_details.password, user.password)

    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=f"Invalid credentials"
        )

    access_token = generate_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}
