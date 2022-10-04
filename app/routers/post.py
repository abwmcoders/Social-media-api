import time
from fastapi import status, Response, HTTPException, APIRouter
from .. import schemas
import psycopg2
from  psycopg2.extras import RealDictCursor

router = APIRouter(
    prefix= "/posts",
    tags=['Posts']
)

while True:
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='fastapi', 
            user='postgres', 
            password='Mbmalikoo1',
            cursor_factory=RealDictCursor,
            )
        cursor = conn.cursor()
        print("Succesfully connected to database")
        break
    except Exception as error:
        print('Connection database failed')
        print('Error was', error)
        time.sleep(5)




@router.get("/")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@router.post("/", status_code= status.HTTP_201_CREATED)
def create_post(post: schemas.postCreate):
    #cursor.execute(f"INSERT INTO posts (title, content, published) VALUES({post.title},
    #  {post.content}, {post.published})")
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING * """, 
    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {
        "data": new_post
    }    


@router.get("/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id), ))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exists")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"Post with id: {id} does not exists"}
    return {
        "post detail": post
    }


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id), ))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exists")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, post: schemas.postCreate):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    (post.title, post.content, post.published, str(id)), )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exists")
    return {
        "data": updated_post
    }
