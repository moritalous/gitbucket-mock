# GitBucket API Documentation

## Root Endpoints API

### 1. Root Endpoint

Provides information about the API root endpoint.

**Endpoint:** `GET /api/v3`

#### Request

```
GET /api/v3
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

##### Response Body

Returns an object with information about the API:

```json
{
  "rate_limit_url": "/api/v3/rate_limit"
}
```

### 2. Rate Limit

Provides information about the API rate limit status. Note that rate limiting is not enabled in GitBucket.

**Endpoint:** `GET /api/v3/rate_limit`

#### Request

```
GET /api/v3/rate_limit
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
| 404 | Not Found |

##### Response Body

Returns an error message indicating that rate limiting is not enabled:

```json
{
  "message": "Rate limiting is not enabled."
}
```

### 3. List Installed Plugins

Retrieves a list of plugins installed in GitBucket. This is a GitBucket-specific API that is not part of the GitHub API.

**Endpoint:** `GET /api/v3/gitbucket/plugins`

#### Request

```
GET /api/v3/gitbucket/plugins
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

##### Response Body

Returns an array of plugin objects.

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/overview/resources-in-the-rest-api
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - API Endpoint: `gitbucket/src/main/scala/gitbucket/core/api/ApiEndPoint.scala`
