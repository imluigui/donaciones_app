from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext

# Configuración de seguridad
SECRET_KEY = "tu_clave_secreta_super_segura" # Debería ser una variable de entorno en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Usamos 'sha256_crypt' o 'pbkdf2_sha256' si bcrypt sigue fallando,
# pero vamos a intentar forzar una configuración más sencilla en passlib.
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # bcrypt limita a 72 bytes. Si la contraseña es corta, no hace falta truncar.
    # El error es en el test con una contraseña dummy gigante creada por passlib internamente al detectar el backend.
    # Vamos a usar una contraseña segura pero corta para el hash.
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
