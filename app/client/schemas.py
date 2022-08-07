from typing import Any, List

from pydantic import BaseModel, Field


class CometLoginUserDto(BaseModel):
    email: str
    password: str
    signupToken: str | None


class CometPayload(BaseModel):
    operationName: str
    variables: dict
    query: str


# COMET Authentication Response Schemas
class Freelance(BaseModel):
    id: int
    isInstructor: bool
    isQualified: bool
    bitbucketUrl: str | None
    gitHubUrl: str | None
    gitlabUrl: str | None
    linkedInUrl: str
    prefContract: str
    prefEnvironment: str
    prefTime: str
    prefWorkplace: str
    profileScore: int
    status: str
    biography: str


class Authenticate(BaseModel):
    id: int
    email: str
    fullName: str
    jobTitle: str
    pendingActivation: bool
    phoneNumber: str
    profilePictureUrl: str
    slackId: Any
    slackUsername: Any
    termsValidated: bool
    termsValidatedAt: str
    corporate: Any
    freelance: Freelance


class Data(BaseModel):
    authenticate: Authenticate


class CometLoginResponseWrapper(BaseModel):
    cookie: dict
    data: Data


# COMET Skills Response Schemas
class Skill(BaseModel):
    id: int
    freelanceSkillId: int | None
    name: str
    primary: bool | None
    duration: int | None
    wishedInMissions: bool | None
    __typename: str


class SkillsResponse(BaseModel):
    freelanceId: int = Field(None, alias='id')
    skills: List[Skill] | None


# COMET Experiences Response Schemas
class Experience(BaseModel):
    id: int
    isCometMission: bool
    startDate: str
    endDate: str
    companyName: str
    description: str
    location: Any
    type: str
    skills: List[Skill]


class ExperiencesResponse(BaseModel):
    freelanceId: int = Field(None, alias='id')
    experienceInYears: int
    autoPilotEnabled: bool
    experiences: List[Experience]
