from datetime import datetime

# Organization data
ORGANIZATIONS = {
    "org1": {
        "login": "org1",
        "description": "Organization 1",
        "created_at": datetime(2023, 1, 5),
        "id": 101,
        "url": "/api/v3/orgs/org1",
        "html_url": "/org1",
        "avatar_url": "/org1/avatar",
    },
    "org2": {
        "login": "org2",
        "description": "Organization 2",
        "created_at": datetime(2023, 2, 10),
        "id": 102,
        "url": "/api/v3/orgs/org2",
        "html_url": "/org2",
        "avatar_url": "/org2/avatar",
    },
}

# User-organization associations
USER_ORGANIZATIONS = {"admin": ["org1", "org2"], "user1": ["org1"]}


def get_organization_by_name(org_name):
    """Get organization by name"""
    return ORGANIZATIONS.get(org_name)


def get_organizations_for_user(username):
    """Get organizations that user belongs to"""
    org_names = USER_ORGANIZATIONS.get(username, [])
    return [
        ORGANIZATIONS[org_name] for org_name in org_names if org_name in ORGANIZATIONS
    ]


def create_organization(org_data):
    """Create a new organization"""
    org_name = org_data["login"]
    if org_name in ORGANIZATIONS:
        return None

    # Create new organization
    new_org = {
        "login": org_name,
        "description": org_data.get("profile_name", ""),
        "created_at": datetime.now(),
        "id": len(ORGANIZATIONS) + 101,
        "url": f"/api/v3/orgs/{org_name}",
        "html_url": f"/{org_name}",
        "avatar_url": f"/{org_name}/avatar",
    }

    ORGANIZATIONS[org_name] = new_org

    # Associate admin with organization
    admin_username = org_data["admin"]
    if admin_username not in USER_ORGANIZATIONS:
        USER_ORGANIZATIONS[admin_username] = []

    if org_name not in USER_ORGANIZATIONS[admin_username]:
        USER_ORGANIZATIONS[admin_username].append(org_name)

    return new_org
