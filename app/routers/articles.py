from fastapi import APIRouter, Query
from app.database import get_db_connection, close_db_connection

router = APIRouter(prefix="/api/articles", tags=["articles"])

@router.get("/")
def get_all_articles(search: str = Query(None)):
    conn = get_db_connection()
    cur = conn.cursor()
    
    if search:
        cur.execute(
            "SELECT * FROM articles WHERE title ILIKE %s OR content ILIKE %s ORDER BY id",
            (f"%{search}%", f"%{search}%")
        )
    else:
        cur.execute("SELECT * FROM articles ORDER BY id")
    
    rows = cur.fetchall()
    cur.close()
    close_db_connection(conn)
    
    return rows

@router.get("/{article_id}")
def get_article(article_id: str):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
    row = cur.fetchone()
    
    cur.close()
    close_db_connection(conn)
    
    if not row:
        return {"error": "Статья не найдена"}
    
    return row