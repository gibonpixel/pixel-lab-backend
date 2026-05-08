from fastapi import APIRouter, Query
from app.database import get_db_connection, close_db_connection

router = APIRouter(prefix="/api/issues", tags=["issues"])

@router.get("/")
def get_all_issues(
    device_type: str = Query(None),
    category: str = Query(None),
    search: str = Query(None)
):
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = "SELECT * FROM issues WHERE 1=1"
    params = []
    
    if device_type and device_type != "all":
        query += " AND device_type = %s"
        params.append(device_type)
    
    if category and category != "all":
        query += " AND category = %s"
        params.append(category)
    
    if search:
        query += " AND (title ILIKE %s OR symptoms ILIKE %s)"
        params.append(f"%{search}%")
    
    query += " ORDER BY id"
    
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    close_db_connection(conn)
    
    return rows

@router.get("/{issue_id}")
def get_issue(issue_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM issues WHERE id = %s", (issue_id,))
    row = cur.fetchone()
    
    cur.close()
    close_db_connection(conn)
    
    if not row:
        return {"error": "Неисправность не найдена"}
    
    return row