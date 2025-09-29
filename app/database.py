import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 🔹 Lee la URL desde la variable de entorno (Render la inyecta automáticamente)
DATABASE_URL = os.getenv("DATABASE_URL")

# 🔹 Crea el motor de conexión
engine = create_engine(DATABASE_URL)

# 🔹 Configuración de la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 Base para los modelos
Base = declarative_base()

# 🔹 Dependencia para obtener la sesión en los endpoints de FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

