from typing import Union
from fastapi import Security, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from .db.session import SessionLocal

async def get_db_session():
  session = SessionLocal()
  try:
      yield session
  finally:
      session.close()

def check_for_login(request: Request):
    try:
        if request.state.access_token is None:
            return RedirectResponse('/401-unauthorized')
    except AttributeError:
        return RedirectResponse('/401-unauthorized')