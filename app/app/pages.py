import requests
import json
from fastapi import APIRouter, Request, status, Depends, HTTPException, Response, Cookie, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.routing import Route, Mount
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from datetime import timedelta
from .core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, verify_password

from .models.rfid_temporary import RFIDTemporary
from .schemas.user import UserRetrieve
from .crud.crud_user import crud_user
from .crud.crud_dokter import crud_dokter
from .crud.crud_pasien import crud_pasien
from .crud.crud_antrian import crud_antrian
from .dependencies import check_for_login, get_db_session

router = APIRouter()

templates = Jinja2Templates(directory="app/templates/")

@router.get('/')
def redirecting():
  return RedirectResponse(url='/login')

@router.get('/login', response_class=HTMLResponse, name='login')
async def login(request: Request, error: str = Cookie(None)):
  context = {
    'request':request
  }
  if error is not None:
    context.update({"error": error})
  response = templates.TemplateResponse('pages/login.html', context)
  response.delete_cookie('error')
  return response

@router.post("/login", dependencies=[], name='token')
async def login_for_access_token(db: Session = Depends(get_db_session), form_data: OAuth2PasswordRequestForm = Depends()):
  user = crud_user.get_by_username(db, username=form_data.username)
  response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
  if not user:
    response.set_cookie(key="error", value="Username salah")
    return response
  if not verify_password(form_data.password, user.password):
    response.set_cookie(key="error", value="Password salah.")
    return response
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

@router.get('/antrian', response_class=HTMLResponse, name='antrian',)
def dashboard(request: Request, user: UserRetrieve = Depends(crud_user.get_current_user_login), access_token: str = Cookie(None)):
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
  antrian = requests.get('http://localhost:8000/api/v1/antrian',
    headers={
      "Authorization": f"Bearer {access_token}"
    },
    # params={"nama_poli": "Poli Kandungan"}
  )
  antrian = antrian.json()
  return templates.TemplateResponse(
    'pages/antrian.html', {
      "request": request,
      "antrian_atas": antrian_atas,
      "antrian_bawah":antrian_bawah,
      "antrian_sidebar_link_active": 'active',
      "user": user,
      "antrian_list": antrian,
    })

@router.get('/admin/dokter', response_class=HTMLResponse, name='dokter')
def dokter(request: Request, access_token: str = Cookie(None),  user: UserRetrieve = Depends(crud_user.get_current_user_login)):
  print('dokter', access_token)
  response = requests.get(url="http://localhost:8000/api/v1/dokter", headers={
    "Authorization": f"Bearer {access_token}"
  })
  dokter = response.json()
  return templates.TemplateResponse(
    'pages/admin/user.html', {
      "request":request,
      "nama": "Dokter",
      "dokter_sidebar_link_active": "active",
      "user_menu_open": "menu-open",
      "dokter_list": dokter,
      "user": user,
    })

@router.post('/admin/dokter', name='pasien-create', dependencies=[Depends(crud_user.get_current_user_login)])
def dokter_create(
  username: str = Form(...),
  password: str = Form(...),
  nama: str = Form(...),
  alamat: str = Form(...),
  no_hp: str = Form(...),
  tempat_lahir: str = Form(...),
  tanggal_lahir: str = Form(...),
  poli: str = Form(...),
  access_token: str = Cookie(None),
  db: Session = Depends(get_db_session),
):
  body= {
    'username': username,
    'password': password,
    'nama': nama,
    'alamat': alamat,
    'no_hp': no_hp,
    'tempat_lahir': tempat_lahir,
    'tanggal_lahir': tanggal_lahir,
    'poli': poli,
  }
  requests.post('http://localhost:8000/api/v1/dokter', headers={
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
  }, json=body)
  return RedirectResponse('/admin/dokter', status_code=status.HTTP_302_FOUND)

