from fastapi import APIRouter, Query
from database import get_db, close_db

router = APIRouter(prefix="/api/issues", tags=["issues"])

@router.get("/")
async def get_all_issues(
    device_type: str = Query(None),
    category: str = Query(None),
    search: str = Query(None)
):
    conn = await get_db()
    
    query = "SELECT * FROM issues WHERE 1=1"
    params = []
    param_count = 1
    
    if device_type and device_type != "all":
        query += f" AND device_type = ${param_count}"
        params.append(device_type)
        param_count += 1
    
    if category and category != "all":
        query += f" AND category = ${param_count}"
        params.append(category)
        param_count += 1
    
    if search:
        query += f" AND (title ILIKE $${param_count} OR symptoms ILIKE $${param_count})"
        params.append(f"%{search}%")
    
    query += " ORDER BY id"
    
    rows = await conn.fetch(query, *params)
    await close_db(conn)
    
    result = []
    for row in rows:
        result.append(dict(row))
    
    return result

@router.get("/{issue_id}")
async def get_issue(issue_id: int):
    conn = await get_db()
    row = await conn.fetchrow("SELECT * FROM issues WHERE id = $1", issue_id)
    await close_db(conn)
    
    if not row:
        return {"error": "Неисправность не найдена"}
    
    return dict(row)