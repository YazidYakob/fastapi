from typing import List, Optional
from fastapi import FastAPI, Body, HTTPException, Depends, APIRouter
from starlette import status
from starlette.responses import Response
from .. import models, schema, oauth2
from ..database import engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #Without SQLAlchemy
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    #With SQL Alchemy
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results


@router.get("/id/{post_id}", response_model=schema.PostOut)
def get_post(post_id: int, response: Response, db: Session = Depends(get_db)):
    # Without SQL Alchemy
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(post_id),))
    # post = cursor.fetchone()

    #With SQL Alchemy
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == post_id).first()

    if post:
        return results
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post ID does not exist.")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.PostResponse)
def create_posts(payload: schema.PostCreate, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    # Without SQL Alchemy
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (payload.title, payload.content, payload.published))
    # post = cursor.fetchone()
    # conn.commit()
    #With SQL Alchemy
    new_post = models.Post(poster_user_id=user.uid, **payload.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/id/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):

    #Without SQL Alchemy
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(post_id),))
    # post = cursor.fetchone()
    # conn.commit()

    #With SQL Alchemy
    query = db.query(models.Post).filter(models.Post.id == post_id)
    post = query.first()

    if query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post by the ID [{post_id}] does not exist.")

    if user.uid != post.poster_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not the owner of post id [{post_id}] does not exist.")

    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/uid/{uid}", response_model=List[schema.PostResponse])
def get_post_by_user(uid: int, db: Session = Depends(get_db)):
    user_posts = db.query(models.Post).filter(models.Post.poster_user_id == uid).all()
    print(user_posts)
    return user_posts

@router.get("/my_posts", response_model=List[schema.PostResponse])
def get_post_by_user(db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):

    user_posts = db.query(models.Post).filter(models.Post.poster_user_id == user.uid).all()
    print(user_posts)
    return user_posts




@router.put("/id/{post_id}", response_model=schema.PostResponse)
def update_post(post_id: int, updated_post: schema.PostUpdate, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    #Without SQL Alchemy
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(post_id)))
    # post = cursor.fetchone()
    # conn.commit()

    #With SQL Alchemyßßßß

    #Create Query Database WHERE POSTID = HEADER ID
    query = db.query(models.Post).filter(models.Post.id == post_id)
    #Query the database and get result
    post = query.first()

    #Return Errors:
    #Error Post Not Found
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post by the ID [{post_id}] does not exist.")
    #If uid == poster_user_id
    if post.poster_user_id != user.uid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You are not the owner of this post, [{post_id}] does not exist.")

    query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return query.first()

