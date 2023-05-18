from api.jira.api import Jira, JiraSearchResponseIssue


def list_to_jql(l: list[str]) -> str:
    content = [f'"{e}"' for e in l]
    return f'({", ".join(content)})'

def get_jql(
        issue_keys: list[str] | None = None,
        projects: list[str] | None = None, 
        types: list[str] | None = None, 
        statuses: list[str] | None = None, 
        require_story_points: bool = False):
    
    parts = []

    part_lookup = {
        'key': issue_keys, 
        'project': projects, 
        'type': types, 
        'status': statuses}
    
    for key, value in part_lookup.items():
        if value:
            parts.append(f'{key} in {list_to_jql(value)}')
    
    if require_story_points:
        parts.append('"Story Points[Number]" > 0')

    return ' & '.join(parts)

def get_all_issues(api: Jira, jql: str, fields: list[str], field_mappings: tuple[str, str] = [('customfield_10215', 'estimate')]) -> list[JiraSearchResponseIssue]:
    issues: list[JiraSearchResponseIssue] = []

    start = 0
    total = 1

    while start < total:
        response = api.search(jql, fields, start=start)
        
        issues += response.issues

        start = response.start + response.max_results
        total = response.total
        
    for issue in issues:
        for mapping_from, mapping_to in field_mappings: 
            if mapping_from in issue.fields:
                issue.fields[mapping_to] = issue.fields[mapping_from]
                del issue.fields[mapping_from]

    return issues

