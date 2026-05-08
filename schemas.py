from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class ContactBase(BaseModel):
    """
    Base schema for contact data shared across creation and updates
    """
    first_name: str = Field(..., min_length=1, max_length=50, examples=["John"])
    last_name: str = Field(..., min_length=1, max_length=50, examples=["Doe"])
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    phone: Optional[str] = Field(None, max_length=20, examples=["+1234567890"])
    birthday: Optional[date] = None
    additional_data: Optional[str] = Field(None, max_length=500)

class ContactCreate(ContactBase):
    """
    Schema for creating a new contact (requires all mandatory Base fields)
    """
    pass

class ContactUpdate(BaseModel):
    """
    Schema for updating an existing contact. 
    All fields are optional to allow partial updates (PATCH).
    """
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    additional_data: Optional[str] = None

class ContactResponse(ContactBase):
    """
    Schema for returning data to the client, including database-generated IDs
    """
    id: int
    
    model_config = ConfigDict(from_attributes=True)