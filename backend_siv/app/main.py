# backend_siv/app/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .database import SessionLocal, engine
from passlib.context import CryptContext

# ---------------------------
# Inicializar DB
# ---------------------------
models.Base.metadata.create_all(bind=engine)

# ---------------------------
# Configuración CORS
# ---------------------------
origins = ["http://localhost:5179"]
app = FastAPI(title="Backend SIV", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Dependencia DB
# ---------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------------
# Password hashing
# ---------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str):
    return pwd_context.hash(password)
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ---------------------------
# Rutas
# ---------------------------
@app.get("/")
def root():
    return {"message": "Backend SIV funcionando ✅"}

@app.post("/auth/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    return crud.create_user(db, user, hash_password(user.password))

@app.post("/auth/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    return {"message": f"Bienvenido {db_user.username}!"}
