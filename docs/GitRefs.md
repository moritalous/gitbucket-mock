# GitBucket API Documentation

## Git References API

### 1. List References

Retrieves a list of all references in a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/git/refs`

#### Request

```
GET /api/v3/repos/:owner/:repository/git/refs
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

Returns an array of reference objects with the following structure:

```json
[
  {
    "ref": "string",
    "node_id": "string",
    "url": "string",
    "object": {
      "sha": "string",
      "type": "string",
      "url": "string"
    }
  }
]
```

### 2. Get a Reference

Retrieves a specific reference.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/git/ref/:ref`

#### Request

```
GET /api/v3/repos/:owner/:repository/git/ref/:ref
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `ref` | `string` | **Required**. The name of the reference. For example, `heads/main` for a branch, `tags/v1.0.0` for a tag. |

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

Returns a reference object with the following structure:

```json
{
  "ref": "string",
  "node_id": "string",
  "url": "string",
  "object": {
    "sha": "string",
    "type": "string",
    "url": "string"
  }
}
```

### 3. Create a Reference

Creates a new reference.

**Endpoint:** `POST /api/v3/repos/:owner/:repository/git/refs`

#### Request

```
POST /api/v3/repos/:owner/:repository/git/refs
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
  "ref": "string",
  "sha": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ref` | `string` | **Yes** | The name of the reference to create. Must be formatted as `refs/heads/branch-name` for a branch or `refs/tags/tag-name` for a tag |
| `sha` | `string` | **Yes** | The SHA1 value of the object the reference points to |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Repository not found |
| 422 | Unprocessable entity (reference already exists or invalid SHA) |

##### Response Body

Returns the created reference object with the same structure as in the "Get a Reference" endpoint.

### 4. Update a Reference

Updates an existing reference.

**Endpoint:** `PATCH /api/v3/repos/:owner/:repository/git/refs/:ref`

#### Request

```
PATCH /api/v3/repos/:owner/:repository/git/refs/:ref
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `ref` | `string` | **Required**. The name of the reference to update. For example, `heads/main` for a branch, `tags/v1.0.0` for a tag. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "sha": "string",
  "force": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `sha` | `string` | **Yes** | The SHA1 value of the object the reference should point to |
| `force` | `boolean` | **Yes** | Whether to force the update even if it's not a fast-forward update |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Repository not found |
| 422 | Unprocessable entity (reference doesn't exist or invalid SHA) |

##### Response Body

Returns the updated reference object with the same structure as in the "Get a Reference" endpoint.

### 5. Delete a Reference

Deletes a reference.

**Endpoint:** `DELETE /api/v3/repos/:owner/:repository/git/refs/:ref`

#### Request

```
DELETE /api/v3/repos/:owner/:repository/git/refs/:ref
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `ref` | `string` | **Required**. The name of the reference to delete. For example, `heads/branch-name` for a branch, `tags/tag-name` for a tag. |

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
| 403 | Forbidden |
| 404 | Repository not found |
| 422 | Unprocessable entity (reference doesn't exist) |

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/git/refs
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Git Reference Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiGitReferenceControllerBase.scala`
  - API Ref: `gitbucket/src/main/scala/gitbucket/core/api/ApiRef.scala`
  - Create A Ref: `gitbucket/src/main/scala/gitbucket/core/api/CreateARef.scala`
  - Update A Ref: `gitbucket/src/main/scala/gitbucket/core/api/UpdateARef.scala`
