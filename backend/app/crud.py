import logging
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, text
from datetime import datetime, date
from typing import Optional, List, Dict, Any

from models import Ticket
from schemas import TicketCreate, TicketUpdate, TicketSearchResponse

logger = logging.getLogger(__name__)

class TicketCRUD:
    def create_ticket(self, db: Session, ticket: TicketCreate) -> int:
        """Create a new ticket"""
        try:
            db_ticket = Ticket(
                subject=ticket.subject,
                body=ticket.body,
                status=ticket.status,
                priority=ticket.priority,
                customer_email=ticket.customer_email,
                customer_name=ticket.customer_name,
                assigned_agent=ticket.assigned_agent
            )
            db.add(db_ticket)
            db.commit()
            db.refresh(db_ticket)
            return db_ticket.id
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating ticket: {str(e)}")
            raise
    
    def get_ticket_by_id(self, db: Session, ticket_id: int) -> Optional[Dict[str, Any]]:
        """Get a ticket by ID"""
        try:
            ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
            if ticket:
                return {
                    "id": ticket.id,
                    "subject": ticket.subject,
                    "body": ticket.body,
                    "status": ticket.status,
                    "priority": ticket.priority,
                    "customer_email": ticket.customer_email,
                    "customer_name": ticket.customer_name,
                    "assigned_agent": ticket.assigned_agent,
                    "created_at": ticket.created_at,
                    "updated_at": ticket.updated_at
                }
            return None
        except Exception as e:
            logger.error(f"Error fetching ticket {ticket_id}: {str(e)}")
            raise
    
    def update_ticket(self, db: Session, ticket_id: int, ticket_update: TicketUpdate) -> bool:
        """Update an existing ticket"""
        try:
            ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
            if not ticket:
                return False
            
            update_data = ticket_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(ticket, field, value)
            
            ticket.updated_at = datetime.utcnow()
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating ticket {ticket_id}: {str(e)}")
            raise
    
    def delete_ticket(self, db: Session, ticket_id: int) -> bool:
        """Delete a ticket"""
        try:
            ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
            if not ticket:
                return False
            
            db.delete(ticket)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting ticket {ticket_id}: {str(e)}")
            raise
    
    def search_tickets(
        self,
        db: Session,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> TicketSearchResponse:
        """Search and filter tickets with PostgreSQL optimizations"""
        try:
            # Base query
            query = db.query(Ticket)
            
            # Apply filters
            filters = []
            
            if search and search.strip():
                # Use PostgreSQL full-text search with trigram similarity
                search_term = search.strip()
                search_filter = or_(
                    Ticket.subject.ilike(f"%{search_term}%"),
                    Ticket.body.ilike(f"%{search_term}%"),
                    Ticket.customer_name.ilike(f"%{search_term}%"),
                    Ticket.customer_email.ilike(f"%{search_term}%"),
                    # PostgreSQL trigram similarity search
                    func.similarity(Ticket.subject, search_term) > 0.3,
                    func.similarity(Ticket.customer_name, search_term) > 0.3
                )
                filters.append(search_filter)
            
            if status and status.strip():
                filters.append(Ticket.status == status.strip())
            
            if priority and priority.strip():
                filters.append(Ticket.priority == priority.strip())
            
            if date_from:
                filters.append(Ticket.created_at >= date_from)
            
            if date_to:
                from datetime import datetime, time
                date_to_end = datetime.combine(date_to, time.max)
                filters.append(Ticket.created_at <= date_to_end)
            
            if filters:
                query = query.filter(and_(*filters))
            
            # Get total count efficiently
            total_count = query.count()
            
            # Apply pagination and ordering with PostgreSQL optimizations
            tickets = (query
                      .order_by(Ticket.created_at.desc())
                      .offset((page - 1) * page_size)
                      .limit(page_size)
                      .all())
            
            # Convert to dictionaries
            ticket_dicts = []
            for ticket in tickets:
                ticket_dicts.append({
                    "id": ticket.id,
                    "subject": ticket.subject,
                    "body": ticket.body,
                    "status": ticket.status,
                    "priority": ticket.priority,
                    "customer_email": ticket.customer_email,
                    "customer_name": ticket.customer_name,
                    "assigned_agent": ticket.assigned_agent,
                    "created_at": ticket.created_at,
                    "updated_at": ticket.updated_at
                })
            
            total_pages = (total_count + page_size - 1) // page_size
            
            return TicketSearchResponse(
                tickets=ticket_dicts,
                total_count=total_count,
                page=page,
                page_size=page_size,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_prev=page > 1
            )
        except Exception as e:
            logger.error(f"Error searching tickets: {str(e)}")
            raise
    
    
