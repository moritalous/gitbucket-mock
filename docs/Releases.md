# GitBucket API Documentation

## Releases API

> **⚠️ Important GitBucket vs GitHub Differences:**
> 
> GitBucket's Release API differs significantly from GitHub's API:
> - **No Release ID concept**: GitBucket uses tag names instead of release IDs
> - **Missing endpoint**: `GET /api/v3/repos/:owner/:repository/releases/:id` is **NOT implemented**
> - **Tag-based operations**: Update and delete operations use `:tag` instead of `:release_id`
> - **Asset handling**: Asset operations require both tag name and file ID
> 
> Use tag-based endpoints or the releases list to access specific releases.

### 1. List Releases

Retrieves a list of releases for a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/releases`

#### Request

```
GET /api/v3/repos/:owner/:repository/releases
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

Returns an array of release objects with the following structure:

```json
[
  {
    "name": "string",
    "tag_name": "string",
    "body": "string",
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
    "assets": [
      {
        "name": "string",
        "size": 0,
        "label": "string",
        "file_id": "string",
        "browser_download_url": "string"
      }
    ]
  }
]
```

### 2. Get the Latest Release

Retrieves the latest release for a repository.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/releases/latest`

#### Request

```
GET /api/v3/repos/:owner/:repository/releases/latest
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
| 404 | No releases found or repository not found |

##### Response Body

Returns a release object with the same structure as in the "List Releases" endpoint.

### 3. Get a Release by Tag Name

> **⚠️ GitBucket Specific:** This is the primary way to get a specific release in GitBucket since release IDs are not supported.

Retrieves a specific release by its tag name.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/releases/tags/:tag`

#### Request

```
GET /api/v3/repos/:owner/:repository/releases/tags/:tag
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `tag` | `string` | **Required**. The tag name of the release. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Release not found or repository not found |

##### Response Body

Returns a release object with the same structure as in the "List Releases" endpoint.

### 4. Create a Release

Creates a new release in a repository.

**Endpoint:** `POST /api/v3/repos/:owner/:repository/releases`

#### Request

```
POST /api/v3/repos/:owner/:repository/releases
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
  "tag_name": "string",
  "target_commitish": "string",
  "name": "string",
  "body": "string",
  "draft": false,
  "prerelease": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag_name` | `string` | **Yes** | The name of the tag for this release |
| `target_commitish` | `string` | No | The commitish value that determines where the Git tag is created from. Can be any branch or commit SHA. Can be `null` |
| `name` | `string` | No | The name of the release. If omitted, GitBucket uses the tag name. Can be `null` |
| `body` | `string` | No | Text describing the release. Can be `null` |
| `draft` | `boolean` | No | Whether the release is a draft. Can be `null`. Default: `false`. **Note: Not used in current GitBucket implementation** |
| `prerelease` | `boolean` | No | Whether the release is a prerelease. Can be `null`. Default: `false`. **Note: Not used in current GitBucket implementation** |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Repository not found |

##### Response Body

Returns the created release object with the same structure as in the "Get a Release by Tag Name" endpoint.

### 5. Update a Release

> **⚠️ GitBucket Specific:** Uses `:tag` parameter instead of `:release_id` like GitHub API.

Updates an existing release.

**Endpoint:** `PATCH /api/v3/repos/:owner/:repository/releases/:tag`

#### Request

