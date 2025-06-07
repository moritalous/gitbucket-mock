# GitBucket API Documentation

## Commits API

### 1. List Commits

Retrieves a list of commits for a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/commits`

#### Request

```
GET /api/v3/repos/:owner/:repository/commits
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `sha` | `string` | Optional. The SHA or branch to start listing commits from. Default: the repository's default branch (usually `main`). |
| `path` | `string` | Optional. Only commits containing this file path will be returned. |
| `author` | `string` | Optional. GitHub login or email address by which to filter by commit author. |
| `since` | `string` | Optional. Only commits after this date will be returned. ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`. |
| `until` | `string` | Optional. Only commits before this date will be returned. ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`. |
| `page` | `integer` | Optional. Page number of the results to fetch. Default: `1`. |
| `per_page` | `integer` | Optional. Number of results per page. Default: `30`. Maximum: `100`. |

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

Returns an array of commit objects with the following structure:

```json
[
  {
    "url": "string",
    "sha": "string",
    "html_url": "string",
    "comment_url": "string",
    "commit": {
      "url": "string",
      "author": {
        "name": "string",
        "email": "string",
        "date": "string"
      },
      "committer": {
        "name": "string",
        "email": "string",
        "date": "string"
      },
      "message": "string",
      "comment_count": 0,
      "tree": {
        "url": "string",
        "sha": "string"
      }
    },
    "author": {
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
    "committer": {
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
    "parents": [
      {
        "url": "string",
        "sha": "string"
      }
    ],
    "stats": {
      "additions": 0,
      "deletions": 0,
      "total": 0
    },
    "files": [
      {
        "filename": "string",
        "additions": 0,
        "deletions": 0,
        "changes": 0,
        "status": "string",
        "raw_url": "string",
        "blob_url": "string",
        "patch": "string"
      }
    ]
  }
]
```

### 2. Get a Commit

Retrieves a specific commit.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/commits/:sha`

#### Request

```
GET /api/v3/repos/:owner/:repository/commits/:sha
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `sha` | `string` | **Required**. The SHA of the commit to retrieve. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Commit or repository not found |

##### Response Body

Returns a commit object with the same structure as in the "List Commits" endpoint.

### 3. List Branches for HEAD Commit

Retrieves all branches where the given commit is the HEAD commit.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/commits/:sha/branches-where-head`

#### Request

```
GET /api/v3/repos/:owner/:repository/commits/:sha/branches-where-head
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `sha` | `string` | **Required**. The SHA of the commit to check. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Commit or repository not found |

##### Response Body

Returns an array of branch objects where the commit is the HEAD:

```json
[
  {
    "name": "string",
    "commit": {
      "sha": "string"
    },
    "protected": "boolean"
  }
]
```

### 4. Get the Combined Status for a Specific Reference

Retrieves the combined status for a specific reference (SHA, branch name, or tag name).

**Endpoint:** `GET /api/v3/repos/:owner/:repository/commits/:ref/status`

#### Request

```
GET /api/v3/repos/:owner/:repository/commits/:ref/status
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `ref` | `string` | **Required**. The reference (SHA, branch name, or tag name) to get the combined status for. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Reference or repository not found |

##### Response Body

Returns a combined status object:

```json
{
  "state": "string",
  "sha": "string",
  "total_count": 0,
  "statuses": [
    {
      "created_at": "string",
      "updated_at": "string",
      "state": "string",
      "target_url": "string",
      "description": "string",
      "id": 0,
      "context": "string",
      "creator": {
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
      "url": "string"
    }
  ],
  "repository": {
    "name": "string",
    "full_name": "string",
    "description": "string",
    "watchers": 0,
    "forks": 0,
    "private": "boolean",
    "default_branch": "string",
    "owner": {
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
    "has_issues": "boolean",
    "id": 0,
    "forks_count": 0,
    "watchers_count": 0,
    "url": "string",
    "clone_url": "string",
    "html_url": "string",
    "ssh_url": "string"
  },
  "url": "string"
}
```

The `state` field can be one of: `"pending"`, `"success"`, `"failure"`, or `"error"`.

### 5. List Statuses for a Specific Reference

Retrieves the statuses for a specific reference (SHA, branch name, or tag name).

**Endpoint:** `GET /api/v3/repos/:owner/:repository/commits/:ref/statuses`

#### Request

```
GET /api/v3/repos/:owner/:repository/commits/:ref/statuses
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `ref` | `string` | **Required**. The reference (SHA, branch name, or tag name) to list the statuses for. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Reference or repository not found |

##### Response Body

Returns an array of status objects:

```json
[
  {
    "created_at": "string",
    "updated_at": "string",
    "state": "string",
    "target_url": "string",
    "description": "string",
    "id": 0,
    "context": "string",
    "creator": {
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
    "url": "string"
  }
]
```

### 6. Create a Status

Creates a commit status.

**Endpoint:** `POST /api/v3/repos/:owner/:repository/statuses/:sha`

#### Request

```
POST /api/v3/repos/:owner/:repository/statuses/:sha
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `sha` | `string` | **Required**. The SHA of the commit to create a status for. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "state": "string",
  "target_url": "string",
  "description": "string",
  "context": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `state` | `string` | **Yes** | The state of the status. Can be one of: `"pending"`, `"success"`, `"failure"`, or `"error"` |
| `target_url` | `string` | No | The URL to associate with this status. Must be HTTP/HTTPS URL and less than 255 characters. Can be `null` |
| `description` | `string` | No | A short description of the status. Must be less than 1000 characters. Can be `null` |
| `context` | `string` | No | A string label to differentiate this status from the status of other systems. Must be less than 255 characters. Can be `null`. Default: `"default"` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Commit or repository not found |

##### Response Body

Returns the created status object.

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/commits
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Commit Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiRepositoryCommitControllerBase.scala`
  - Status Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiRepositoryStatusControllerBase.scala`
  - API Commits: `gitbucket/src/main/scala/gitbucket/core/api/ApiCommits.scala`
  - API Commit Status: `gitbucket/src/main/scala/gitbucket/core/api/ApiCommitStatus.scala`
  - API Combined Commit Status: `gitbucket/src/main/scala/gitbucket/core/api/ApiCombinedCommitStatus.scala`
  - Create A Status: `gitbucket/src/main/scala/gitbucket/core/api/CreateAStatus.scala`
