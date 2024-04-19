from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from  . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id:  int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

# @app.delete("/delete/{id}")
# def delete(id:int,db:Session=Depends(get_db),status_code=status.HTTP_204_NO_CONTENT):
#     delete_post= db._query(models.User).filter(models.User.id==id)
#     if delete_post == None :
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User does not exist with this id")
#     else:
#         delete_post.delete(synchronize_session=False)
#         db.commit()
#         return Response(status_code=HTTP_204_NO_CONTENT)
# @app.put("/update/{id}")
# def update(id:int,product:user,db:Session=Depends(get_db)):
#     update_post.first()
#     if update_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with such id: {id} does not exist")
#     else:
#         update_post.update(product,synchronize_session=False)
#         db.commit
#     return update_post.first()

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id=user_id)
    return {"message": "User deleted successfully"}

@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.update_user(db, user_id=user_id, user_update=user_update)
    return {"message": "User updated successfully"}
