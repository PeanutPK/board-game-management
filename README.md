# board-game-management

A website that manages the current board game stock for each store for users to lend or buy board games.

## Tech Stack

- **Frontend**: Vue 3 + Vite + Vue Router
- **Backend**: FastAPI + Pydantic + Uvicorn

## Project Structure

```
board-game-management/
├── backend/          # FastAPI backend
│   ├── main.py       # Application entry point
│   ├── models.py     # Pydantic data models
│   ├── requirements.txt
│   └── routers/
│       ├── games.py  # Board game CRUD endpoints
│       └── stores.py # Store CRUD endpoints
└── frontend/         # Vue 3 frontend
    ├── src/
    │   ├── App.vue
    │   ├── main.js
    │   ├── components/
    │   │   ├── GameCard.vue
    │   │   └── StoreCard.vue
    │   ├── views/
    │   │   ├── HomeView.vue
    │   │   ├── GamesView.vue
    │   │   └── StoresView.vue
    │   ├── router/
    │   │   └── index.js
    │   └── services/
    │       └── api.js  # Axios API client
    ├── .env.example
    └── package.json
```

## Getting Started

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.  
Interactive docs are at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # adjust VITE_API_BASE_URL if needed
npm run dev
```

The app will be available at `http://localhost:5173`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/games/` | List all board games |
| POST | `/api/games/` | Create a new board game |
| GET | `/api/games/{id}` | Get a board game by ID |
| PUT | `/api/games/{id}` | Update a board game |
| DELETE | `/api/games/{id}` | Delete a board game |
| GET | `/api/stores/` | List all stores |
| POST | `/api/stores/` | Create a new store |
| GET | `/api/stores/{id}` | Get a store by ID |
| PUT | `/api/stores/{id}` | Update a store |
| DELETE | `/api/stores/{id}` | Delete a store |

