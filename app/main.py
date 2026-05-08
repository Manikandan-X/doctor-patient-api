import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)

from app.db.base import Base
from app.db.session import engine

# ✅ Load env
load_dotenv()




# ✅ Routers
from app.routers import auth
from app.routers import doctor as doctor_router
from app.routers import patient as patient_router
from app.routers import appointment as appointment_router
from app.routers import websocket, file

# ✅ Register model
import app.models

# ✅ Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ App
app = FastAPI()


# =========================
# ✅ GLOBAL EXCEPTION HANDLERS
# =========================
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# =========================
# ✅ CREATE TABLES
# =========================



# =========================
# ✅ STATIC FILES
# =========================
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# =========================
# ✅ CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ✅ ROOT
# =========================
@app.get("/")
def home():
    return {"message": "API Running"}


# =========================
# ✅ ROUTERS
# =========================
app.include_router(auth.router)
app.include_router(doctor_router.router)
app.include_router(patient_router.router)
app.include_router(appointment_router.router)
app.include_router(websocket.router)
app.include_router(file.router)