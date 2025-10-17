# backend_siv/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ---------------------------
# URL de conexión a MySQL
# ---------------------------
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:A.Alcedo2705@localhost/siv_db"

# ---------------------------
# Motor de SQLAlchemy
# ---------------------------
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # muestra todas las consultas SQL
    future=True
)

# ---------------------------
# Sesiones
# ---------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ---------------------------
# Base de modelos
# ---------------------------
Base = declarative_base()

# ---------------------------
# Función para crear las tablas
# ---------------------------
def init_db():
    from . import models  # importación relativa
    Base.metadata.create_all(bind=engine)
