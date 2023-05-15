import dataclasses

import urlpath


@dataclasses.dataclass
class JiraConfiguration():
    token: str
    base_url: urlpath.URL = urlpath.URL('https://hesehus-jira.atlassian.net/')