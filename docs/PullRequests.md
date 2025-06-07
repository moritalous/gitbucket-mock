# GitBucket API Documentation

## Pull Requests API

### 1. List Pull Requests

Retrieves a list of pull requests for a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/pulls`

#### Request

```
GET /api/v3/repos/:owner/:repository/pulls
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `state` | `string` | Optional. Filter pull requests by state. Can be `open`, `closed`, or `all`. Default: `open`. |
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

Returns an array of pull request objects with the following structure:

```json
[
  {
    "number": 0,
    "state": "string",
    "updated_at": "string",
    "created_at": "string",
    "head": {
      "sha": "string",
      "ref": "string",
      "repo": {
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
      "label": "string",
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
    },
    "base": {
      "sha": "string",
      "ref": "string",
      "repo": {
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
      "label": "string",
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
    },
    "mergeable": "boolean",
    "merged": "boolean",
    "merged_at": "string",
    "merged_by": {
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
    "title": "string",
    "body": "string",
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
    "labels": [
      {
        "name": "string",
        "color": "string",
        "url": "string"
      }
    ],
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
    "draft": "boolean",
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
    "html_url": "string",
    "url": "string",
    "commits_url": "string",
    "review_comments_url": "string",
    "review_comment_url": "string",
    "comments_url": "string",
    "statuses_url": "string"
  }
]
```

The `state` field can be either `"open"` or `"closed"`.

### 2. Get a Pull Request

Retrieves a specific pull request.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/pulls/:id`

#### Request

```
GET /api/v3/repos/:owner/:repository/pulls/:id
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The pull request number. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Pull request or repository not found |

##### Response Body

Returns a pull request object with the same structure as in the "List Pull Requests" endpoint.

### 3. Create a Pull Request

Creates a new pull request in a repository.

**Endpoint:** `POST /api/v3/repos/:owner/:repository/pulls`

#### Request

