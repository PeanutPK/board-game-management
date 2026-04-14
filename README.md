# board-game-management

A website that manages the current board game stock for each store for user to lends or buy the board games.
Extra information in the project [wiki](https://github.com/PeanutPK/board-game-management/wiki)

## Table of Content

- [board-game-management](#board-game-management)
  - [Table of Content](#table-of-content)
  - [System Architecture Overview](#system-architecture-overview)
  - [User Roles \& Permissions](#user-roles--permissions)
  - [Technology Stack](#technology-stack)
    - [Frontend (TypeScript)](#frontend-typescript)
    - [Backend (Python)](#backend-python)
  - [Installation](#installation)
    - [Backend](#backend)
    - [Frontend](#frontend)
  - [Linting](#linting)
    - [Frontend Lint](#frontend-lint)
    - [Backend Lint](#backend-lint)
  - [Screenshots of Your System](#screenshots-of-your-system)

## System Architecture Overview

## User Roles & Permissions

## Technology Stack

### Frontend (TypeScript)

- Frameworks
  - Vue.js
- Styling
  - Iconify (icons)
  - Tailwindcss (for inline and tweaking some style)
  - css (detail styling, more customizable)

### Backend (Python)

- Frameworks & Dependencies
  - FastAPI             # API framework
  - Uvicorn             # ASGI server application
  - Black               # formatting
  - mypy                # type checking
  - bcrypt              # encrypt data
  - sqlalchemy          # SQL toolkit for python
  - pydantic            # data validation
  - python-jose         # JWT

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
    python init_db.py
    # or
    python3 init_db.py
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
npm run lint:oxlint     # auto fix using oxlint
```

### Backend Lint

Make sure to set directory at `/backend`

```bash
black --check .         # check using black formatter
black .                 # run black formatter
```

## Screenshots of Your System

| Page                                     | Screenshot                                       |
| ---------------------------------------- | ------------------------------------------------ |
| Admin Page (Admin Permission)            | ![admin page](images/admin/page.png)             |
| Admin Edit User Modal                    | ![admin edit](images/admin/edit.png)             |
| Admin Add User Modal                     | ![admin add](images/admin/add.png)               |
| Management Page (Staff/Admin Permission) | ![management page](images/manage/page.png)       |
| Management Add Game Modal                | ![mangement add](images/manage/add.png)          |
| Management Edit Game Modal               | ![management edit](images/manage/edit.png)       |
| Game List Page (Carousel)                | ![game page](images/game/list/carousel.png)      |
| Game List Page (List)                    | ![game list](images/game/list/list.png)          |
| Game Detail Page (Description)           | ![game detail page](images/game/detail/page.png) |
| Game Detail Page (Review)                | ![game review](images/game/detail/review.png)    |
| Login Page                               | ![login page](images/auth/login.png)             |
| Signup Page                              | ![signup page](images/auth/signup.png)           |
| Dashboard Page                           | ![dashboard page](images/dashboard/page.png)     |
| Status Page                              | ![status page](images/status/page.png)           |
| Policy Page                              | ![policy page](images/policy/page.png)           |
| Contact Page                             | ![contact page](images/contact/page.png)         |
| Home Page                                | ![home](images/home.png)                         |
