from fastapi import APIRouter, Query
from database import get_db, close_db

router = APIRouter(prefix="/api/goods", tags=["goods"])

@router.get("/")
async def get_all_goods(
    category: str = Query(None),
    type: str = Query(None),
    search: str = Query(None)
):
    conn = await get_db()
    
    query = "SELECT * FROM goods WHERE 1=1"
    params = []
    param_count = 1
    
    if category and category != "all":
        query += f" AND category = ${param_count}"
        params.append(category)
        param_count += 1
    
    if type and type != "all":
        query += f" AND type = ${param_count}"
        params.append(type)
        param_count += 1
    
    if search:
        query += f" AND (name ILIKE $${param_count} OR description ILIKE $${param_count})"
        params.append(f"%{search}%")
    
    query += " ORDER BY id"
    
    rows = await conn.fetch(query, *params)
    await close_db(conn)
    
    result = []
    for row in rows:
        result.append(dict(row))
    
    return result

@router.get("/{goods_id}")
async def get_goods(goods_id: int):
    conn = await get_db()
    row = await conn.fetchrow("SELECT * FROM goods WHERE id = $1", goods_id)
    await close_db(conn)
    
    if not row:
        return {"error": "Товар не найден"}
    
    return dict(row)