```
POST /api/v3/repos/:owner/:repository/pulls
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

GitBucket supports two different ways to create pull requests using the same endpoint:

**Method 1: Create a new pull request**
```json
{
  "title": "string",
  "head": "string", 
  "base": "string",
  "body": "string",
  "maintainer_can_modify": true,
  "draft": false
}
```

**Method 2: Create a pull request from an existing issue**
```json
{
  "issue": 1,
  "head": "string",
  "base": "string", 
  "maintainer_can_modify": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | **Method 1 only** | The title of the pull request. Required when creating a new pull request |
| `body` | `string` | No | The contents of the pull request description. Can be `null`. Only used in Method 1 |
| `draft` | `boolean` | No | Indicates whether the pull request is a draft. Can be `null`. Default: `false`. Only used in Method 1 |
| `issue` | `integer` | **Method 2 only** | The issue number to convert to a pull request. Required when creating from existing issue |
| `head` | `string` | **Yes** | The name of the branch where your changes are implemented. For cross-repository pull requests, use the format `username:branch` |
| `base` | `string` | **Yes** | The name of the branch you want the changes pulled into |
| `maintainer_can_modify` | `boolean` | No | Indicates whether maintainers can modify the pull request. Can be `null`. Default: `false` |

**Note:** When using Method 2 (creating from an existing issue), the title and body will be taken from the existing issue, so these fields should be omitted from the request.

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Repository not found or invalid parameters |

##### Response Body

Returns the created pull request object with the same structure as in the "Get a Pull Request" endpoint.

### 4. Update a Pull Request

Updates an existing pull request.

**Endpoint:** `PATCH /api/v3/repos/:owner/:repository/pulls/:id`

#### Request

```
PATCH /api/v3/repos/:owner/:repository/pulls/:id
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The pull request number. |

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
  "state": "string",
  "base": "string",
  "maintainer_can_modify": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | No | The title of the pull request. Can be `null` |
| `body` | `string` | No | The contents of the pull request description. Can be `null` |
| `state` | `string` | No | State of the pull request. Can be `open` or `closed`. Can be `null` |
| `base` | `string` | No | The name of the branch you want the changes pulled into. Can be `null` |
| `maintainer_can_modify` | `boolean` | No | Indicates whether maintainers can modify the pull request. Can be `null` |

**Note:** All fields are optional, but at least one field should be provided to update the pull request.

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Pull request or repository not found |

##### Response Body

Returns the updated pull request object with the same structure as in the "Get a Pull Request" endpoint.

### 5. List Commits on a Pull Request

Retrieves a list of commits for a specific pull request.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/pulls/:id/commits`

#### Request

```
GET /api/v3/repos/:owner/:repository/pulls/:id/commits
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The pull request number. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Pull request or repository not found |

##### Response Body

Returns an array of commit objects.

### 6. Check if a Pull Request Has Been Merged

> **⚠️ GitBucket Implementation Issue:** GitBucket's implementation differs significantly from GitHub's API and has logical problems.

Checks if a pull request has been merged.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/pulls/:id/merge`

#### GitBucket vs GitHub Behavior

| Scenario | GitHub API | GitBucket API | GitBucket Logic Issue |
|----------|------------|---------------|----------------------|
| **Pull request is merged** | 204 No Content | 204 No Content | ✅ Correct |
| **Pull request is not merged** | 404 Not Found | 404 Not Found | ✅ Correct |
| **Pull request has conflicts** | 404 Not Found | **204 No Content** | ❌ **Wrong** |
| **Pull request is mergeable** | 404 Not Found | **204 No Content** | ❌ **Wrong** |

#### GitBucket's Implementation Problem

GitBucket uses `checkConflict()` function which checks **merge possibility**, not **merge status**:

- **Returns 204** when: Pull request is mergeable OR has conflicts (both cases!)
- **Returns 404** when: Merge status is unknown/uncached

This means GitBucket returns 204 for both:
1. ✅ **Actually merged pull requests** (correct)
2. ❌ **Unmerged but mergeable pull requests** (incorrect)
3. ❌ **Unmerged pull requests with conflicts** (incorrect)

#### Request

```
GET /api/v3/repos/:owner/:repository/pulls/:id/merge
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The pull request number. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 204 | **GitBucket**: Pull request is mergeable, has conflicts, OR is actually merged |
| 404 | **GitBucket**: Merge status unknown or pull request/repository not found |

**Note:** Due to GitBucket's implementation issue, you cannot reliably determine if a pull request is actually merged using this endpoint.

### 7. Merge a Pull Request

Merges a pull request.

**Endpoint:** `PUT /api/v3/repos/:owner/:repository/pulls/:id/merge`

#### Request

```
PUT /api/v3/repos/:owner/:repository/pulls/:id/merge
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The pull request number. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "commit_title": "string",
  "commit_message": "string",
  "merge_method": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `commit_title` | `string` | No | Title for the automatic commit message. Can be `null`. **Note: Currently not implemented in GitBucket** |
| `commit_message` | `string` | No | Extra detail to append to automatic commit message. Can be `null`. Default: empty string |
| `merge_method` | `string` | No | Merge method to use. Can be `merge` or `merge-commit`. Can be `null`. Default: `merge-commit` |

**Note:** All fields are optional. If no body is provided or all fields are `null`, default values will be used.

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 405 | Method Not Allowed (pull request is not mergeable) |
| 409 | Conflict (head branch was modified) |

##### Response Body

Success:
```json
{
  "sha": "string",
  "merged": true,
  "message": "string"
}
```

Error:
```json
{
  "documentation_url": "string",
  "message": "string"
}
```

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/pulls
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Pull Request Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiPullRequestControllerBase.scala`
  - API Pull Request: `gitbucket/src/main/scala/gitbucket/core/api/ApiPullRequest.scala`
  - Create A Pull Request: `gitbucket/src/main/scala/gitbucket/core/api/CreateAPullRequest.scala`
  - Merge A Pull Request: `gitbucket/src/main/scala/gitbucket/core/api/MergeAPullRequest.scala`
