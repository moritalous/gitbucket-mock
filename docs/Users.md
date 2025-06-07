# GitBucket API Documentation

## Users API

### 1. Get Users

Retrieves a list of all users registered in GitBucket.

**Endpoint:** `GET /api/v3/users`

#### Request

```
GET /api/v3/users
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
| 401 | Unauthorized (if authentication is required) |

##### Response Body

Returns an array of user objects with the following structure:

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

### 2. Get a Single User

Retrieves information about a specific user.

**Endpoint:** `GET /api/v3/users/:userName`

#### Request

```
GET /api/v3/users/:userName
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `userName` | `string` | **Required**. The username of the user to retrieve. |

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

Returns a user object with the following structure:

```json
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
```

### 3. Get the Authenticated User

Retrieves information about the currently authenticated user.

**Endpoint:** `GET /api/v3/user`

#### Request

```
GET /api/v3/user
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

Returns a user object with the following structure:

```json
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
```

### 4. Update the Authenticated User

Updates information for the currently authenticated user.

**Endpoint:** `PATCH /api/v3/user`

#### Request

```
PATCH /api/v3/user
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
  "email": "string",
  "blog": "string",
  "company": "string",
  "location": "string",
  "hireable": true,
  "bio": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | No | The user's full name. Can be `null` |
| `email` | `string` | No | The user's email address. Can be `null` |
| `blog` | `string` | No | The user's blog/website URL. Can be `null` |
| `company` | `string` | No | The user's company. Can be `null` |
| `location` | `string` | No | The user's location. Can be `null` |
| `hireable` | `boolean` | No | Whether the user is available for hire. Can be `null` |
| `bio` | `string` | No | The user's biography. Can be `null` |

**Note:** All fields are optional. Only specified fields will be updated.

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |

##### Response Body

Returns the updated user object:

```json
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
```

### 5. Create a New User (Admin Only)

Creates a new user account. This endpoint is only available to administrators.

**Endpoint:** `POST /api/v3/admin/users`

#### Request

```
POST /api/v3/admin/users
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
  "password": "string",
  "email": "string",
  "fullName": "string",
  "isAdmin": false,
  "description": "string",
  "url": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `login` | `string` | **Yes** | Username for the new account |
| `password` | `string` | **Yes** | Password for the new account |
| `email` | `string` | **Yes** | Email address for the new account |
| `fullName` | `string` | No | Full name of the user. Can be `null`. Defaults to login name if not specified |
| `isAdmin` | `boolean` | No | Whether the user should have administrator privileges. Can be `null`. Default: `false` |
| `description` | `string` | No | User description/bio. Can be `null` |
| `url` | `string` | No | User's website URL. Can be `null` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 403 | Forbidden (not an administrator) |

##### Response Body

Returns the newly created user object:

```json
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
```

### 6. Suspend a User (Admin Only)

Suspends a user account. This endpoint is only available to administrators.

**Endpoint:** `PUT /api/v3/users/:userName/suspended`

#### Request

```
PUT /api/v3/users/:userName/suspended
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `userName` | `string` | **Required**. The username of the user to suspend. |

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
| 403 | Forbidden (not an administrator) |
| 404 | User not found |

### 7. Unsuspend a User (Admin Only)

Unsuspends a previously suspended user account. This endpoint is only available to administrators.

**Endpoint:** `DELETE /api/v3/users/:userName/suspended`

#### Request

```
DELETE /api/v3/users/:userName/suspended
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `userName` | `string` | **Required**. The username of the user to unsuspend. |

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
| 403 | Forbidden (not an administrator) |
| 404 | User not found |

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/users/users
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - User Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiUserControllerBase.scala`
  - Model: `gitbucket/src/main/scala/gitbucket/core/model/User.scala`
  - Service: `gitbucket/src/main/scala/gitbucket/core/service/UserService.scala`
  - API User: `gitbucket/src/main/scala/gitbucket/core/api/ApiUser.scala`
  - Create User: `gitbucket/src/main/scala/gitbucket/core/api/CreateAUser.scala`
  - Update User: `gitbucket/src/main/scala/gitbucket/core/api/UpdateAUser.scala`
