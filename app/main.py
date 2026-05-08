from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import issues, goods, articles, requests

app = FastAPI(title="Pixel Lab API", description="API для сайта Pixel Lab", version="1.0.0")

# Разрешаем запросы с любых источников (для теста)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(issues.router)
app.include_router(goods.router)
app.include_router(articles.router)
app.include_router(requests.router)

@app.get("/")
async def root():
    return {"message": "Pixel Lab API работает!", "status": "ok"}

@app.get("/health")
async def health():
    return {"status": "healthy"}