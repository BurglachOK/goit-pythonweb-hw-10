from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from db import get_db, engine
from models import Base
from schemas import ContactResponse, ContactCreate, ContactUpdate
import crud


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Premium Contacts API",
    description="A professional API for managing personal and business contacts",
    version="1.1.0"
)

# --- Endpoints ---

@app.get("/contacts/", response_model=List[ContactResponse], tags=["Contacts"])
def read_contacts(
    skip: int = Query(0, ge=0), 
    limit: int = Query(100, ge=1, le=500), 
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of contacts with pagination support.
    """
    return crud.get_contacts(db=db, skip=skip, limit=limit)

@app.post("/contacts/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED, tags=["Contacts"])
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    """
    Create a new contact entry in the system.
    """
    return crud.create_contact(db=db, contact=contact)

@app.get("/contacts/search", response_model=List[ContactResponse], tags=["Search & Events"])
def search_contacts(
    query: str = Query(..., min_length=1, description="Search by name, last name or email"), 
    db: Session = Depends(get_db)
):
    """
    Search for contacts using a keyword.
    """
    return crud.search_contacts(db=db, query=query)

@app.get("/contacts/birthdays", response_model=List[ContactResponse], tags=["Search & Events"])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    """
    Get a list of contacts who have birthdays in the next 7 days.
    """
    return crud.get_upcoming_birthdays(db=db)

@app.get("/contacts/{contact_id}", response_model=ContactResponse, tags=["Contacts"])
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Fetch a specific contact by its unique ID.
    """
    db_contact = crud.get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Contact with ID {contact_id} not found"
        )
    return db_contact

@app.patch("/contacts/{contact_id}", response_model=ContactResponse, tags=["Contacts"])
def update_existing_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    """
    Update an existing contact partially (PATCH).
    """
    db_contact = crud.update_contact(db=db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Contacts"])
def delete_existing_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Permanently remove a contact from the database.
    """
    db_contact = crud.delete_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return None