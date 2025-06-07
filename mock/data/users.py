from datetime import datetime

# User data
USERS = {
    "admin": {
        "login": "admin",
        "id": 1,
        "email": "admin@example.com",
        "type": "User",
        "site_admin": True,
        "created_at": datetime(2023, 1, 1),
        "url": "/api/v3/users/admin",
        "html_url": "/admin",
        "avatar_url": "/admin/avatar",
    },
    "user1": {
        "login": "user1",
        "id": 2,
        "email": "user1@example.com",
        "type": "User",
        "site_admin": False,
        "created_at": datetime(2023, 1, 2),
        "url": "/api/v3/users/user1",
        "html_url": "/user1",
        "avatar_url": "/user1/avatar",
    },
}


def get_user_by_username(username):
    """Get user by username"""
    return USERS.get(username)


def create_user(user_data):
    """Create a new user"""
    username = user_data["login"]
    if username in USERS:
        return None

    USERS[username] = user_data
    return user_data


def update_user(username, update_data):
    """Update user information"""
    if username not in USERS:
        return None

    for key, value in update_data.items():
        if value is not None:
            USERS[username][key] = value

    return USERS[username]
