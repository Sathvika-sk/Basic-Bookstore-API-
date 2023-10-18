from sqlalchemy import Column, Integer, String
from database import Base

class Book(Base):
    __tablename__ = 'Books'
    id=Column(Integer,primary_key=True,index=True)
    Book_Name=Column(String)
    Pages=Column(Integer)