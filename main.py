from fastapi import FastAPI
from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import sqlite3 as sql

router = APIRouter()

class Customers(BaseModel):
    company: str = None
    address: str = None
    city: str = None
    state: str = None
    country: str = None
    postalcode: str = None
    fax: str = None

class Albums(BaseModel):
    title: str
    artist_id: int

@router.on_event("startup")
async def startup():
    router.db_connection = sql.connect("chinook.db")

@router.on_event("shutdown")
async def shutdown():
    router.db_connection.close()

@router.get("/tracks")
async def tracks(page: int = 0, per_page: int = 10):
    router.db_connection.row_factory = sql.Row
    return router.db_connection.execute(
        "SELECT * FROM tracks ORDER BY TrackId LIMIT :per_page OFFSET :offset",
        {'per_page': per_page, 'offset': page*per_page}).fetchall()

@router.get("/tracks/composers")
async def composers(response: Response, composer_name: str):
    router.db_connection.row_factory = lambda cursor, x: x[0]
    if len(router.db_connection.execute(
        "SELECT Name FROM tracks WHERE Composer = :composer ORDER By name",
        {'composer': composer_name}).fetchall()) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail":{"error":"No tracks for composer"}}
    return router.db_connection.execute(
        "SELECT Name FROM tracks WHERE Composer = :composer ORDER By name",
        {'composer': composer_name}).fetchall()

@router.post("/albums")
async def album_add(response: Response, album: Albums):
    router.db_connection.row_factory = lambda cursor, x: x[0]
    artist = router.db_connection.execute(
        "SELECT Artistid FROM artists WHERE Artistid = :id",
        {'id': album.artist_id}).fetchall()
    if not artist:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail":{"error":"No Artist with id"}}
    data = router.db_connection.execute(
        "INSERT INTO albums (Title, Artistid) VALUES (:Title, :id)",
        {'Title': album.title, 'id': album.artist_id})
    router.db_connection.commit()
    new_album_id = data.lastrowid
    router.db_connection.row_factory = sql.Row
    album = router.db_connection.execute(
        "SELECT albumid, title, artistid FROM albums WHERE albumid = :id;",
        {'id': new_album_id }).fetchone()
    response.status_code = status.HTTP_201_CREATED
    return album

@router.get("/albums/{album_id}")
async def tracks_composers(response: Response, album_id: int):
	router.db_connection.row_factory = sql.Row
	album = router.db_connection.execute("SELECT * FROM albums WHERE AlbumId = ?",
		(album_id, )).fetchone()
	return album

app = FastAPI()
app.include_router(router, tags=['endpoint zad4'])
