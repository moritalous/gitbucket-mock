# GitBucket API Documentation

## Organizations API

### 1. List All Organizations

Retrieves a list of all organizations.

**Endpoint:** `GET /api/v3/organizations`

#### Request

```
GET /api/v3/organizations
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

Returns an array of organization objects with the following structure:

```json
[
  {
    "login": "string",
    "description": "string",
    "created_at": "string",
    "id": 0,
    "url": "string",
    "html_url": "string",
    "avatar_url": "string"
  }
]
```

### 2. Get an Organization

Retrieves information about a specific organization.

**Endpoint:** `GET /api/v3/orgs/:groupName`

#### Request

```
GET /api/v3/orgs/:groupName
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `groupName` | `string` | **Required**. The name of the organization. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Organization not found |

##### Response Body

Returns an organization object with the following structure:

```json
{
  "login": "string",
  "description": "string",
  "created_at": "string",
  "id": 0,
  "url": "string",
  "html_url": "string",
  "avatar_url": "string"
}
```

### 3. List Organization Repositories

Retrieves repositories for a specific organization.

**Endpoint:** `GET /api/v3/orgs/:orgName/repos`

#### Request

```
GET /api/v3/orgs/:orgName/repos
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `orgName` | `string` | **Required**. The name of the organization. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Organization not found |

##### Response Body

Returns an array of repository objects owned by the specified organization.

### 4. List User's Organizations

Retrieves organizations for a specific user.

**Endpoint:** `GET /api/v3/users/:userName/orgs`

#### Request

```
GET /api/v3/users/:userName/orgs
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `userName` | `string` | **Required**. The username of the user whose organizations to retrieve. |

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

Returns an array of organization objects that the specified user is a member of.

### 5. List Your Organizations

Retrieves organizations for the authenticated user.

**Endpoint:** `GET /api/v3/user/orgs`

#### Request

```
GET /api/v3/user/orgs
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

Returns an array of organization objects that the authenticated user is a member of.

### 6. Create an Organization (Admin Only)

Creates a new organization. This endpoint is only available to administrators.

**Endpoint:** `POST /api/v3/admin/organizations`

#### Request

```
POST /api/v3/admin/organizations
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
  "login": "string",
  "admin": "string",
  "profile_name": "string",
  "url": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `login` | `string` | **Yes** | The name of the organization |
| `admin` | `string` | **Yes** | The username of the user who will be the organization administrator |
| `profile_name` | `string` | No | The display name of the organization. Can be `null` |
| `url` | `string` | No | The URL of the organization's website. Can be `null` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 403 | Forbidden (not an administrator) |

##### Response Body

Returns the newly created organization object.

### 7. Create Repository in an Organization

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

Required fields:
- `name`: The name of the repository. Must be 100 characters or less, contain only alphanumeric characters, hyphens, plus signs, underscores, or periods, and cannot start with an underscore or hyphen.

Optional fields:
- `description`: A description of the repository
- `private`: Whether the repository is private (defaults to false)
- `auto_init`: Whether to create an initial commit with README (defaults to false)

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 403 | Forbidden (user cannot create repository in this organization) |
| 404 | Not Found (invalid JSON body or organization not found) |

##### Response Body

Returns the newly created repository object.

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/orgs
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Organization Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiOrganizationControllerBase.scala`
  - API Group: `gitbucket/src/main/scala/gitbucket/core/api/ApiGroup.scala`
  - Create Group: `gitbucket/src/main/scala/gitbucket/core/api/CreateAGroup.scala`
