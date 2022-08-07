import json

from fastapi import HTTPException
from pydantic import ValidationError, BaseModel
from requests import Session, Response

from app import loggr
from app.client.constants import CometOperation, comet_base_url
from app.client.schemas import CometLoginUserDto, CometPayload, CometLoginResponseWrapper, SkillsResponse, \
    ExperiencesResponse
from app.persistence.models import User
from app.schemas import AuthRequest

logger = loggr.get_logger(__name__)


def login(auth_request: AuthRequest) -> CometLoginResponseWrapper:
    logger.info('Login request to Comet for %s username', auth_request.username)
    rest_client_session = Session()
    login_payload = create_auth_payload(auth_request)
    headers = create_headers_from_operation(CometOperation.auth)
    response = rest_client_session.post(url=comet_base_url, data=login_payload.json(), headers=headers)
    return handle_response(response, CometOperation.auth)


def get_skills(user: User) -> SkillsResponse:
    logger.info('Skills request to Comet for %s username', user.username)
    rest_client_session = get_session_with_user_cookie(user)
    skills_payload = create_payload_from_operation_and_user(CometOperation.skills, user)
    headers = create_headers_from_operation(CometOperation.skills)
    response = rest_client_session.post(url=comet_base_url, data=skills_payload.json(), headers=headers)
    return handle_response(response, CometOperation.skills)


def get_experiences(user: User) -> ExperiencesResponse:
    logger.info('Experiences request to Comet for %s username', user.username)
    rest_client_session = get_session_with_user_cookie(user)
    experiences_payload = create_payload_from_operation_and_user(CometOperation.experiences, user)
    headers = create_headers_from_operation(CometOperation.experiences)
    response = rest_client_session.post(url=comet_base_url, data=experiences_payload.json(), headers=headers)
    return handle_response(response, CometOperation.experiences)


def get_session_with_user_cookie(user: User):
    rest_client_session = Session()
    rest_client_session.cookies.update(user.cookie)
    return rest_client_session


def create_auth_payload(auth_request: AuthRequest) -> CometPayload:
    login_user_dto = CometLoginUserDto(email=auth_request.username, password=auth_request.password)
    return CometPayload(operationName=CometOperation.auth.value.operation_name,
                        variables=login_user_dto.dict(),
                        query=CometOperation.auth.value.query_string)


def create_payload_from_operation_and_user(comet_operation: CometOperation, user: User) -> CometPayload:
    variables = {'id': user.freelancer_id}
    return CometPayload(operationName=comet_operation.value.operation_name,
                        variables=variables,
                        query=comet_operation.value.query_string)


def create_headers_from_operation(comet_operation: CometOperation) -> dict:
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    if comet_operation == CometOperation.auth:
        headers['authority'] = 'app.comet.co'
    else:
        headers['x-queryhash'] = comet_operation.value.query_hash
        headers['x-version'] = comet_operation.value.version
    return headers


def handle_response(response: Response, comet_operation: CometOperation) -> BaseModel:
    logger.info('http status code from Comet is %s ', response.status_code)
    if response.status_code == 200:
        content_dict = json.loads(response.content)
        if 'data' in content_dict.keys() and content_dict['data'] is not None:
            try:
                match comet_operation:
                    case CometOperation.auth:
                        content_dict['cookie'] = response.cookies.get_dict()
                        response_data = CometLoginResponseWrapper.parse_obj(content_dict)
                    case CometOperation.skills:
                        response_data = SkillsResponse.parse_obj(content_dict['data']['freelance'])
                    case CometOperation.experiences:
                        response_data = ExperiencesResponse.parse_obj(content_dict['data']['freelance'])
            except ValidationError as e:
                logger.error(e)
                raise HTTPException(status_code=401, detail='Comet login error')
            return response_data
    raise HTTPException(status_code=401, detail='Comet login error')
