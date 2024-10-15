
# Soccer Simulation Backend

## Overview

This repository contains the backend logic for a soccer simulation game. The backend is built using Python with FastAPI and includes logic to generate soccer players, teams, and other relevant simulations. The game simulates various soccer-related scenarios by generating player statistics, handling team formations, and offering an API for external interaction.

---

## Features

- **Team Generator**: Automatically generates a soccer team with different positions such as goalkeepers, defenders, midfielders, strikers, and wingers.
- **Position-Specific Logic**: Each position in the team has specific stat configurations to reflect real-life soccer skills.
- **Player Stats**: Each player is generated with unique stats such as Physical Power, Finishing, Tackling, and more.
- **API Endpoints**: Provides endpoints to retrieve generated teams or individual player data.

---

## Technologies

- Python
- FastAPI
- Pydantic (for models)
- Uvicorn (as ASGI server)

---

## Installation

### macOS

1. Clone the repository:

    ```bash
    git clone https://github.com/SoccerSimulator/Soccer-Simulation-BE.git
    cd Soccer-Simulation-BE
    ```

2. Install [Pipenv](https://pipenv.pypa.io/en/latest/) if you haven't already:

    ```bash
    brew install pipenv
    ```

3. Install dependencies:

    ```bash
    pipenv install
    ```

4. Activate the environment:

    ```bash
    pipenv shell
    ```

### Ubuntu

1. Clone the repository:

    ```bash
    git clone https://github.com/SoccerSimulator/Soccer-Simulation-BE.git
    cd Soccer-Simulation-BE
    ```

2. Install [Pipenv](https://pipenv.pypa.io/en/latest/):

    ```bash
    sudo apt install pipenv
    ```

3. Install dependencies:

    ```bash
    pipenv install
    ```

4. Activate the environment:

    ```bash
    pipenv shell
    ```

### Windows

1. Clone the repository:

    ```bash
    git clone https://github.com/SoccerSimulator/Soccer-Simulation-BE.git
    cd Soccer-Simulation-BE
    ```

2. Install [Pipenv](https://pipenv.pypa.io/en/latest/):

    ```bash
    pip install pipenv
    ```

3. Install dependencies:

    ```bash
    pipenv install
    ```

4. Activate the environment:

    ```bash
    pipenv shell
    ```

---

## Running the Application

To run the server, use the following command:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

---

## API Endpoints

- **GET** `/team`: Generates a team and returns it as JSON.
- **GET** `/team/player/{player_id}`: Returns information for a specific player by their ID.

---

## English - Hebrew positions translation

```txt
שוער -  goalkeeper
בלם - defenders
מגנים -  full backs
קשרים -  Midfielder
חלוצים - Striker
וינגר - Wingers
```
