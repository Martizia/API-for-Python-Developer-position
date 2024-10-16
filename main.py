import os
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from src.database.db import get_db
from src.config.config import config
from src.routes import auth, users, posts, comments, analytics

import uvicorn

app = FastAPI()


app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(posts.router, prefix="/api")
app.include_router(comments.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    This function checks the health of the database connection by executing a test query.

    :param db: An async database connection.
    :type db: AsyncSession
    :return: A dictionary with a message indicating the health status of the database connection.
    :raises HTTPException 500: If there is an error connecting to the database or the database is not configured correctly.

    """
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
