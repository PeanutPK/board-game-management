"""Main application setup and entry point for the board game management system."""
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import Base, engine
from app.api.v1 import auth, games, bookings, orders, users

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, description="API for managing board games, bookings, and orders.", docs_url=f"{settings.API_V_STR}/docs", redoc_url=f"{settings.API_V_STR}/redoc")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vue dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V_STR)
app.include_router(users.router, prefix=settings.API_V_STR)
app.include_router(games.router, prefix=settings.API_V_STR)
app.include_router(bookings.router, prefix=settings.API_V_STR)
app.include_router(orders.router, prefix=settings.API_V_STR)


@app.get(f"{settings.API_V_STR}/")
def read_root():
    """Root endpoint."""
    return {"message": "Board Game Management API"}


@app.get(f"{settings.API_V_STR}/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": settings.PROJECT_VERSION}