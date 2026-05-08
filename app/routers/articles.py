from fastapi import APIRouter, Query
from database import get_db, close_db

router = APIRouter(prefix="/api/articles", tags=["articles"])

@router.get("/")
async def get_all_articles(search: str = Query(None)):
    conn = await get_db()
    
    if search:
        rows = await conn.fetch(
            "SELECT * FROM articles WHERE title ILIKE $1 OR content ILIKE $1 ORDER BY id",
            f"%{search}%"
        )
    else:
        rows = await conn.fetch("SELECT * FROM articles ORDER BY id")
    
    await close_db(conn)
    
    result = []
    for row in rows:
        result.append(dict(row))
    
    return result

@router.get("/{article_id}")
async def get_article(article_id: str):
    conn = await get_db()
    row = await conn.fetchrow("SELECT * FROM articles WHERE id = $1", article_id)
    await close_db(conn)
    
    if not row:
        return {"error": "Статья не найдена"}
    
    return dict(row)