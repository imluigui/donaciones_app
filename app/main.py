from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from .database import create_db_and_tables, get_session
from .models import Usuario
from .schemas import DonanteCreate, Token
from .auth import get_password_hash, verify_password, create_access_token
from datetime import timedelta

app = FastAPI(title="Sistema de Gestión de Donaciones")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Gestión de Donaciones"}

@app.post("/register/")
def register_donante(donante: DonanteCreate, session: Session = Depends(get_session)):
    statement = select(Usuario).where(Usuario.email == donante.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    hashed_password = get_password_hash(donante.password)
    nuevo_usuario = Usuario(
        email=donante.email,
        nombre=donante.nombre,
        hashed_password=hashed_password
    )
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    return {"message": "Usuario registrado exitosamente", "id": nuevo_usuario.id}

@app.post("/login/", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    statement = select(Usuario).where(Usuario.email == form_data.username)
    user = session.exec(statement).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
# Trigger
