from faker import Faker
from sqlalchemy.orm import Session
from models import Ticket
import random
from datetime import datetime, timedelta

fake = Faker()

def seed_tickets(db: Session, count: int = 100000):
    """Seed the database with fake ticket data"""
    
    # Clear existing data
    db.query(Ticket).delete()
    db.commit()
    
    statuses = ["open", "closed", "in-progress"]
    priorities = ["low", "medium", "high"]
    agents = [
        "John Smith", "Sarah Johnson", "Mike Davis", "Emily Brown", 
        "David Wilson", "Lisa Anderson", "Chris Taylor", "Amanda White"
    ]
    
    tickets = []
    batch_size = 1000
    
    print(f"Generating {count} tickets...")
    
    for i in range(count):
        # Generate realistic ticket data
        created_date = fake.date_time_between(start_date='-2y', end_date='now')
        
        ticket = Ticket(
            subject=fake.sentence(nb_words=6)[:-1],  # Remove the period
            body=fake.text(max_nb_chars=500),
            status=random.choice(statuses),
            priority=random.choice(priorities),
            customer_email=fake.email(),
            customer_name=fake.name(),
            assigned_agent=random.choice(agents) if random.random() > 0.3 else None,
            created_at=created_date,
            updated_at=created_date + timedelta(hours=random.randint(0, 48))
        )
        
        tickets.append(ticket)
        
        # Batch insert for better performance
        if len(tickets) >= batch_size:
            db.bulk_save_objects(tickets)
            db.commit()
            tickets = []
            if (i + 1) % 10000 == 0:
                print(f"Inserted {i + 1} tickets...")
    
    # Insert remaining tickets
    if tickets:
        db.bulk_save_objects(tickets)
        db.commit()
    
    print(f"Successfully seeded {count} tickets!")
