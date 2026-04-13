# board-game-management

A website that manages the current board game stock for each store for user to lends or buy the board games.
Extra information in the project [wiki](https://github.com/PeanutPK/board-game-management/wiki)

## Installation

### Backend

1. Create virtual environment

    ```bash
    python3 -m venv .venv
    ```

2. Copy environment file and configure the variable inside

    ```bash
    cp example.env .env
    ```

3. Activate virtual environment

    - MacOS/Linux

        ```bash
        source .venv/bin/activate
        ```

    - Windows

        ```bash
        .venv/Scripts/activate
        ```

4. Download required dependencies

    ```bash
    pip install -r requirements.txt
    ```

5. Run the app
    The backend will automatically create the database file (board_games.db).

    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

6. (Optional) Initialize database

    ```bash
    python3 initial_database
    ```

    After running the python file the terminal will show a question about initializing the default format data.

    Press 'y' or 'enter' to confirm a default information.

    The information is provided with the admin and staff user account and the board game data. If user choose not to use default admin and staff setting the app will prompt with the admin and staff form to create them.

### Frontend

1. Install dependencies

    ```bash
    npm i
    ```

2. Copy environment file and configure the variable inside

    ```bash
    cp example.env .env
    ```

3. Run app

    ```bash
    npm run dev
    ```

## Linting

### Frontend Lint

Make sure to set directory at `/frontend`

```bash
npm run lint            # linting
npm run lint:eslint     # auto fix using eslint
```

### Backend Lint

Make sure to set directory at `/backend`

```bash
black                   # run black formatter
```
