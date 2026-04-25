import logging
from fastapi import FastAPI
from dotenv import load_dotenv

from app.database import engine
import app.models as models
from app.routers import doctor, patient, appointment, auth

# ✅ Load environment variables
load_dotenv()

# ✅ Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ✅ Create DB tables
models.Base.metadata.create_all(bind=engine)

# ✅ Create app
app = FastAPI()

# ✅ Root API
@app.get("/")
def home():
    logger.info("Home endpoint called")
    return {"message": "Advanced API Running"}

# ✅ Include routers
app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(patient.router)
app.include_router(appointment.router)