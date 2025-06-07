# GitBucket API Documentation

## Contents API

### 1. Get Repository README

Retrieves the README file from a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/readme`

#### Request

```
GET /api/v3/repos/:owner/:repository/readme
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `ref` | `string` | Optional. The name of the commit/branch/tag. Default: the repository's default branch (usually `main`). |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |
| `Accept` | `string` | Optional. Media type to specify the format of the response. Can be `application/vnd.github.v3.raw` for raw content, `application/vnd.github.v3.html` for HTML-rendered content, or omitted for JSON metadata. |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Repository or README not found |

##### Response Body

Returns a file object with the following structure (when Accept header is not specified):

```json
{
  "type": "file",
  "name": "string",
  "path": "string",
  "sha": "string",
  "content": "string",
  "encoding": "base64",
  "download_url": "string"
}
```

### 2. Get Contents

Retrieves the contents of a file or directory in a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/contents/:path`

#### Request

```
GET /api/v3/repos/:owner/:repository/contents/:path
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `path` | `string` | Optional. The path to the file or directory. Default: repository root. |
| `ref` | `string` | Optional. The name of the commit/branch/tag. Default: the repository's default branch (usually `main`). |
| `large_file` | `boolean` | Optional. Set to `true` to retrieve large files. Default: `false`. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |
| `Accept` | `string` | Optional. Media type to specify the format of the response. Can be `application/vnd.github.v3.raw` for raw content, `application/vnd.github.v3.html` for HTML-rendered content, or omitted for JSON metadata. |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | File, directory, or repository not found |

##### Response Body

**Note:** The response format depends on whether the path points to a file or directory:

**When path is a file:**
Returns a single content object:

```json
{
  "type": "file",
  "name": "string",
  "path": "string", 
  "sha": "string",
  "content": "string",
  "encoding": "base64",
  "download_url": "string"
}
```

**When path is a directory:**
Returns an array of content objects:

```json
[
  {
    "type": "file",
    "name": "string",
    "path": "string",
    "sha": "string",
    "download_url": "string"
  },
  {
    "type": "dir", 
    "name": "string",
    "path": "string",
    "sha": "string",
    "download_url": "string"
  }
]
```

**Response Schema:**
For OpenAPI compatibility, the response is always treated as an array. When the path points to a file, the response will be an array containing a single content object. When the path points to a directory, the response will be an array containing multiple content objects.

**Unified Response Format:**
```json
[
  {
    "type": "file|dir",
    "name": "string", 
    "path": "string",
    "sha": "string",
    "content": "string",
    "encoding": "base64",
    "download_url": "string"
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | `string` | The type of content. Either `"file"` or `"dir"` |
| `name` | `string` | The name of the file or directory |
| `path` | `string` | The path to the file or directory |
| `sha` | `string` | The SHA hash of the content |
| `content` | `string` | The Base64-encoded content of the file. Only present for files, not directories |
| `encoding` | `string` | The encoding used for the content. Always `"base64"` when present. Only present for files |
| `download_url` | `string` | The URL to download the raw content |

### 3. Create or Update a File

Creates a new file or updates an existing file in a repository.

**Endpoint:** `PUT /api/v3/repos/:owner/:repository/contents/:path`

#### Request

```
PUT /api/v3/repos/:owner/:repository/contents/:path
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `path` | `string` | **Required**. The path to the file. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "message": "string",
  "content": "string",
  "sha": "string",
  "branch": "string",
  "committer": {
    "name": "string",
    "email": "string"
  },
  "author": {
    "name": "string",
    "email": "string"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | `string` | **Yes** | The commit message |
| `content` | `string` | **Yes** | The new file content, Base64 encoded |
| `sha` | `string` | No | The blob SHA of the file being replaced. Required when updating a file. Can be `null` |
| `branch` | `string` | No | The branch name to commit to. Can be `null`. Default: the repository's default branch (usually `main`) |
| `committer` | `object` | No | The person that committed the file. Can be `null`. Default: the authenticated user |
| `committer.name` | `string` | No | The name of the committer |
| `committer.email` | `string` | No | The email of the committer |
| `author` | `object` | No | The author of the file. Can be `null`. Default: the committer or the authenticated user |
| `author.name` | `string` | No | The name of the author |
| `author.email` | `string` | No | The email of the author |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Repository not found |
| 409 | Conflict (SHA mismatch) |

##### Response Body

Returns an object with the following structure:

```json
{
  "content": {
    "type": "file",
    "name": "string",
    "path": "string",
    "sha": "string",
    "content": "string",
    "encoding": "base64",
    "download_url": "string"
  },
  "commit": {
    "sha": "string",
    "url": "string",
    "html_url": "string",
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
    "tree": {
      "sha": "string",
      "url": "string"
    },
    "parents": [
      {
        "sha": "string",
        "url": "string",
        "html_url": "string"
      }
    ]
  }
}
```

### 4. Get Raw File Content

Retrieves the raw content of a file in a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/raw/*`

#### Request

```
GET /api/v3/repos/:owner/:repository/raw/{ref}/{path}
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `ref` | `string` | **Required**. The name of the commit/branch/tag. Part of the path parameter. |
| `path` | `string` | **Required**. The path to the file. Part of the path parameter. |

**Note:** The `ref` and `path` are combined as a single path parameter in the URL (e.g., `/api/v3/repos/owner/repo/raw/main/src/file.txt`).

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | File or repository not found |

##### Response Body

Returns the raw content of the file.

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/repos/contents
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Contents Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiRepositoryContentsControllerBase.scala`
  - API Contents: `gitbucket/src/main/scala/gitbucket/core/api/ApiContents.scala`
  - Create A File: `gitbucket/src/main/scala/gitbucket/core/api/CreateAFile.scala`
