from fastapi import HTTPException, APIRouter, Depends

from fastapi.security import HTTPBasicCredentials

from ..schemas import UserRequesModel, UserResponseModel

from ..database import User

from .utilits import get_db

from sqlalchemy.orm import Session

router = APIRouter(prefix="/users")

@router.post("/user", response_model=UserResponseModel)
async def create_user(user: UserRequesModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(409, "El usuario ingresado ya esta en uso, intente usar otro.")

    hash_password = User.create_password(user.hashedPassword)

    db_user = User(
        email = user.email,
        hashedPassword = hash_password,
        dateBirth = user.dateBirth,
        firstName = user.firstName,
        secondName = user.secondName,
        firstSurname = user.firstSurname,
        secondSurname = user.secondSurname,
        address = user.address,
        number_id = user.number_id,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponseModel(
        id=db_user.id, 
        email=user.email
    )