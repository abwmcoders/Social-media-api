from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session




###################################################################
# ################################################ AUTH REQUEST

router = APIRouter(
    prefix= "/users",
    tags=['Users']
)

    
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateUserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    # Hash password which is coming from user.password
    hashed_password = utils.HashPassword(user.password)
    user.password = hashed_password
    """
    existing_user = user.email
    if existing_user == new_user.email:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail= f"User with email already exists")
    """
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model= schemas.CreateUserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"User with {id} does not exists"
        )

    return user    

