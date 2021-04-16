from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from app.routers.admin import router as AdminRouter
from app.routers.dokter_router import router as DokterRouter
from app.routers.pasien_router import router as PasienRouter
from app.routers.rekam_medis_router import router as RekamMedisRouter
from app.routers.antrian_router import router as AntrianRouter
from app.pages import router as PagesRouter
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.seeder import (
    seed_pasien,
    seed_rekam_medis,
    seed_dokter,
    seed_antrian,
)

app = FastAPI()

app.mount('/static', StaticFiles(directory="app/static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:3000",
]

@app.on_event("startup")
def init_data():
    db = SessionLocal()
    init_db(db)
    # seed_dokter(iter=10, db=db)
    # seed_pasien(iter=10, db=db)
    # seed_antrian(iter=5, db=db, range_pasien_id=[1, 10])
    # seed_rekam_medis(iter=50, db=db, range_pasien_id=[2,11], range_dokter_id=[1,10])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AdminRouter, tags=['User'])
app.include_router(DokterRouter, tags=['Dokter'])
app.include_router(PasienRouter, tags=['Pasien'])
app.include_router(RekamMedisRouter, tags=['RekamMedis'])
app.include_router(AntrianRouter, tags=['Antrian'])
app.include_router(PagesRouter, include_in_schema=False,default_response_class=HTMLResponse)