from itertools import count
from fastapi import status, Response, HTTPException, Depends, APIRouter
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func





###################################################################
# ################################################ SQLALCHEMY REQUEST


router = APIRouter(
    prefix= "/sqlalchemys",
    tags=['Alchemy Posts']
)

#@router.get("/", response_model=List[schemas.PostVoteResponse])
@router.get("/", response_model=List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user), 
limit: int = 100, skip: int = 0, search_title: Optional[str] = ''):
    #post = db.query(models.Post).filter(models.Post.title.contains(search_title)).limit(limit).offset(skip).all()
    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, 
    isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search_title)).limit(limit).offset(skip).all()
    return post

@router.get("/users", response_model=List[schemas.PostVoteResponse])
def get_users_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, 
    isouter=True).group_by(models.Post.id).all()
    
    return post



@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.postCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    print(current_user)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

    


@router.get("/{id}", response_model=schemas.PostVoteResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, 
    isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exists")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with id: {id} does not exists"}
    return  post
    

@router.get("/users/{id}", response_model=schemas.PostVoteResponse)
def get_user_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Votes.post_id == models.Post.id, 
    isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, 
            detail= f"Post with id: {id} does not exists",
            )
### TODO
    #if post.owner_id != current_user.id:
        #raise HTTPException(
            #status_code= status.HTTP_403_FORBIDDEN,
            #detail="User is not authorized to perform requested operation"
        #)        
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with id: {id} does not exists"}
    return  post
        


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail= f"Post with id: {id} does not exists",
            )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to perform requested operation."
        )   

    post_query.delete(synchronize_session=False)  
    db.commit()      
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.postCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail= f"Post with id: {id} does not exists",
            )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to perform requested operation."
        )   

    post_query.update(updated_post.dict(), synchronize_session=False) 
    db.commit()       
    return  post