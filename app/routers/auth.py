from os import access
from fastapi import Depends, HTTPException, Response, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, database

from app import database, models, utils, oauth2


router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model= schemas.Token)
def login(user_credencials: OAuth2PasswordRequestForm= Depends(),db: Session = Depends(database.get_db)):
    # schemas.user_login
    #oauth2passwordrequestfrom is going to return username and password
    # so instead of email we use username cos thats what it takes it as
    user = db.query(models.User).filter(models.User.email == user_credencials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Invalid credentials")

    if not utils.verify(plain_password= user_credencials.password, hashed_password= user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= f"Invalid credentials")


    # create a token
    # return the token
    access_token = oauth2.create_access_token(data = {"user_id": user.id, "dev": "made berry"})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


