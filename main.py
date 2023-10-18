from fastapi import FastAPI,Depends,status,Response
import schemas
import models
from typing import Optional
from database import engine,SessionLocal
from sqlalchemy.orm import Session

mochi = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@mochi.get("/")
def welcome():
    return "welcome to the store"

@mochi.post("/add-new-book",status_code=status)
def create_our_book(create: schemas.creatingbooks, db: Session = Depends(get_db)):
    new_book=models.Book(id=create.id,Book_Name=create.Book_Name,Pages=create.Pages)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@mochi.get("/all_books",status_code=200)
def total(db: Session = Depends(get_db)):
    books=db.query(models.Book).all()
    return books

@mochi.get("/all_books/{id}",status_code=status.HTTP_200_OK)
def show(id:int,response:Response ,db: Session = Depends(get_db)):
    book=db.query(models.Book).filter(models.Book.id==id).first()
    if not book:
        response.status_code=status.HTTP_404_NOT_FOUND
        return f"Book with the ID {id} does not exist"

    return book

@mochi.delete("/all_books/{id}")
def pick_a_book(id,db: Session = Depends(get_db)):
    book=db.query(models.Book).filter(models.Book.id==id).delete(synchronize_session=False)
    db.commit()
    return f"the book {book} you asked for is picked up from the shelf."
    

