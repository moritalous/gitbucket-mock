# GitBucket API Documentation

## Milestones API

### 1. List Milestones

Retrieves a list of milestones for a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/milestones`

#### Request

```
GET /api/v3/repos/:owner/:repository/milestones
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `state` | `string` | Optional. Filter milestones by state. Can be `open`, `closed`, or `all`. Default: `all`. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Repository not found or invalid state parameter |

##### Response Body

Returns an array of milestone objects with the following structure:

```json
[
  {
    "url": "string",
    "html_url": "string",
    "id": 0,
    "number": 0,
    "state": "string",
    "title": "string",
    "description": "string",
    "open_issues": 0,
    "closed_issues": 0,
    "closed_at": "string",
    "due_on": "string"
  }
]
```

The `state` field can be either `"open"` or `"closed"`.

### 2. Get a Milestone

Retrieves a specific milestone.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/milestones/:number`

#### Request

```
GET /api/v3/repos/:owner/:repository/milestones/:number
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `number` | `integer` | **Required**. The milestone ID. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Milestone or repository not found |

##### Response Body

Returns a milestone object with the same structure as in the "List Milestones" endpoint.

### 3. Create a Milestone

Creates a new milestone in a repository.

**Endpoint:** `POST /api/v3/repos/:owner/:repository/milestones`

#### Request

```
POST /api/v3/repos/:owner/:repository/milestones
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
  "state": "string",
  "description": "string",
  "due_on": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | **Yes** | The title of the milestone. Must be 100 characters or less and contain only alphanumeric characters, hyphens, plus signs, underscores, or periods |
| `state` | `string` | No | The state of the milestone. Can be `open` or `closed`. Default: `open` |
| `description` | `string` | No | A description of the milestone. Can be `null` |
| `due_on` | `string` | No | The milestone due date in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`. Can be `null` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Repository not found or invalid parameters |

##### Response Body

Returns the created milestone object with the same structure as in the "Get a Milestone" endpoint.

### 4. Update a Milestone

Updates an existing milestone.

**Endpoint:** `PATCH /api/v3/repos/:owner/:repository/milestones/:number`

#### Request

```
PATCH /api/v3/repos/:owner/:repository/milestones/:number
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `number` | `integer` | **Required**. The milestone ID. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "title": "string",
  "state": "string",
  "description": "string",
  "due_on": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | No | The title of the milestone. Must be 100 characters or less and contain only alphanumeric characters, hyphens, plus signs, underscores, or periods. Can be `null` |
| `state` | `string` | No | The state of the milestone. Can be `open` or `closed`. Can be `null` |
| `description` | `string` | No | A description of the milestone. Can be `null` |
| `due_on` | `string` | No | The milestone due date in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`. Can be `null` |

**Note:** At least one field should be provided to update the milestone.

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Milestone or repository not found |

##### Response Body

Returns the updated milestone object with the same structure as in the "Get a Milestone" endpoint.

### 5. Delete a Milestone

Deletes a milestone from a repository.

**Endpoint:** `DELETE /api/v3/repos/:owner/:repository/milestones/:number`

#### Request

```
DELETE /api/v3/repos/:owner/:repository/milestones/:number
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `number` | `integer` | **Required**. The milestone ID. |

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
| 404 | Milestone or repository not found |

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/issues/milestones
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Milestone Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiIssueMilestoneControllerBase.scala`
  - API Milestone: `gitbucket/src/main/scala/gitbucket/core/api/ApiMilestone.scala`
  - Create A Milestone: `gitbucket/src/main/scala/gitbucket/core/api/CreateAMilestone.scala`
