
from fastapi import FastAPI, Depends, HTTPException ,status ,Response , APIRouter

from .. import models , schemas ,oauth2

from ..database import get_db

from sqlalchemy.orm import Session

from typing import List , Optional

from sqlalchemy import func

router=APIRouter(
    prefix="/sqlalchemy/post",
    tags=["Posts"]
    )

# Root health-check route
@router.get("/health")
def home():
    """Health check endpoint that returns a simple greeting message."""
    return {"message": "Hello World"}




# =====================================================================================================
# GET
# =====================================================================================================

@router.get("/getAllPosts", response_model=List[schemas.PostOut])
def get_all_posts_sqlalchemy(db: Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user), limit: int = 10,skip :int = 0, search : Optional[str] =""):
    """Retrieve all posts from the database using SQLAlchemy ORM."""

    posts = db.query(models.Post,func.count(models.Votes.post_id).label("votes"))\
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search))\
        .offset(skip).limit(limit).all()

    return [{"Post": post, "votes": votes} for post, votes in posts]


@router.get("/getPostFromDB/{id}", response_model=schemas.PostOut)
def get_post_by_id_sqlalchemy(id: int, db: Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    """Retrieve a specific post by ID from the database using SQLAlchemy. Returns 404 if post not found."""
    post = db.query(models.Post,func.count(models.Votes.post_id).label("votes"))\
            .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)\
            .filter(models.Post.id == id)\
            .group_by(models.Post.id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not Found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this post")
    return {"Post": post[0], "votes": post[1]}

    

# =====================================================================================================
# POST
# =====================================================================================================

@router.post("/createPost", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post_in_sqlalchemy(post: schemas.CreatePost, db: Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    """Create a new post in the database using SQLAlchemy ORM. Returns the created post with 201 status."""
      # Assuming current_user is a Pydantic model with an 'id' attribute
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post




# =====================================================================================================
# DELETE
# =====================================================================================================

@router.delete("/deletePostFromDB/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_from_sqlalchemy(id: int, db: Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    """Delete a post from the database using SQLAlchemy. Returns 204 on success, 404 if post not found."""
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)  # 204 = success, no body returned


# =====================================================================================================
# PUT
# =====================================================================================================

@router.put("/updatePostInDB/{id}", response_model=schemas.Post)
def update_post_in_sqlalchemy(id: int, updated_post: schemas.UpdatePost, db: Session = Depends(get_db),current_user:int =Depends(oauth2.get_current_user)):
    """Update an existing post in the database using SQLAlchemy. Returns 404 if post not found."""
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_from_db = post_query.first()

    if post_from_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post_from_db.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this post")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
