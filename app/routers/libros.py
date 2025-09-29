from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth

router = APIRouter(prefix="/libros", tags=["Libros"])

@router.post("/", response_model=schemas.Libro)
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(database.get_db), user: dict = Depends(auth.get_current_user)):
    nuevo_libro = models.Libro(**libro.dict())
    db.add(nuevo_libro)
    db.commit()
    db.refresh(nuevo_libro)
    return nuevo_libro

@router.get("/", response_model=list[schemas.Libro])
def listar_libros(db: Session = Depends(database.get_db)):
    return db.query(models.Libro).all()

@router.get("/{libro_id}", response_model=schemas.Libro)
def obtener_libro(libro_id: int, db: Session = Depends(database.get_db)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.put("/{libro_id}", response_model=schemas.Libro)
def actualizar_libro(libro_id: int, datos: schemas.LibroCreate, db: Session = Depends(database.get_db), user: dict = Depends(auth.get_current_user)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    for key, value in datos.dict().items():
        setattr(libro, key, value)
    db.commit()
    db.refresh(libro)
    return libro

@router.delete("/{libro_id}")
def eliminar_libro(libro_id: int, db: Session = Depends(database.get_db), user: dict = Depends(auth.get_current_user)):
    libro = db.query(models.Libro).filter(models.Libro.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    db.delete(libro)
    db.commit()
    return {"msg": "Libro eliminado"}
