# GitBucket API Documentation

## Labels API

### 1. List Labels for a Repository

Retrieves a list of all labels for a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/labels`

#### Request

```
GET /api/v3/repos/:owner/:repository/labels
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

Returns an array of label objects with the following structure:

```json
[
  {
    "name": "string",
    "color": "string",
    "url": "string"
  }
]
```

### 2. Get a Label

Retrieves a specific label.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/labels/:labelName`

#### Request

```
GET /api/v3/repos/:owner/:repository/labels/:labelName
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `labelName` | `string` | **Required**. The name of the label. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Label or repository not found |

##### Response Body

Returns a label object with the following structure:

```json
{
  "name": "string",
  "color": "string",
  "url": "string"
}
```

### 3. Create a Label

Creates a new label in a repository.

**Endpoint:** `POST /api/v3/repos/:owner/:repository/labels`

#### Request

```
POST /api/v3/repos/:owner/:repository/labels
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
  "name": "string",
  "color": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | **Yes** | The name of the label. Must be 100 characters or less and cannot start with an underscore or hyphen |
| `color` | `string` | **Yes** | The color of the label in 6-character hex code format (without #). Must contain only hexadecimal characters (a-f, A-F, 0-9) |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 201 | Created |
| 401 | Unauthorized |
| 404 | Repository not found |
| 422 | Unprocessable Entity (validation failed) |

##### Response Body

Returns the created label object with the same structure as in the "Get a Label" endpoint.

### 4. Update a Label

Updates an existing label.

**Endpoint:** `PATCH /api/v3/repos/:owner/:repository/labels/:labelName`

#### Request

```
PATCH /api/v3/repos/:owner/:repository/labels/:labelName
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `labelName` | `string` | **Required**. The name of the label to update. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "name": "string",
  "color": "string"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `string` | **Yes** | The new name of the label. Must be 100 characters or less and cannot start with an underscore or hyphen |
| `color` | `string` | **Yes** | The new color of the label in 6-character hex code format (without #). Must contain only hexadecimal characters (a-f, A-F, 0-9) |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Label or repository not found |
| 422 | Unprocessable Entity (validation failed) |

##### Response Body

Returns the updated label object with the same structure as in the "Get a Label" endpoint.

### 5. Delete a Label

Deletes a label from a repository.

**Endpoint:** `DELETE /api/v3/repos/:owner/:repository/labels/:labelName`

#### Request

```
DELETE /api/v3/repos/:owner/:repository/labels/:labelName
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `labelName` | `string` | **Required**. The name of the label to delete. |

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
| 404 | Label or repository not found |

### 6. List Labels on an Issue

Retrieves a list of all labels for a specific issue.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/issues/:id/labels`

#### Request

```
GET /api/v3/repos/:owner/:repository/issues/:id/labels
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

Returns an array of label objects with the same structure as in the "List Labels for a Repository" endpoint.

### 7. Add Labels to an Issue

Adds labels to an issue.

**Endpoint:** `POST /api/v3/repos/:owner/:repository/issues/:id/labels`

#### Request

```
POST /api/v3/repos/:owner/:repository/issues/:id/labels
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
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "labels": ["string"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `labels` | `array[string]` | **Yes** | An array of label names to add to the issue. If a label doesn't exist, it will be created |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Issue or repository not found |

##### Response Body

Returns an array of label objects that were added to the issue.

### 8. Remove a Label from an Issue

Removes a label from an issue.

**Endpoint:** `DELETE /api/v3/repos/:owner/:repository/issues/:id/labels/:name`

#### Request

```
DELETE /api/v3/repos/:owner/:repository/issues/:id/labels/:name
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `id` | `integer` | **Required**. The issue number. |
| `name` | `string` | **Required**. The name of the label to remove. |

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
| 404 | Label, issue, or repository not found |

##### Response Body

Returns an array containing the removed label.

### 9. Replace All Labels for an Issue

Replaces all labels for an issue.

**Endpoint:** `PUT /api/v3/repos/:owner/:repository/issues/:id/labels`

#### Request

```
PUT /api/v3/repos/:owner/:repository/issues/:id/labels
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
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "labels": ["string"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `labels` | `array[string]` | **Yes** | An array of label names to set on the issue. Any labels not in this list will be removed. If a label doesn't exist, it will be created |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Issue or repository not found |

##### Response Body

Returns an array of label objects that are now on the issue.

### 10. Remove All Labels from an Issue

Removes all labels from an issue.

**Endpoint:** `DELETE /api/v3/repos/:owner/:repository/issues/:id/labels`

#### Request

```
DELETE /api/v3/repos/:owner/:repository/issues/:id/labels
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
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 204 | Success (No Content) |
| 401 | Unauthorized |
| 404 | Issue or repository not found |

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/issues/labels
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Label Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiIssueLabelControllerBase.scala`
  - API Label: `gitbucket/src/main/scala/gitbucket/core/api/ApiLabel.scala`
  - Create A Label: `gitbucket/src/main/scala/gitbucket/core/api/CreateALabel.scala`
  - Add Labels To An Issue: `gitbucket/src/main/scala/gitbucket/core/api/AddLabelsToAnIssue.scala`
