import requests
from fastapi import APIRouter, Request, status, Depends, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.routing import Route, Mount
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from datetime import timedelta
from .core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

from .crud.crud_user import crud_user
from .crud.crud_dokter import crud_dokter
from .dependencies import check_for_login, get_db_session

router = APIRouter()

templates = Jinja2Templates(directory="app/templates/")

@router.get('/')
def redirecting():
  return RedirectResponse(url='/login')

@router.get('/login', response_class=HTMLResponse, name='login')
async def login(request: Request):
  return templates.TemplateResponse('pages/login.html', {'request':request})

@router.post("/login", dependencies=[], name='token')
async def login_for_access_token(db: Session = Depends(get_db_session), form_data: OAuth2PasswordRequestForm = Depends()):
  user = crud_user.authenticate(db=db, username=form_data.username, password=form_data.password)
  if not user:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Incorrect username or password",
          headers={"WWW-Authenticate": "Bearer"},
      )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = await create_access_token(
      data={"sub": user.username}, expires_delta=access_token_expires
  )
  response = RedirectResponse('/antrian', status_code=status.HTTP_302_FOUND)
  response.set_cookie(key="access_token", value=access_token)
  return response

@router.get('/logout', name='logout')
async def logout():
  response = RedirectResponse('/login')
  response.delete_cookie(key="access_token")
  return response

@router.get('/antrian', response_class=HTMLResponse, name='antrian', dependencies=[Depends(crud_user.get_current_user_login)])
async def dashboard(request: Request):
  antrian_atas = [
    {
      "nama_poli": "Poli Umum",
      "color": "info"
    },
    {
      "nama_poli": "Poli Gigi",
      "color": "success"
    },
    {
      "nama_poli": "Poli Kandungan",
      "color": "warning"
    },
  ]
  antrian_bawah = [
    {
      "nama_poli": "Poli Anak",
      "color": "danger"
    },
    {
      "nama_poli": "Poli Penyakit Dalam",
      "color": "purple"
    },
  ]
  return templates.TemplateResponse(
    'pages/antrian.html', {
      "request": request,
      "antrian_atas": antrian_atas,
      "antrian_bawah":antrian_bawah,
      "antrian_sidebar_link_active": 'active'
    })

@router.get('/admin/dokter', response_class=HTMLResponse, name='dokter', dependencies=[Depends(crud_user.get_current_user_login)])
def dokter(request: Request, access_token: str = Cookie(None)):
  print('dokter', access_token)
  response = requests.get(url="http://localhost:8000/api/v1/dokter", headers={
    "Authorization": f"Bearer {access_token}"
  })
  dokter = response.json()
  print(dokter)
  return templates.TemplateResponse(
    'pages/admin/user.html', {
      "request":request,
      "nama": "Dokter",
      "dokter_sidebar_link_active": "active",
      "user_menu_open": "menu-open",
      "dokter_list": dokter
    })

@router.get('/admin/pasien', response_class=HTMLResponse, name='pasien', dependencies=[Depends(crud_user.get_current_user_login)])
def dokter(request: Request, access_token: str = Cookie(None)):
  response = requests.get(url="http://localhost:8000/api/v1/pasien", headers={
    "Authorization": f"Bearer {access_token}"
  })
  pasien = response.json()
  return templates.TemplateResponse(
    'pages/admin/pasien.html', {
      "request":request,
      "nama": "Pasien",
      "pasien_sidebar_link_active": "active",
      "user_menu_open": "menu-open",
      "pasien_list": pasien
    })

@router.get('/rekam-medis', response_class=HTMLResponse, name='rekam-medis', dependencies=[Depends(crud_user.get_current_user_login)])
def rekam_medis(request: Request):
  return templates.TemplateResponse(
    'pages/rekam-medis.html', {
      "request": request,
      "rekam_sidebar_link_active": "active",
    }
  )

@router.get('/404-not-found', name='404-not-found')
def redirect_404_not_found(request: Request):
  return templates.TemplateResponse('pages/404.html', {'request': request})

@router.get('/401-not-found', name='401-unauthorized')
def redirect_401_not_found(request: Request):
  return templates.TemplateResponse('pages/401.html', {'request': request})