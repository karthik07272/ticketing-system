from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from datetime import date
import uvicorn
import logging
from contextlib import asynccontextmanager

from database import get_db, test_connection, create_database
from schemas import TicketCreate, TicketUpdate, TicketResponse, TicketSearchResponse
from app.crud import TicketCRUD
from seed_data import seed_tickets
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting Rule-Based Support Assistant API with PostgreSQL...")
    
    # Test database connection
    if not test_connection():
        logger.error("Failed to connect to PostgreSQL database")
        raise Exception("Database connection failed")
    
    # Create database tables
    try:
        create_database()
        logger.info("Database tables ready")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise    
    yield
    
    logger.info("Shutting down Support Ticket System...")

app = FastAPI(
    title="Support Ticket System",
    description="support ticket system with PostgreSQL",
    version="1.0.0"
)

# CORS middleware - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize CRUD operations
ticket_crud = TicketCRUD()

@app.get("/")
async def root():
    return {
        "message": "Support Ticekt System",
        "version": "1.0.0",
        "status": "running",
        "database": "PostgreSQL"
    }

@app.post("/create-ticket", response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate, db=Depends(get_db)):
    """Create a new support ticket"""
    try:
        ticket_id = ticket_crud.create_ticket(db, ticket)
        created_ticket = ticket_crud.get_ticket_by_id(db, ticket_id)
        return created_ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating ticket: {str(e)}")

@app.get("/get-ticket-by-id", response_model=TicketResponse)
async def get_ticket_by_id(id: int, db=Depends(get_db)):
    """Get a ticket by ID"""
    ticket = ticket_crud.get_ticket_by_id(db, id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.put("/update-ticket", response_model=TicketResponse)
async def update_ticket(id: int, ticket_update: TicketUpdate, db=Depends(get_db)):
    """Update an existing ticket"""
    try:
        success = ticket_crud.update_ticket(db, id, ticket_update)
        if not success:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        updated_ticket = ticket_crud.get_ticket_by_id(db, id)
        return updated_ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating ticket: {str(e)}")

@app.delete("/delete-ticket")
async def delete_ticket(id: int, db=Depends(get_db)):
    """Delete a ticket"""
    try:
        success = ticket_crud.delete_ticket(db, id)
        if not success:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        return {"message": "Ticket deleted successfully", "id": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting ticket: {str(e)}")

@app.get("/search-tickets", response_model=TicketSearchResponse)
async def search_tickets(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db=Depends(get_db)
):
    """Search, filter, and paginate tickets with optimized performance"""
    try:
        result = ticket_crud.search_tickets(
            db, page, page_size, search, status, priority, date_from, date_to
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching tickets: {str(e)}")

@app.post("/seed-database")
async def seed_database(count: int = Query(100000), db=Depends(get_db)):
    """Seed the database with sample tickets"""
    try:
        seed_tickets(db, count)
        return {"message": f"Successfully seeded {count} tickets", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error seeding database: {str(e)}")


