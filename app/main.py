import random
import string
import time

from fastapi import FastAPI, Request, Depends, Header
from sqlalchemy.orm import Session

from app import loggr
from app.client.schemas import SkillsResponse, ExperiencesResponse
from app.persistence import models
from app.persistence.database import engine, SessionLocal
from app.schemas import AuthRequest, AuthResponse, AllDataResponse
from app.service import login_comet_and_save_user_cookie, fetch_skills_data_of_user, fetch_experience_data_of_user, \
    fetch_all_data, authenticate_and_fetch_all_data

app = FastAPI()

logger = loggr.get_logger(__name__)

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    return response


@app.post("/auth", response_model=AuthResponse)
def auth(auth_request: AuthRequest, db: Session = Depends(get_db)):
    return login_comet_and_save_user_cookie(auth_request, db)


@app.get("/skills", response_model=SkillsResponse, response_model_by_alias=False, response_model_exclude_none=True)
def skills(token: str = Header(), db: Session = Depends(get_db)):
    return fetch_skills_data_of_user(token, db)


@app.get("/experiences", response_model=ExperiencesResponse, response_model_by_alias=False,
         response_model_exclude_none=True)
def experiences(token: str = Header(), db: Session = Depends(get_db)):
    return fetch_experience_data_of_user(token, db)


@app.get("/pull", response_model=AllDataResponse, response_model_by_alias=False, response_model_exclude_none=True)
def pull(token: str = Header(), db: Session = Depends(get_db)):
    return fetch_all_data(token, db)


@app.post("/fetch", response_model=AllDataResponse, response_model_by_alias=False, response_model_exclude_none=True)
def fetch(auth_request: AuthRequest, db: Session = Depends(get_db)):
    return authenticate_and_fetch_all_data(auth_request, db)
