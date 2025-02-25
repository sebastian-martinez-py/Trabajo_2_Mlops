from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid

app = FastAPI(
    title="API de Usuarios",
    description="API para gestionar usuarios",
    version="1.0.0"
)

usuarios = []  # Lista para almacenar usuarios temporalmente

# Modelo de datos para el usuario
class Usuario(BaseModel):
    nombre: str
    correo: str
    username: str

# Endpoint POST para agregar un usuario
@app.post("/usuarios/", tags=["Usuarios"], status_code=status.HTTP_201_CREATED)
async def agregar_usuario(data: Usuario):
    usuario = {
        "id": str(uuid.uuid4()),
        "nombre": data.nombre,
        "correo": data.correo,
        "username": data.username
    }
    usuarios.append(usuario)
    return {
        "mensaje": f"Usuario {data.username} creado exitosamente.",
        "id": usuario["id"],
        "nombre": data.nombre,
        "status_code": status.HTTP_201_CREATED
    }

# Endpoint GET para obtener usuarios
@app.get("/usuarios/", tags=["Usuarios"], status_code=status.HTTP_200_OK)
async def obtener_usuarios():
    if not usuarios:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay usuarios disponibles.")
    return JSONResponse(status_code=status.HTTP_200_OK, content=usuarios)

# Endpoint GET para obtener un usuario específico por ID
@app.get("/usuarios/{user_id}", tags=["Usuarios"])
async def obtener_usuario(user_id: str):
    for usuario in usuarios:
        if usuario["id"] == user_id:
            return JSONResponse(status_code=status.HTTP_200_OK, content=usuario)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")