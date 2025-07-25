# Ticketing System Backend

FastAPI backend with SQLite database and raw SQL queries for high-performance ticket management.

## Setup

1. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

2. Run the server:
   \`\`\`bash
   cd app
   python main.py
   \`\`\`

3. API will be available at `http://localhost:8000`

## API Endpoints

- `GET /` - Health check
- `POST /create-ticket` - Create new ticket
- `GET /get-ticket-by-id?id={id}` - Get ticket by ID
- `PUT /update-ticket?id={id}` - Update ticket
- `DELETE /delete-ticket?id={id}` - Delete ticket
- `GET /search-tickets` - Search and filter tickets
- `POST /seed-database?count={count}` - Seed database
- `GET /stats` - Get statistics

## Database

Uses SQLite for development. The database file `tickets.db` will be created automatically.
\`\`\`

## Frontend Structure