@router.get('/admin/pasien', response_class=HTMLResponse, name='pasien')
def pasien(request: Request, access_token: str = Cookie(None),  user: UserRetrieve = Depends(crud_user.get_current_user_login), db: Session = Depends(get_db_session)):
  response = requests.get(url="http://localhost:8000/api/v1/pasien", headers={
    "Authorization": f"Bearer {access_token}"
  })
  pasien = response.json()
  rfid = db.query(RFIDTemporary).filter_by(id=1).first()
  return templates.TemplateResponse(
    'pages/admin/pasien.html', {
      "request":request,
      "nama": "Pasien",
      "pasien_sidebar_link_active": "active",
      "user_menu_open": "menu-open",
      "pasien_list": pasien,
      "user": user,
      "rfid": rfid,
    })

@router.post('/admin/pasien', name="pasien-create")
def pasien_create(
  nama: str = Form(...),
  alamat: str = Form(...),
  no_hp: str = Form(...),
  tempat_lahir: str = Form(...),
  tanggal_lahir: str = Form(...),
  rfid: str = Form(...),
  bpjs: bool = Form(...),
  db: Session = Depends(get_db_session),
  access_token: str = Cookie(None)
):
  print(bpjs)
  print(tanggal_lahir)
  body= {
    'nama': nama,
    'alamat': alamat,
    'no_hp': no_hp,
    'tempat_lahir': tempat_lahir,
    'tanggal_lahir': tanggal_lahir,
    'rfid': rfid,
    'bpjs': bpjs
  }
  response = requests.post('http://localhost:8000/api/v1/pasien', headers={
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
  }, json=body)
  if response.status_code == 201:
    rfid_obj = db.query(RFIDTemporary).filter(RFIDTemporary.id == 1).first()
    rfid_obj.aktif = False
    db.add(rfid_obj)
    db.commit()
  return RedirectResponse('/admin/pasien', status_code=status.HTTP_302_FOUND)

@router.get('/rekam-medis/{pasien_id}', response_class=HTMLResponse, name='rekam-medis')
def rekam_medis(request: Request, pasien_id: int, db: Session = Depends(get_db_session), access_token: str = Cookie(None), user: UserRetrieve = Depends(crud_user.get_current_user_login)):
  response = requests.get(url=f"http://localhost:8000/api/v1/rekam-medis/{pasien_id}", headers={
    "Authorization": f"Bearer {access_token}"
  })
  rekam_medis = response.json()
  pasien = crud_pasien.get(id=pasien_id, db=db)
  print(rekam_medis)
  print(pasien)
  return templates.TemplateResponse(
    'pages/rekam-medis.html', {
      "request": request,
      "rekam_sidebar_link_active": "active",
      "user": user,
      "rekam_medis": rekam_medis,
      "pasien_id": pasien_id,
      "pasien": pasien
    }
  )

@router.post('/rekam-medis/{pasien_id}', name='rekam-medis-create')
def rekam_medis_create(
  pasien_id: int,
  keluhan: str = Form(...),
  user: UserRetrieve = Depends(crud_user.get_current_user_login),
  access_token: str = Cookie(None),
):
  print(user.dokter)
  body= {
    'pasien_id': pasien_id,
    'dokter_id': user.dokter[0].id,
    'keluhan': keluhan
  }
  requests.post('http://localhost:8000/api/v1/rekam-medis', headers={
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
  }, json=body)
  return RedirectResponse(f'/rekam-medis/{pasien_id}', status_code=status.HTTP_302_FOUND)

@router.get('/daftar-periksa', name='daftar-periksa')
def daftar_periksa(request: Request, access: str = Cookie(None), user: UserRetrieve = Depends(crud_user.get_current_user_login), db: Session= Depends(get_db_session)):
  antrian_list = crud_antrian.get_by_antrian_aktif_per_poli(db=db, poli=user.dokter[0].poli)
  print(antrian_list)
  context = {
    'daftar_periksa_sidebar_link_active': 'active',
    'nama': 'Periksa',
    'request': request,
    'user': user,
    'antrian_list': antrian_list
  }
  return templates.TemplateResponse('pages/daftar-periksa.html', context)

@router.get('/404-not-found', name='404-not-found')
def redirect_404_not_found(request: Request):
  return templates.TemplateResponse('pages/404.html', {'request': request})

@router.get('/401-not-found', name='401-unauthorized')
def redirect_401_not_found(request: Request):
  return templates.TemplateResponse('pages/401.html', {'request': request})