from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta


from . import dependencies
from .. import crud, schemas

router = APIRouter(
    tags=["Users"],
    prefix="/users",
)


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dependencies.get_db)):
    user = dependencies.authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = dependencies.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/create")
async def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    response = crud.create_user_in_db(db=db, user=user)
    return {"message": "User created successfully", "status": 200, "data": response}


@router.post("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(dependencies.get_current_user)):
    return current_user


@router.get("/all")
async def read_users(token: str = Depends(dependencies.oauth2_scheme), skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, token: str = Depends(dependencies.oauth2_scheme), db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
