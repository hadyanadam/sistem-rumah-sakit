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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AdminRouter)
app.include_router(DokterRouter)
app.include_router(PasienRouter)
app.include_router(RekamMedisRouter)
app.include_router(AntrianRouter)
app.include_router(PagesRouter, include_in_schema=False,default_response_class=HTMLResponse)