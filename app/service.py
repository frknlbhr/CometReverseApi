import uuid

from sqlalchemy.orm import Session

from app.client.operations import login, get_skills, get_experiences
from app.client.schemas import SkillsResponse, ExperiencesResponse
from app.persistence.crud import check_user_exist_by_username, create_user, update_user_cookie_by_username, \
    get_user_by_token
from app.schemas import AuthRequest, AuthResponse, AllDataResponse


def login_comet_and_save_user_cookie(auth_request: AuthRequest, db: Session) -> AuthResponse:
    comet_login_response = login(auth_request)
    if not check_user_exist_by_username(db, auth_request.username):
        token = uuid.uuid4().hex
        user = create_user(db, auth_request, token, comet_login_response.cookie,
                           comet_login_response.data.authenticate.freelance.id)
    else:
        user = update_user_cookie_by_username(db, auth_request.username, comet_login_response.cookie)
    return AuthResponse(username=user.username, token=user.token, profileInfo=comet_login_response.data.authenticate)


def fetch_skills_data_of_user(token: str, db: Session) -> SkillsResponse:
    logged_in_user = get_user_by_token(db, token)
    return get_skills(logged_in_user)


def fetch_experience_data_of_user(token: str, db: Session) -> ExperiencesResponse:
    logged_in_user = get_user_by_token(db, token)
    return get_experiences(logged_in_user)


def fetch_all_data(token: str, db: Session) -> AllDataResponse:
    skills_response = fetch_skills_data_of_user(token, db)
    experience_response = fetch_experience_data_of_user(token, db)
    return AllDataResponse(profileInfo=None, skillsInfo=skills_response, experiencesInfo=experience_response)


def authenticate_and_fetch_all_data(auth_request: AuthRequest, db: Session) -> AllDataResponse:
    auth_response = login_comet_and_save_user_cookie(auth_request, db)
    skills_response = fetch_skills_data_of_user(auth_response.token, db)
    experience_response = fetch_experience_data_of_user(auth_response.token, db)
    return AllDataResponse(profileInfo=auth_response.profileInfo, skillsInfo=skills_response,
                           experiencesInfo=experience_response)
