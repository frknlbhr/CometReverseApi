from pydantic import BaseModel

from app.client.schemas import Authenticate, SkillsResponse, ExperiencesResponse


class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    username: str
    token: str
    profileInfo: Authenticate


class AllDataResponse(BaseModel):
    profileInfo: Authenticate | None
    skillsInfo: SkillsResponse
    experiencesInfo: ExperiencesResponse
