from fastapi import APIRouter, Query
from app.database import get_db_connection, close_db_connection

router = APIRouter(prefix="/api/requests", tags=["requests"])

@router.get("/")
def get_all_requests(
    status: str = Query(None),
    type: str = Query(None),
    search: str = Query(None)
):
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = "SELECT * FROM requests WHERE 1=1"
    params = []
    
    if status and status != "all":
        query += " AND status = %s"
        params.append(status)
    
    if type and type != "all":
        query += " AND request_type = %s"
        params.append(type)
    
    if search:
        query += " AND (name ILIKE %s OR phone ILIKE %s)"
        params.append(f"%{search}%")
    
    query += " ORDER BY created_at DESC"
    
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    close_db_connection(conn)
    
    return rows

@router.post("/")
def create_request(
    request_type: str,
    name: str,
    phone: str,
    service: str = None,
    product: str = None,
    message: str = None
):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        """INSERT INTO requests (request_type, name, phone, service, product, message, status)
           VALUES (%s, %s, %s, %s, %s, %s, 'new') RETURNING *""",
        (request_type, name, phone, service, product, message)
    )
    
    row = cur.fetchone()
    conn.commit()
    cur.close()
    close_db_connection(conn)
    
    return row