```
PATCH /api/v3/repos/:owner/:repository/releases/:tag
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `tag` | `string` | **Required**. The tag name of the release to update. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. Must be `application/json` |

#### Request Body

```json
{
  "tag_name": "string",
  "target_commitish": "string",
  "name": "string",
  "body": "string",
  "draft": false,
  "prerelease": false
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tag_name` | `string` | No | The name of the tag for this release. Can be `null` |
| `target_commitish` | `string` | No | The commitish value that determines where the Git tag is created from. Can be any branch or commit SHA. Can be `null` |
| `name` | `string` | No | The name of the release. If omitted, GitBucket uses the tag name. Can be `null` |
| `body` | `string` | No | Text describing the release. Can be `null` |
| `draft` | `boolean` | No | Whether the release is a draft. Can be `null`. Default: `false`. **Note: Not used in current GitBucket implementation** |
| `prerelease` | `boolean` | No | Whether the release is a prerelease. Can be `null`. Default: `false`. **Note: Not used in current GitBucket implementation** |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Release not found or repository not found |

##### Response Body

Returns the updated release object with the same structure as in the "Get a Release by Tag Name" endpoint.

### 6. Delete a Release

> **⚠️ GitBucket Specific:** Uses `:tag` parameter instead of `:release_id` like GitHub API.

Deletes a release from a repository.

**Endpoint:** `DELETE /api/v3/repos/:owner/:repository/releases/:tag`

#### Request

```
DELETE /api/v3/repos/:owner/:repository/releases/:tag
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `tag` | `string` | **Required**. The tag name of the release to delete. |

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
| 404 | Release not found or repository not found |

### 7. Upload a Release Asset

> **⚠️ Implementation Note:** While GitBucket implements this endpoint, it may encounter issues in certain environments due to file system dependencies and directory creation requirements.

Uploads an asset to a release.

**Endpoint:** `POST /api/v3/repos/:owner/:repository/releases/:tag/assets`

#### GitBucket Implementation Details

GitBucket's asset upload implementation:
- Uses `request.inputStream.available()` for file size detection
- Requires write permissions to the release files directory
- Generates unique file IDs for asset identification
- May fail with 500 errors in restricted environments

#### Request

```
POST /api/v3/repos/:owner/:repository/releases/:tag/assets?name=example.zip
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `tag` | `string` | **Required**. The tag name of the release. |
| `name` | `string` | **Required**. The name of the asset. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | **Required**. Authentication token in the format: `token {personal_access_token}` |
| `Content-Type` | `string` | **Required**. The content type of the asset. |
| `Content-Length` | `integer` | **Required**. The size of the asset in bytes. |

#### Request Body

The raw binary content of the asset.

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 401 | Unauthorized |
| 404 | Release not found or repository not found |
| 500 | Internal Server Error (common in restricted environments) |

##### Response Body

Returns the uploaded asset object:

```json
{
  "name": "string",
  "size": 0,
  "label": "string",
  "file_id": "string",
  "browser_download_url": "string"
}
```

### 8. Get a Release Asset

> **⚠️ GitBucket Specific:** Requires both `:tag` and `:fileId` parameters, unlike GitHub which only needs `:asset_id`.

Retrieves a specific release asset.

**Endpoint:** `GET /api/v3/repos/:owner/:repository/releases/:tag/assets/:fileId`

#### Request

```
GET /api/v3/repos/:owner/:repository/releases/:tag/assets/:fileId
```

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `owner` | `string` | **Required**. The owner of the repository. |
| `repository` | `string` | **Required**. The name of the repository. |
| `tag` | `string` | **Required**. The tag name of the release. |
| `fileId` | `string` | **Required**. The file ID of the asset. |

#### Headers

| Name | Type | Description |
|------|------|-------------|
| `Authorization` | `string` | Optional. Authentication token in the format: `token {personal_access_token}` |

#### Response

##### Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Asset not found, release not found, or repository not found |

##### Response Body

Returns the asset object with the same structure as in the "Upload a Release Asset" endpoint.

## GitBucket vs GitHub API Differences

### Missing Endpoints

The following GitHub API endpoints are **NOT implemented** in GitBucket:

- `GET /api/v3/repos/:owner/:repository/releases/:id` - Get a single release by ID
- `PATCH /api/v3/repos/:owner/:repository/releases/:id` - Update a release by ID  
- `DELETE /api/v3/repos/:owner/:repository/releases/:id` - Delete a release by ID
- `GET /api/v3/repos/:owner/:repository/releases/:id/assets` - List assets for a release by ID
- `PATCH /api/v3/repos/:owner/:repository/releases/assets/:asset_id` - Edit a release asset
- `DELETE /api/v3/repos/:owner/:repository/releases/assets/:asset_id` - Delete a release asset

### Key Differences

| Feature | GitHub API | GitBucket API | Notes |
|---------|------------|---------------|-------|
| Release Identification | Uses release ID | Uses tag name | GitBucket has no release ID concept |
| Get specific release | `/releases/:id` | `/releases/tags/:tag` | Must use tag-based endpoint |
| Update release | `/releases/:id` | `/releases/:tag` | Tag-based parameter |
| Delete release | `/releases/:id` | `/releases/:tag` | Tag-based parameter |
| Asset identification | Uses asset ID only | Uses tag + file ID | Requires both parameters |
| Draft releases | Supported | **Not implemented** | `draft` field ignored |
| Prerelease flag | Supported | **Not implemented** | `prerelease` field ignored |

### Workarounds

To work with GitBucket's Release API:

1. **To get a specific release**: Use `/releases/tags/:tag` instead of `/releases/:id`
2. **To find a release ID equivalent**: Use the tag name throughout your application
3. **To list and filter**: Use `/releases` and filter client-side by tag name
4. **For asset operations**: Always provide both tag name and file ID

## References

- GitBucket API documentation from README.md
- GitHub REST API documentation: https://docs.github.com/en/rest/releases
- GitBucket source code:
  - Controller: `gitbucket/src/main/scala/gitbucket/core/controller/ApiController.scala`
  - Release Controller: `gitbucket/src/main/scala/gitbucket/core/controller/api/ApiReleaseControllerBase.scala`
  - API Release: `gitbucket/src/main/scala/gitbucket/core/api/ApiRelease.scala`
  - Create A Release: `gitbucket/src/main/scala/gitbucket/core/api/CreateARelease.scala`
