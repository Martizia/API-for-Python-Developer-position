This project is a FastAPI-based application that manages comments for posts. It uses a PostgreSQL database to store the data.

Prerequisites
Before you begin, ensure you have the following installed:

- Python 3.7 or higher

- Poetry (for dependency management)

- PostgreSQL

## Installation

### 1. Install Dependencies

First, clone the repository to your local machine:

```sh
git clone https://github.com/Martizia/API-for-Python-Developer-position
cd your-repo
```

Next, install the project dependencies using Poetry:

```sh
poetry install
```

### 2. Set Up the Database

Ensure you have PostgreSQL installed and running. Create a new database for this project.

### 3. Configure Environment Variables

Copy the .env.example file to a new file named .env:

```sh
cp .env.example .env
```

Edit the .env file and fill in the necessary environment variables, such as the database URL, secret key, etc.

### 4. Run the Application

Once everything is set up, you can run the application using the following command:

```sh
poetry run python main.py
```

The application should now be running on http://127.0.0.1:8000. You can access the API documentation at http://127.0.0.1:8000/docs.
