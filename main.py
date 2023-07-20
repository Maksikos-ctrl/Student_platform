
import uuid
import re
import conf
import uvicorn

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator
from fastapi import FastAPI

from fastapi.routing import APIRouter
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID




# create async engine for interacting with database
# echo = True for logging purposes(логирование == запись и хранение информации о событиях, происходящих в системе)
engine = conf.create_async_engine(conf.REAL_DATABASE_URL, future=True, echo=True)


# create session for the interaction with database
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


#############################################
#? BLOCK OF DB MODELS
#############################################

Base = declarative_base()




class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    is_active = Column(Boolean(), default=True)



#############################################
#! BLOCK FOR INTERACTING WITH DB IN BUSSINESS CONTEXT
#############################################


class UserModifying:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


    async def create_user(self, name: str, surname: str, email: str) -> User:
        new_user = User(name=name, surname=surname, email=email)
        self.db_session.add(new_user)
        await self.db_session.commit()
        return new_user

    

#############################################
#? BLOCK API WITH MODELS 
##############################################


LETTER_MATCH_PATTERN = re.compile(r"[a-zA-Z\-]+$")


class TunedModel(BaseModel):
    #! will be json-ize everything which will go there
    class Config:
        orm_mode = True 


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool
            


class UserCreate(TunedModel):
    name: str
    surname: str
    email: EmailStr

    @validator("name", "surname")
    def validate_name(cls, val):
        if not LETTER_MATCH_PATTERN.match(val):
            raise HTTPException(status_code=422, detail="name must contain only letters")
        return val  


    @validator("name", "surname")
    def validate_surname(cls, val):
        if not LETTER_MATCH_PATTERN.match(val):
            raise HTTPException(status_code=422, detail="surname must contain only letters")
        return val   
    


#############################################
#? BLOCK WITH API ROUTES
#############################################    

app = FastAPI(title="studentska-platforma-znamok")

router = APIRouter()

async def _create_new_user(body: UserCreate) -> User:
    async with async_session() as session:
        async with session.begin():
            user_modifying = UserModifying(db_session=session)
            new_user = await user_modifying.create_user(name=body.name, surname=body.surname, email=body.email)
            return User(user_id=new_user.user_id, name=new_user.name, surname=new_user.surname, email=new_user.email, is_active=new_user.is_active)
        




    


    
            










