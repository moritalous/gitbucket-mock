# GitBucket API Documentation

## Collaborators API

### 1. List Repository Collaborators

Retrieves a list of collaborators for a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/collaborators`

#### Request

```
GET /api/v3/repos/:owner/:repository/collaborators
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Repository not found |

##### Response Body

Returns an array of user objects representing the collaborators:

```json
[
  {
    "login": "string",
    "id": 0,
    "email": "string",
    "type": "string",
    "site_admin": "boolean",
    "created_at": "string",
    "url": "string",
    "html_url": "string",
    "avatar_url": "string"
  }
]
```

### 2. Check if a User is a Collaborator

Checks if a user is a collaborator on a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/collaborators/:userName`

#### Request

```
GET /api/v3/repos/:owner/:repository/collaborators/:userName
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `userName` | `string` | **Required**. The username of the potential collaborator. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 204 | User is a collaborator |
| 404 | User is not a collaborator or repository/user not found |

### 3. Get Repository Permissions for a User

Retrieves the permission level of a collaborator on a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/collaborators/:userName/permission`

#### Request

```
GET /api/v3/repos/:owner/:repository/collaborators/:userName/permission
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `userName` | `string` | **Required**. The username of the collaborator. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | User is not a collaborator or repository/user not found |

##### Response Body

Returns a collaborator object with permission information:

```json
{
  "permission": "string",
  "user": {
    "login": "string",
    "id": 0,
    "email": "string",
    "type": "string",
    "site_admin": "boolean",
    "created_at": "string",
    "url": "string",
    "html_url": "string",
    "avatar_url": "string"
  }
}
```

The `permission` field will be one of: `ADMIN`, `DEVELOPER`, or `GUEST`.

### 4. Add a Repository Collaborator

Adds a user as a collaborator to a repository.

**Endpoint:** `PUT /api/v3/repos/:owner/:repository/collaborators/:userName`

#### Request

```
PUT /api/v3/repos/:owner/:repository/collaborators/:userName
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `userName` | `string` | **Required**. The username of the user to add as a collaborator. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "permission": "push"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `permission` | `string` | **Yes** | The permission level for the collaborator. Must be one of: `"admin"` (Admin access, maps to `ADMIN` role), `"push"` (Push access, maps to `DEVELOPER` role), or `"pull"` (Pull access, maps to `GUEST` role) |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 204 | Success (No Content) |
| 401 | Unauthorized |
| 403 | Forbidden (not repository owner) |
| 404 | Repository or user not found |

### 5. Remove a Repository Collaborator

Removes a user as a collaborator from a repository.

**Endpoint:** `DELETE /api/v3/repos/:owner/:repository/collaborators/:userName`

#### Request

```
DELETE /api/v3/repos/:owner/:repository/collaborators/:userName
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `userName` | `string` | **Required**. The username of the collaborator to remove. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 204 | Success (No Content) |
| 401 | Unauthorized |
| 403 | Forbidden (not repository owner) |
| 404 | Repository not found |

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/collaborators
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Collaborator Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiRepositoryCollaboratorControllerBase.scala`
  - API Repository Collaborator: `gitbucket/src/main/scala/gitbucket/core/api/ApiRepositoryCollaborator.scala`
  - Add A Collaborator: `gitbucket/src/main/scala/gitbucket/core/api/AddACollaborator.scala`
