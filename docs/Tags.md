# GitBucket API Documentation

## Tags API

### 1. List Repository Tags

Retrieves a list of tags for a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/tags`

#### Request

```
GET /api/v3/repos/:owner/:repository/tags
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

Returns an array of tag objects with the following structure:

```json
[
  {
    "name": "string",
    "commit": {
      "sha": "string",
      "url": "string"
    },
    "zipball_url": "string",
    "tarball_url": "string"
  }
]
```

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/repos/tags
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Repository Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiRepositoryControllerBase.scala`
  - API Tag: `gitbucket/src/main/scala/gitbucket/core/api/ApiTag.scala`
