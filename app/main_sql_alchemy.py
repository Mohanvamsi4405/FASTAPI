# =====================================================================================================
#  STAGE 3: SQLALCHEMY (ORM)
#  Final version — all routes go through the SQLAlchemy ORM session instead of raw SQL or an in-memory list.
# =====================================================================================================

from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from .database import engine, Base, SessionLocal, get_db
from . import models, schemas , utils

models.Base.metadata.create_all(bind=engine)


print("6)Models Created and Back to app.py")

app = FastAPI()


# Root health-check route
@app.get("/")
def home():
    """Health check endpoint that returns a simple greeting message."""
    return {"message": "Hello World"}


# Simple sample route
@app.get("/mohan")
def mohan1():
    """Simple welcome route for testing."""
    return {"message": "Welcome Mohan"}


# =====================================================================================================
# GET
# =====================================================================================================

@app.get("/sqlalchemy/getAllPosts", response_model=List[schemas.Post])
def get_all_posts_sqlalchemy(db: Session = Depends(get_db)):
    """Retrieve all posts from the database using SQLAlchemy ORM."""
    posts = db.query(models.Post).all()
    return posts


@app.get("/sqlalchemy/getPostFromDB/{id}", response_model=schemas.Post)
def get_post_by_id_sqlalchemy(id: int, db: Session = Depends(get_db)):
    """Retrieve a specific post by ID from the database using SQLAlchemy. Returns 404 if post not found."""
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not Found")

    return post

@app.get("/getusers/{id}",response_model=schemas.UserOutputResponse)
def get_user_by_id(id:int,db:Session=Depends(get_db)):
    user_detail=db.query(models.Users).filter(models.Users.id==id).first()
    if user_detail is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found in Database")
    
    return user_detail
    

# =====================================================================================================
# POST
# =====================================================================================================

@app.post("/sqlalchemy/createPost", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post_in_sqlalchemy(post: schemas.CreatePost, db: Session = Depends(get_db)):
    """Create a new post in the database using SQLAlchemy ORM. Returns the created post with 201 status."""
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.post("/createUser", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user in the database using SQLAlchemy ORM. Returns the created user with 201 status."""
    
    hashed_password=utils.hashpassword(user.password)
    user.password=hashed_password
    
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# =====================================================================================================
# DELETE
# =====================================================================================================

@app.delete("/sqlalchemy/deletePostFromDB/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_from_sqlalchemy(id: int, db: Session = Depends(get_db)):
    """Delete a post from the database using SQLAlchemy. Returns 204 on success, 404 if post not found."""
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # 204 = success, no body returned


# =====================================================================================================
# PUT
# =====================================================================================================

@app.put("/sqlalchemy/updatePostInDB/{id}", response_model=schemas.Post)
def update_post_in_sqlalchemy(id: int, updated_post: schemas.UpdatePost, db: Session = Depends(get_db)):
    """Update an existing post in the database using SQLAlchemy. Returns 404 if post not found."""
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_from_db = post_query.first()

    if post_from_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
