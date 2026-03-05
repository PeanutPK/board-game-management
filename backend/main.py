from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import games, stores

app = FastAPI(
    title="Board Game Management API",
    description="API for managing board game stock across stores",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(games.router, prefix="/api")
app.include_router(stores.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Board Game Management API", "docs": "/docs"}
