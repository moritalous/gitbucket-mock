# GitBucket API Documentation

## Repositories API

### 1. List All Public Repositories

Retrieves a list of all public repositories.

**Endpoint:** `GET /api/v3/repositories`

#### Request

```
GET /api/v3/repositories
```

#### Parameters

None required.

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |

##### Response Body

Returns an array of repository objects with the following structure:

```json
[
  {
    "name": "string",
    "full_name": "string",
    "description": "string",
    "watchers": 0,
    "forks": 0,
    "private": false,
    "default_branch": "string",
    "owner": {
      "login": "string",
      "id": 0,
      "email": "string",
      "type": "string",
      "site_admin": false,
      "created_at": "string",
      "url": "string",
      "html_url": "string",
      "avatar_url": "string"
    },
    "has_issues": true,
    "id": 0,
    "forks_count": 0,
    "watchers_count": 0,
    "url": "string",
    "clone_url": "string",
    "html_url": "string",
    "ssh_url": "string"
  }
]
```

### 2. List Repositories for the Authenticated User

Retrieves repositories for the authenticated user.

**Endpoint:** `GET /api/v3/user/repos`

#### Request

```
GET /api/v3/user/repos
```

#### Parameters

None required.

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |

##### Response Body

Returns an array of repository objects owned by the authenticated user with the same structure as the "List All Public Repositories" endpoint.

### 3. List User's Repositories

Retrieves repositories for a specific user.

**Endpoint:** `GET /api/v3/users/:userName/repos`

#### Request

```
GET /api/v3/users/:userName/repos
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `userName` | `string` | **Required**. The username of the user whose repositories to retrieve. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | User not found |

##### Response Body

Returns an array of repository objects owned by the specified user with the same structure as the "List All Public Repositories" endpoint.

### 4. Get Repository

Retrieves information about a specific repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository`

#### Request

```
GET /api/v3/repos/:owner/:repository
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

Returns a repository object with the same structure as in the "List All Public Repositories" endpoint.

### 5. Create Repository for the Authenticated User

Creates a new repository for the authenticated user.

**Endpoint:** `POST /api/v3/user/repos`

#### Request

```
POST /api/v3/user/repos
```

#### Parameters

None required in URL.

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "name": "string",
  "description": "string",
  "private": false,
  "auto_init": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | **Yes** | The name of the repository. Must be 100 characters or less, contain only alphanumeric characters, hyphens, plus signs, underscores, or periods, and cannot start with an underscore or hyphen |
| `description` | `string` | No | A description of the repository. Can be `null` |
| `private` | `boolean` | No | Whether the repository is private. Default: `false` |
| `auto_init` | `boolean` | No | Whether to create an initial commit with README. Default: `false` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Not Found (invalid JSON body) |

##### Response Body

Returns the newly created repository object with the same structure as in the "List All Public Repositories" endpoint.

### 6. Create Repository in an Organization

Creates a new repository in an organization.

**Endpoint:** `POST /api/v3/orgs/:org/repos`

#### Request

```
POST /api/v3/orgs/:org/repos
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `org` | `string` | **Required**. The name of the organization. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "name": "string",
  "description": "string",
  "private": false,
  "auto_init": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | **Yes** | The name of the repository. Must be 100 characters or less, contain only alphanumeric characters, hyphens, plus signs, underscores, or periods, and cannot start with an underscore or hyphen |
| `description` | `string` | No | A description of the repository. Can be `null` |
| `private` | `boolean` | No | Whether the repository is private. Default: `false` |
| `auto_init` | `boolean` | No | Whether to create an initial commit with README. Default: `false` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 403 | Forbidden (user cannot create repository in this organization) |
| 404 | Not Found (invalid JSON body or organization not found) |

##### Response Body

Returns the newly created repository object with the same structure as in the "List All Public Repositories" endpoint.

### 7. List Repository Tags

Retrieves a list of tags for a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/tags`

#### Request

```
GET /api/v3/repos/:owner/:repository/tags
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

Returns an array of tag objects.

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/repos
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Repository Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiRepositoryControllerBase.scala`
  - API Repository: `gitbucket/src/main/scala/gitbucket/core/api/ApiRepository.scala`
  - Create Repository: `gitbucket/src/main/scala/gitbucket/core/api/CreateARepository.scala`
