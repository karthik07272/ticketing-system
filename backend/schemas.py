from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class TicketBase(BaseModel):
    subject: str
    body: str
    status: str = "open"
    priority: str = "medium"
    customer_email: str  
    customer_name: str
    assigned_agent: Optional[str] = None

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    subject: Optional[str] = None
    body: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_agent: Optional[str] = None

class TicketResponse(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TicketSearchResponse(BaseModel):
    tickets: List[TicketResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
