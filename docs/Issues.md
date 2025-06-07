# GitBucket API Documentation

## Issues API

### 1. List Issues for a Repository

Retrieves a list of issues for a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/issues`

#### Request

```
GET /api/v3/repos/:owner/:repository/issues
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `state` | `string` | Optional. Filter issues by state. Can be `open`, `closed`, or `all`. Default: `open`. |
| `page` | `integer` | Optional. Page number of the results to fetch. Default: `1`. |

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

Returns an array of issue objects with the following structure:

```json
[
  {
    "number": 0,
    "title": "string",
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
    },
    "assignees": [
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
    ],
    "labels": [
      {
        "name": "string",
        "color": "string"
      }
    ],
    "state": "string",
    "created_at": "string",
    "updated_at": "string",
    "body": "string",
    "milestone": {
      "number": 0,
      "state": "string",
      "title": "string",
      "description": "string",
      "created_at": "string",
      "updated_at": "string",
      "due_on": "string",
      "closed_at": "string"
    },
    "id": 0,
    "assignee": {
      "login": "string",
      "id": 0,
      "email": "string",
      "type": "string",
      "site_admin": "boolean",
      "created_at": "string",
      "url": "string",
      "html_url": "string",
      "avatar_url": "string"
    },
    "comments_url": "string",
    "html_url": "string",
    "pull_request": {
      "url": "string",
      "html_url": "string"
    }
  }
]
```

The `state` field can be either `"open"` or `"closed"`.

### 2. Get a Single Issue

Retrieves a specific issue.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/issues/:id`

#### Request

```
GET /api/v3/repos/:owner/:repository/issues/:id
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The issue number. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Issue or repository not found |

##### Response Body

Returns an issue object with the same structure as in the "List Issues for a Repository" endpoint.

### 3. Create an Issue

Creates a new issue in a repository.

**Endpoint:** `POST /api/v3/repos/:owner/:repository/issues`

#### Request

```
POST /api/v3/repos/:owner/:repository/issues
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "title": "string",
  "body": "string",
  "assignees": ["string"],
  "milestone": 1,
  "labels": ["string"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | **Yes** | The title of the issue |
| `body` | `string` | No | The contents of the issue. Can be `null` |
| `assignees` | `array[string]` | No | Logins for users to assign to this issue. Can be empty array `[]` |
| `milestone` | `integer` | No | The milestone ID to associate this issue with. Can be `null` |
| `labels` | `array[string]` | No | Labels to associate with this issue. Can be empty array `[]` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Repository not found |

##### Response Body

Returns the created issue object with the same structure as in the "Get a Single Issue" endpoint.

### 4. List Issue Comments

Retrieves a list of comments for a specific issue.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/issues/:id/comments`

#### Request

```
GET /api/v3/repos/:owner/:repository/issues/:id/comments
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The issue number. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Issue or repository not found |

##### Response Body

Returns an array of comment objects with the following structure:

```json
[
  {
    "id": 0,
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
    },
    "body": "string",
    "created_at": "string",
    "updated_at": "string",
    "html_url": "string"
  }
]
```

### 5. Get an Issue Comment

Retrieves a specific comment for an issue.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/issues/comments/:id`

#### Request

```
GET /api/v3/repos/:owner/:repository/issues/comments/:id
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The comment ID. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Comment or repository not found |

##### Response Body

Returns a comment object with the same structure as in the "List Issue Comments" endpoint.

### 6. Create an Issue Comment

Creates a new comment on an issue.

**Endpoint:** `POST /api/v3/repos/:owner/:repository/issues/:id/comments`

#### Request

```
POST /api/v3/repos/:owner/:repository/issues/:id/comments
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The issue number. |
| `action` | `string` | Optional. Action to perform. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "body": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `body` | `string` | **Yes** | The contents of the comment |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Issue or repository not found |

##### Response Body

Returns the created comment object with the same structure as in the "Get an Issue Comment" endpoint.

### 7. Update an Issue Comment

Updates an existing comment on an issue.

**Endpoint:** `PATCH /api/v3/repos/:owner/:repository/issues/comments/:id`

#### Request

```
PATCH /api/v3/repos/:owner/:repository/issues/comments/:id
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The comment ID. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "body": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `body` | `string` | **Yes** | The contents of the comment |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 403 | Forbidden (not comment author or repository owner) |
| 404 | Comment or repository not found |

##### Response Body

Returns the updated comment object with the same structure as in the "Get an Issue Comment" endpoint.

### 8. Delete an Issue Comment

Deletes a comment from an issue.

**Endpoint:** `DELETE /api/v3/repos/:owner/:repository/issues/comments/:id`

#### Request

```
DELETE /api/v3/repos/:owner/:repository/issues/comments/:id
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The comment ID. |

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
| 403 | Forbidden (not comment author or repository owner) |
| 404 | Comment or repository not found |

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/issues
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Issue Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiIssueControllerBase.scala`
  - Issue Comment Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiIssueCommentControllerBase.scala`
  - API Issue: `gitbucket/src/main/scala/gitbucket/core/api/ApiIssue.scala`
  - API Comment: `gitbucket/src/main/scala/gitbucket/core/api/ApiComment.scala`
  - Create An Issue: `gitbucket/src/main/scala/gitbucket/core/api/CreateAnIssue.scala`
  - Create A Comment: `gitbucket/src/main/scala/gitbucket/core/api/CreateAComment.scala`
