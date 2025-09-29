from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database
from .routers import libros, chat, users

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Venta de Libros con IA")

# 👉 Aquí agregamos el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes poner ["http://127.0.0.1:5500"] si usas Live Server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(users.router)
app.include_router(libros.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "API de Venta de Libros con IA funcionando 🚀"}
