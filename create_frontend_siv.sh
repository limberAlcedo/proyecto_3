#!/bin/bash

# ------------------------------
# VARIABLES
# ------------------------------
FRONTEND_NAME="frontend_siv"
BACKEND_NAME="backend_siv"
PYTHON_ENV=".venv"
FASTAPI_PORT=8000
REACT_PORT=5173

# ------------------------------
# BACKEND - FastAPI + MySQL
# ------------------------------
echo "🚀 Creando backend FastAPI..."
mkdir $BACKEND_NAME
cd $BACKEND_NAME || exit

python3 -m venv $PYTHON_ENV
source $PYTHON_ENV/bin/activate

pip install fastapi uvicorn sqlalchemy pymysql pydantic passlib[bcrypt] python-jose python-multipart python-dotenv

mkdir app
cd app || exit
mkdir routers

# database.py
cat <<EOL > database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
EOL

# models.py
cat <<EOL > models.py
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="user")
EOL

# schemas.py
cat <<EOL > schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str = "user"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        orm_mode = True
EOL

# crud.py
cat <<EOL > crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
EOL

# auth.py
cat <<EOL > auth.py
from passlib.context import CryptContext
from jose import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
EOL

# routers/auth_router.py
cat <<EOL > routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, auth
from app.database import SessionLocal

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    token = auth.create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "role": user.role}
EOL

# routers/user_router.py
cat <<EOL > routers/user_router.py
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

user_router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

@user_router.post("/")
def create_user(user: schemas.UserCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos")
    return crud.create_user(db, user)
EOL

# main.py
cat <<EOL > main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_router, user_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["http://localhost:$REACT_PORT"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth_router.auth_router)
app.include_router(user_router.user_router)

@app.get("/")
def root():
    return {"message": "API funcionando"}
EOL

cd ../..  # volver al root

echo "✅ Backend con MySQL listo. Para correr:"
echo "source $BACKEND_NAME/$PYTHON_ENV/bin/activate && uvicorn app.main:app --reload"

# ------------------------------
# FRONTEND - React + Bootstrap
# ------------------------------
echo "🚀 Creando frontend React..."
npm create vite@latest $FRONTEND_NAME -- --template react
cd $FRONTEND_NAME || exit
npm install react-router-dom bootstrap

mkdir -p src/api src/components src/pages src/layout

# src/index.css
cat <<EOL > src/index.css
@import "bootstrap/dist/css/bootstrap.min.css";

body {
  background-color: #f8f9fa;
  font-family: Arial, sans-serif;
}
EOL

# src/api/auth.js
cat <<EOL > src/api/auth.js
const API_URL = "http://127.0.0.1:$FASTAPI_PORT";

export const loginUser = async (credentials) => {
  const res = await fetch(\`\${API_URL}/auth/login\`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });
  if (!res.ok) throw new Error("Usuario o contraseña incorrectos");
  return res.json();
};

export const registerUser = async (user, token) => {
  const res = await fetch(\`\${API_URL}/users/\`, {
    method: "POST",
    headers: { 
      "Content-Type": "application/json",
      "Authorization": \`Bearer \${token}\`
    },
    body: JSON.stringify(user),
  });
  if (!res.ok) throw new Error("No se pudo crear el usuario");
  return res.json();
};
EOL

# src/components/ProtectedRoute.jsx
cat <<EOL > src/components/ProtectedRoute.jsx
import { Navigate } from "react-router-dom";

export default function ProtectedRoute({ children }) {
  const token = localStorage.getItem("token");
  if (!token) return <Navigate to="/" />;
  return children;
}
EOL

# src/layout/Navbar.jsx
cat <<EOL > src/layout/Navbar.jsx
import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const role = localStorage.getItem("role");

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/");
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light px-4">
      <Link className="navbar-brand" to="/dashboard">Dashboard</Link>
      <div className="collapse navbar-collapse">
        <ul className="navbar-nav mr-auto">
          {role === "admin" && (
            <li className="nav-item">
              <Link className="nav-link" to="/register">Registrar Usuario</Link>
            </li>
          )}
        </ul>
        <button className="btn btn-danger" onClick={handleLogout}>Logout</button>
      </div>
    </nav>
  );
}
EOL

# src/pages/Login.jsx
cat <<EOL > src/pages/Login.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginUser } from "../api/auth";

export default function Login() {
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => setForm({...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await loginUser(form);
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("role", data.role);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="card p-4 shadow" style={{width:"350px"}}>
        <h3 className="text-center mb-4">Iniciar Sesión</h3>
        {error && <div className="alert alert-danger">{error}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <input type="email" name="email" placeholder="Email" className="form-control" value={form.email} onChange={handleChange} required />
          </div>
          <div className="mb-3">
            <input type="password" name="password" placeholder="Contraseña" className="form-control" value={form.password} onChange={handleChange} required />
          </div>
          <button type="submit" className="btn btn-primary w-100">Ingresar</button>
        </form>
      </div>
    </div>
  );
}
EOL

# src/pages/RegisterUser.jsx
cat <<EOL > src/pages/RegisterUser.jsx
import { useState } from "react";
import { registerUser } from "../api/auth";

export default function RegisterUser() {
  const [form, setForm] = useState({ email:"", password:"", role:"user" });
  const [message, setMessage] = useState("");
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  if(role !== "admin") return <p className="text-center mt-5 text-danger">No tienes permisos para registrar usuarios</p>;

  const handleChange = (e) => setForm({...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await registerUser(form, token);
      setMessage("Usuario creado correctamente");
      setForm({ email:"", password:"", role:"user" });
    } catch (err) {
      setMessage(err.message);
    }
  };

  return (
    <div className="d-flex justify-content-center mt-5">
      <div className="card p-4 shadow" style={{width:"400px"}}>
        <h3 className="text-center mb-4">Registrar Usuario</h3>
        {message && <div className="alert alert-info">{message}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <input type="email" name="email" placeholder="Email" className="form-control" value={form.email} onChange={handleChange} required />
          </div>
          <div className="mb-3">
            <input type="password" name="password" placeholder="Contraseña" className="form-control" value={form.password} onChange={handleChange} required />
          </div>
          <div className="mb-3">
            <select name="role" className="form-select" value={form.role} onChange={handleChange}>
              <option value="user">Usuario</option>
              <option value="admin">Administrador</option>
            </select>
          </div>
          <button type="submit" className="btn btn-success w-100">Crear Usuario</button>
        </form>
      </div>
    </div>
  );
}
EOL

# src/App.jsx
cat <<EOL > src/App.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import RegisterUser from "./pages/RegisterUser";
import ProtectedRoute from "./components/ProtectedRoute";
import Navbar from "./layout/Navbar";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<ProtectedRoute><RegisterUser /></ProtectedRoute>} />
        <Route path="/register" element={<ProtectedRoute><RegisterUser /></ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
EOL

# src/main.jsx
cat <<EOL > src/main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
EOL

npm install

echo "✅ Full Stack con React + Bootstrap listo!"
echo "Para correr backend: source $BACKEND_NAME/$PYTHON_ENV/bin/activate && uvicorn app.main:app --reload"
echo "Para correr frontend: cd $FRONTEND_NAME && npm run dev"
