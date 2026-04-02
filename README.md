# board-game-management

A website that manages the current board game stock for each store for user to lends or buy the board games.
Extra information in the project [wiki](https://github.com/PeanutPK/board-game-management/wiki)

## Installation

### Backend

1. Create virtual environment

    ```bash
    python3 -m venv .venv
    ```

2. Activate virtual environment

    - MacOS/Linux

      ```bash
      source .venv/bin/activate
      ```

    - Windows

      ```bash
      .venv/Scripts/activate
      ```

3. Download required dependencies

    ```bash
    pip install -r requirements.txt
    ```

4. Copy environment file and configure the variable inside

    ```bash
    cp example.env .env
    ```

5. Run the app

    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

### Frontend

1. Install dependencies

    ```bash
    npm i
    ```

2. Run app

    ```bash
    npm run dev
    ```
