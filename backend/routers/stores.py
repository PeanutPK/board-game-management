from fastapi import APIRouter, HTTPException
from typing import List
from models import Store, StoreCreate

router = APIRouter(prefix="/stores", tags=["stores"])

# In-memory store for boilerplate purposes
stores_db: List[Store] = [
    Store(
        id=1,
        name="Board Game Hub",
        location="123 Main St, Bangkok",
        contact="info@boardgamehub.com",
    ),
    Store(
        id=2,
        name="Play & Borrow",
        location="456 Game Ave, Chiang Mai",
        contact="hello@playandborrow.com",
    ),
]
_next_id = 3


@router.get("/", response_model=List[Store])
def list_stores():
    return stores_db


@router.get("/{store_id}", response_model=Store)
def get_store(store_id: int):
    for store in stores_db:
        if store.id == store_id:
            return store
    raise HTTPException(status_code=404, detail="Store not found")


@router.post("/", response_model=Store, status_code=201)
def create_store(store: StoreCreate):
    global _next_id
    new_store = Store(id=_next_id, **store.model_dump())
    _next_id += 1
    stores_db.append(new_store)
    return new_store


@router.put("/{store_id}", response_model=Store)
def update_store(store_id: int, store: StoreCreate):
    for index, existing in enumerate(stores_db):
        if existing.id == store_id:
            updated = Store(id=store_id, **store.model_dump())
            stores_db[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Store not found")


@router.delete("/{store_id}", status_code=204)
def delete_store(store_id: int):
    for index, store in enumerate(stores_db):
        if store.id == store_id:
            stores_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Store not found")
