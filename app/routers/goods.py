from fastapi import APIRouter, Query
from app.database import get_db_connection, close_db_connection

router = APIRouter(prefix="/api/goods", tags=["goods"])

@router.get("/")
def get_all_goods(
    category: str = Query(None),
    type: str = Query(None),
    search: str = Query(None)
):
    conn = get_db_connection()
    cur = conn.cursor()
    
    query = "SELECT * FROM goods WHERE 1=1"
    params = []
    
    if category and category != "all":
        query += " AND category = %s"
        params.append(category)
    
    if type and type != "all":
        query += " AND type = %s"
        params.append(type)
    
    if search:
        query += " AND (name ILIKE %s OR description ILIKE %s)"
        params.append(f"%{search}%")
    
    query += " ORDER BY id"
    
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    close_db_connection(conn)
    
    return rows

@router.get("/{goods_id}")
def get_goods(goods_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM goods WHERE id = %s", (goods_id,))
    row = cur.fetchone()
    
    cur.close()
    close_db_connection(conn)
    
    if not row:
        return {"error": "Товар не найден"}
    
    return row