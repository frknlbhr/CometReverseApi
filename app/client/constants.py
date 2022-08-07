import enum
from dataclasses import dataclass


auth_query_string = "mutation authenticate($email: EmailType!, $password: String!, $signupToken: String) {\n  authenticate(email: $email, password: $password, signupToken: $signupToken) {\n    id\n    ...User\n    __typename\n  }\n}\n\nfragment User on User {\n  id\n  email\n  firstName\n  fullName\n  jobTitle\n  lastName\n  pendingActivation\n  phoneNumber\n  profilePictureUrl\n  slackId\n  slackUsername\n  termsValidated\n  termsValidatedAt\n  unreadChatMessagesCount\n  unseenMentionsCount\n  mentionsViewedAt\n  corporate {\n    id\n    comments\n    companyId\n    role\n    token\n    missions {\n      id\n      count\n      __typename\n    }\n    missionPendingRating {\n      id\n      __typename\n    }\n    company {\n      id\n      skipTermsValidation\n      __typename\n    }\n    __typename\n  }\n  freelance {\n    id\n    preUser\n    isInstructor\n    flaggedForQualif\n    isFrozen\n    isQualified\n    acquisitionSource\n    availabilityDate\n    bankName\n    bic\n    bitbucketUrl\n    callAvailability\n    gitHubUrl\n    gitlabUrl\n    iban\n    isAvailable\n    isBillable\n    kaggleUrl\n    linkedInUrl\n    shouldUpdateAvailability\n    maxDistance\n    prefContract\n    prefEnvironment\n    prefMobility\n    prefTime\n    prefWorkplace\n    profileScore\n    publicId\n    referralCode\n    retribution\n    retryDate\n    stackExchangeUrl\n    status\n    talentSuccessManagerId\n    twitterUrl\n    websiteUrl\n    slackStatus\n    ...LinkedInImport\n    __typename\n  }\n  teamMember {\n    id\n    accountManager\n    ...TeamMemberTip\n    __typename\n  }\n  impersonating {\n    id\n    email\n    firstName\n    lastName\n    fullName\n    teamMember {\n      id\n      __typename\n    }\n    __typename\n  }\n  ...FreelancerNavBar\n  ...UserFlags\n  ...CorporatePermissions\n  ...FreelancePermissions\n  __typename\n}\n\nfragment TeamMemberTip on TeamMember {\n  id\n  tips\n  __typename\n}\n\nfragment UserFlags on User {\n  id\n  corporate {\n    id\n    ...CorporateFlags\n    __typename\n  }\n  freelance {\n    id\n    ...FreelancerFlags\n    __typename\n  }\n  __typename\n}\n\nfragment CorporateFlags on Corporate {\n  id\n  flags {\n    id\n    ...Flag\n    __typename\n  }\n  __typename\n}\n\nfragment Flag on Flag {\n  id\n  level\n  once\n  payload\n  permanent\n  type\n  __typename\n}\n\nfragment FreelancerFlags on Freelance {\n  id\n  flags {\n    id\n    ...Flag\n    __typename\n  }\n  __typename\n}\n\nfragment FreelancerNavBar on User {\n  id\n  slackId\n  profilePictureUrl\n  unreadChatMessagesCount\n  freelance {\n    id\n    status\n    __typename\n  }\n  __typename\n}\n\nfragment CorporatePermissions on User {\n  id\n  permissions {\n    id\n    showProfile\n    showMissions\n    showAdministration\n    showCommunity\n    showCrew\n    __typename\n  }\n  __typename\n}\n\nfragment FreelancePermissions on User {\n  id\n  permissions {\n    id\n    showProfile\n    showMissions\n    showStore\n    showInfos\n    showExperiences\n    showQualification\n    showInstructor\n    askForQualification\n    showPreferences\n    showCompany\n    __typename\n  }\n  __typename\n}\n\nfragment LinkedInImport on Freelance {\n  id\n  fetchingLinkedIn\n  lastLinkedInImport {\n    id\n    status\n    lastError\n    importedAt\n    __typename\n  }\n  biography\n  user {\n    id\n    profilePictureUrl\n    jobTitle\n    __typename\n  }\n  __typename\n}\n"
skills_query_string = "query FreelancerProfileSkills($id: ID!) {\n  freelance(id: $id) {\n    id\n    skills {\n      id\n      freelanceSkillId\n      name\n      duration\n      wishedInMissions\n      __typename\n    }\n    __typename\n  }\n}\n"
skills_query_hash = 'f1ad18fe651a8b7db89a731a955650b72c26cf99c4fe8288f4c8c5d09200737a'
experiences_query_string = "query FreelancerExperiences($id: ID!) {\n  freelance(id: $id) {\n    id\n    experienceInYears\n    autoPilotEnabled\n    experiences {\n      id\n      ...FreelancerExperience\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FreelancerExperience on Experience {\n  id\n  isCometMission\n  startDate\n  endDate\n  companyName\n  description\n  location\n  type\n  skills {\n    id\n    name\n    primary\n    freelanceExperienceSkillId\n    __typename\n  }\n  __typename\n}\n"
experiences_query_hash = '3711c32cb6e43625dbbc63db6065dd1223c23b02e6544f6d5db23af15d903b6b'

comet_base_url = 'https://app.comet.co/api/graphql'
version = 'master-d83bcbf7'


@dataclass
class CometOperationDefinition:
    operation_name: str
    query_string: str
    query_hash: str
    version: str

    def __hash__(self):
        hash(self.operation_name)


class CometOperation(enum.Enum):
    auth = CometOperationDefinition(operation_name='authenticate',
                                    query_string=auth_query_string,
                                    query_hash='',
                                    version='')
    skills = CometOperationDefinition(operation_name='FreelancerProfileSkills',
                                      query_string=skills_query_string,
                                      query_hash=skills_query_hash,
                                      version=version)
    experiences = CometOperationDefinition(operation_name='FreelancerExperiences',
                                           query_string=experiences_query_string,
                                           query_hash=experiences_query_hash,
                                           version=version)

    def __repr__(self):
        return self.value
