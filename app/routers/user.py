
from sqlalchemy.orm import Session

from fastapi import FastAPI, Response , status , Depends , HTTPException , APIRouter

from .. import models , schemas , utils

from ..database import get_db

router=APIRouter(
    prefix="/sqlalchemy/user",
    tags=["Users"]
    )


@router.post("/createUser", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user in the database using SQLAlchemy ORM. Returns the created user with 201 status."""
    
    hashed_password=utils.hashpassword(user.password)
    user.password=hashed_password
    
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get("/getusers/{id}",response_model=schemas.UserOutputResponse)
def get_user_by_id(id:int,db:Session=Depends(get_db)):
    user_detail=db.query(models.Users).filter(models.Users.id==id).first()
    if user_detail is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found in Database")
    
    return user_detail
    