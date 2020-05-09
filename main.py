from fastapi import FastAPI
import sqlite3 as sql
from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()
router = APIRouter()

@router.on_event("startup")
async def startup():
    router.db_connection = sql.connect("chinook.db")

@router.on_event("shutdown")
async def shutdown():
    router.db_connection.close()

@router.get("/tracks")
async def tracks(page: int = 0, per_page: int = 10):
    router.db_connection.row_factory = sql.Row
    tracks = router.db_connection.execute(
        "SELECT * FROM tracks ORDER BY TrackId LIMIT :per_page OFFSET :offset",
        {'per_page': per_page, 'offset': page*per_page}).fetchall()
    return tracks
