from fastapi import APIRouter, Query
from database import get_db, close_db

router = APIRouter(prefix="/api/requests", tags=["requests"])

@router.get("/")
async def get_all_requests(
    status: str = Query(None),
    type: str = Query(None),
    search: str = Query(None)
):
    conn = await get_db()
    
    query = "SELECT * FROM requests WHERE 1=1"
    params = []
    param_count = 1
    
    if status and status != "all":
        query += f" AND status = ${param_count}"
        params.append(status)
        param_count += 1
    
    if type and type != "all":
        query += f" AND request_type = ${param_count}"
        params.append(type)
        param_count += 1
    
    if search:
        query += f" AND (name ILIKE $${param_count} OR phone ILIKE $${param_count})"
        params.append(f"%{search}%")
    
    query += " ORDER BY created_at DESC"
    
    rows = await conn.fetch(query, *params)
    await close_db(conn)
    
    result = []
    for row in rows:
        result.append(dict(row))
    
    return result

@router.post("/")
async def create_request(
    request_type: str,
    name: str,
    phone: str,
    service: str = None,
    product: str = None,
    message: str = None
):
    conn = await get_db()
    
    row = await conn.fetchrow(
        """INSERT INTO requests (request_type, name, phone, service, product, message, status)
           VALUES ($1, $2, $3, $4, $5, $6, 'new') RETURNING *""",
        request_type, name, phone, service, product, message
    )
    
    await close_db(conn)
    return dict(row)