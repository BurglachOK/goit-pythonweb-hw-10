from datetime import date, timedelta
from typing import List, Optional

from sqlalchemy import or_, extract, and_
from sqlalchemy.orm import Session
from models import Contact
from schemas import ContactCreate, ContactUpdate

def get_contacts(db: Session, skip: int = 0, limit: int = 100) -> List[Contact]:
    """
    Retrieve a list of contacts with pagination.
    """
    return db.query(Contact).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int) -> Optional[Contact]:
    """
    Retrieve a single contact by its ID.
    """
    return db.query(Contact).filter(Contact.id == contact_id).first()

def create_contact(db: Session, contact: ContactCreate) -> Contact:
    """
    Create a new contact record.
    """
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactUpdate) -> Optional[Contact]:
    """
    Update an existing contact. Supports partial updates (PATCH).
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        update_data = contact.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contact, key, value)
        
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int) -> Optional[Contact]:
    """
    Remove a contact record from the database.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def search_contacts(db: Session, query: str) -> List[Contact]:
    """
    Search contacts by first name, last name, or email using case-insensitive matching.
    """
    return db.query(Contact).filter(
        or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.last_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%")
        )
    ).all()

def get_upcoming_birthdays(db: Session) -> List[Contact]:
    """
    Retrieve contacts with birthdays within the next 7 days using SQL filters.
    """
    today = date.today()
    days_range = []
    
    for i in range(8):
        future_date = today + timedelta(days=i)
        days_range.append((future_date.month, future_date.day))

    date_filters = [
        and_(
            extract('month', Contact.birthday) == m,
            extract('day', Contact.birthday) == d
        ) for m, d in days_range
    ]

    return db.query(Contact).filter(or_(*date_filters)).all()