from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Configuración del hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración del token JWT
SECRET_KEY = "tu_clave_secreta_super_segura"  # 🔐 Reemplaza esto por una clave segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Token válido por 60 minutos

# Función para hashear contraseñas
def hashear_contraseña(contraseña: str) -> str:
    return pwd_context.hash(contraseña)

# Función para verificar contraseñas
def verificar_contraseña(contraseña_plana: str, contraseña_hashed: str) -> bool:
    return pwd_context.verify(contraseña_plana, contraseña_hashed)

# Función para crear token JWT
def crear_token_acceso(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
