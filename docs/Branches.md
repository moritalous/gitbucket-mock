# GitBucket API Documentation

## Branches API

### 1. List Branches

Retrieves a list of branches for a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/branches`

#### Request

```
GET /api/v3/repos/:owner/:repository/branches
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

Returns an array of branch objects with the following structure:

```json
[
  {
    "name": "string",
    "commit": {
      "sha": "string"
    }
  }
]
```

### 2. Get a Branch

Retrieves information about a specific branch.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/branches/:branch`

#### Request

```
GET /api/v3/repos/:owner/:repository/branches/:branch
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `branch` | `string` | **Required**. The name of the branch. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Branch or repository not found |

##### Response Body

Returns a branch object with the following structure:

```json
{
  "name": "string",
  "commit": {
    "sha": "string"
  },
  "protection": {
    "url": "string",
    "enabled": "boolean",
    "required_status_checks": {
      "url": "string",
      "enforcement_level": "string",
      "contexts": ["string"],
      "contexts_url": "string"
    }
  },
  "_links": {
    "self": "string",
    "html": "string"
  }
}
```

The `enforcement_level` field can be one of: `"off"`, `"non_admins"`, or `"everyone"`.

### 3. Get Branch Protection

Retrieves the protection settings for a branch.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/branches/:branch/protection`

#### Request

```
GET /api/v3/repos/:owner/:repository/branches/:branch/protection
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `branch` | `string` | **Required**. The name of the branch. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Branch or repository not found |

##### Response Body

Returns a branch protection object with the following structure:

```json
{
  "url": "string",
  "enabled": "boolean",
  "required_status_checks": {
    "url": "string",
    "enforcement_level": "string",
    "contexts": ["string"],
    "contexts_url": "string"
  }
}
```

### 4. Get Required Status Checks

Retrieves the required status checks for a protected branch.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/branches/:branch/protection/required_status_checks`

#### Request

```
GET /api/v3/repos/:owner/:repository/branches/:branch/protection/required_status_checks
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `branch` | `string` | **Required**. The name of the branch. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Branch or repository not found |

##### Response Body

Returns a status checks object with the following structure:

```json
{
  "url": "string",
  "enforcement_level": "string",
  "contexts": ["string"],
  "contexts_url": "string"
}
```

### 5. Get Required Status Check Contexts

Retrieves the required status check contexts for a protected branch.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/branches/:branch/protection/required_status_checks/contexts`

#### Request

```
GET /api/v3/repos/:owner/:repository/branches/:branch/protection/required_status_checks/contexts
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `branch` | `string` | **Required**. The name of the branch. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Branch or repository not found, or branch protection not enabled |

##### Response Body

Returns an array of strings representing the required status check contexts.

### 6. Update Branch Protection

Updates the protection settings for a branch.

**Endpoint:** `PATCH /api/v3/repos/:owner/:repository/branches/:branch`

#### Request

```
PATCH /api/v3/repos/:owner/:repository/branches/:branch
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `branch` | `string` | **Required**. The name of the branch. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "protection": {
    "enabled": true,
    "required_status_checks": {
      "enforcement_level": "off",
      "contexts": ["string"]
    }
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protection` | `object` | **Yes** | Branch protection configuration |
| `protection.enabled` | `boolean` | **Yes** | Whether branch protection is enabled |
| `protection.required_status_checks` | `object` | No | Required status checks configuration. Can be `null` |
| `protection.required_status_checks.enforcement_level` | `string` | **Yes** | The enforcement level. Can be `"off"`, `"non_admins"`, or `"everyone"` |
| `protection.required_status_checks.contexts` | `array[string]` | **Yes** | The list of status checks to require in order to merge into this branch |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 403 | Forbidden (not repository owner) |
| 404 | Branch or repository not found |

##### Response Body

Returns the updated branch object.

### 7. Delete Branch Protection

Removes the protection settings from a branch.

**Endpoint:** `DELETE /api/v3/repos/:owner/:repository/branches/:branch/protection`

#### Request

```
DELETE /api/v3/repos/:owner/:repository/branches/:branch/protection
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `branch` | `string` | **Required**. The name of the branch. |

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
| 403 | Forbidden (not repository owner) |
| 404 | Branch or repository not found, or branch protection not enabled |

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/branches
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Branch Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiRepositoryBranchControllerBase.scala`
  - API Branch: `gitbucket/src/main/scala/gitbucket/core/api/ApiBranch.scala`
  - API Branch Protection: `gitbucket/src/main/scala/gitbucket/core/api/ApiBranchProtection.scala`
