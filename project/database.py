from fastapi import background
from fastapi.datastructures import Default
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import hashlib

SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://parzival:@localhost/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashedPassword = Column(String(256))
    dateBirth = Column(Date, index=True)
    firstName = Column(String(50), index=True)
    secondName = Column(String(50), index=True)
    firstSurname = Column(String(50), index=True)
    secondSurname = Column(String(50), index=True)
    address = Column(String(100), index=True)
    number_id = Column(Integer, index=True)
    createdAt = Column(Date, default=datetime.now)

    loan = relationship("Loan", back_populates="owner")


    __mapper_args__ = {
                    'version_id_col': dateBirth,
                    'version_id_generator': lambda v:datetime.now()
                }

    @classmethod
    def create_password(cls, hashedPassword):
        h = hashlib.md5()

        hashedPassword = h.update(hashedPassword.encode("utf-8"))
        return h.hexdigest()

class Loan(Base):
    __tablename__ = "loan"

    id = Column(Integer, primary_key=True, index=True)
    dateLoan = Column(Date, default=datetime.now)
    dateReturn = Column(Date)
    dateReturnReal = Column(Date)
    userId = Column(Integer, ForeignKey("user.id"))
    bookId = Column(Integer, ForeignKey("book.id"))

    owner = relationship("User", back_populates="loan")
    book = relationship("Book", back_populates="loan")

    __mapper_args__ = {
            'version_id_col': dateLoan,
            'version_id_generator': lambda v:datetime.now()
    }


class Book(Base):
    __tablename__= "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), index=True)
    synopsis = Column(String(250), index=True)
    debutDate = Column(Date)
    authorId = Column(Integer, ForeignKey("autor.id"))
    editorialId = Column(Integer, ForeignKey("editorial.id"))
    genreId = Column(Integer, ForeignKey("genre.id"))
    stock = Column(Integer, index=True)
    conditionId = Column(Integer, ForeignKey("condition.id"))
    loan = relationship("Loan")

    autor = relationship("Autor", back_populates="book")
    editorial = relationship("Editorial", back_populates="book")
    genre = relationship("Genre", back_populates="book")
    condition = relationship("Condition", back_populates="book")

    loan = relationship("Loan", back_populates="book")

class Autor(Base):
    __tablename__= "autor"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(25))
    firstSurname = Column(String(25))
    book = relationship("Book", back_populates="autor")

class Editorial(Base):
    __tablename__= "editorial"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25))
    address = Column(String(50))
    book = relationship("Book", back_populates="editorial")

    
class Genre(Base):
    __tablename__= "genre"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25))
    book = relationship("Book", back_populates="genre")

class Condition(Base):
    __tablename__= "condition"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(25))
    book = relationship("Book", back_populates="condition")
