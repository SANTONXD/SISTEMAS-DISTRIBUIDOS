from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database, models
from ..auth import get_current_user
from pydantic import BaseModel
from openai import OpenAI

router = APIRouter(prefix="/chat", tags=["Chat IA"])

client = OpenAI(
base_url="https://openrouter.ai/api/v1",
api_key="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",
)

class ChatRequest(BaseModel):
    titulo: str

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def chat_libros(body: ChatRequest,
                user: dict = Depends(get_current_user),
                db: Session = Depends(get_db)):

    # Buscar el libro en la BD
    libro = db.query(models.Libro).filter(models.Libro.titulo == body.titulo).first()
    if not libro:
        return {"respuesta": f"No encontré el libro '{body.titulo}' en la base de datos."}

    # Pasar a la IA el contexto del libro
    completion = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en literatura."},
            {"role": "user", "content": f"Por favor, dame un resumen y opinión del libro '{libro.titulo}'"}
        ]
    )
    return {"respuesta": completion.choices[0].message.content}
